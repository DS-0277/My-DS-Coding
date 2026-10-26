require('dotenv').config();

const express = require('express');
const session = require('express-session');
const bcrypt = require('bcrypt');
const Database = require('better-sqlite3');
const path = require('path');

const app = express();
const port = Number(process.env.PORT || 3000);
const sessionSecret = process.env.SESSION_SECRET;
const isProduction = process.env.NODE_ENV === 'production';

if (!sessionSecret) {
  throw new Error('SESSION_SECRET must be configured in the environment.');
}

const db = new Database('auth-rbac.db');
db.pragma('foreign_keys = ON');
db.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'User' CHECK (role IN ('User', 'Admin')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
  )
`);

async function ensureAdminAccount() {
  const adminUsername = process.env.ADMIN_USERNAME;
  const adminPassword = process.env.ADMIN_PASSWORD;
  if (!adminUsername || !adminPassword) return;
  if (adminPassword.length < 12) throw new Error('ADMIN_PASSWORD must be at least 12 characters.');

  const existing = db.prepare('SELECT id FROM users WHERE username = ?').get(adminUsername);
  if (!existing) {
    const passwordHash = await bcrypt.hash(adminPassword, 12);
    db.prepare('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)')
      .run(adminUsername, passwordHash, 'Admin');
  }
}

app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(express.static(path.join(__dirname, 'public')));
app.use(session({
  secret: sessionSecret,
  resave: false,
  saveUninitialized: false,
  cookie: { httpOnly: true, sameSite: 'lax', secure: isProduction, maxAge: 60 * 60 * 1000 }
}));

const failedLogins = new Map();
function loginRateLimited(username) {
  const attempt = failedLogins.get(username);
  if (!attempt) return false;
  if (Date.now() - attempt.startedAt > 15 * 60 * 1000) {
    failedLogins.delete(username);
    return false;
  }
  return attempt.count >= 5;
}

function recordFailedLogin(username) {
  const current = failedLogins.get(username);
  if (!current || Date.now() - current.startedAt > 15 * 60 * 1000) {
    failedLogins.set(username, { startedAt: Date.now(), count: 1 });
  } else {
    current.count += 1;
  }
}

function requireAuth(req, res, next) {
  if (!req.session.user) return res.status(401).json({ error: 'Authentication required.' });
  next();
}

function requireRole(role) {
  return (req, res, next) => {
    if (!req.session.user) return res.status(401).json({ error: 'Authentication required.' });
    if (req.session.user.role !== role) return res.status(403).json({ error: 'Forbidden.' });
    next();
  };
}

app.get('/', (req, res) => res.json({ message: 'Public resource.' }));

app.post('/register', async (req, res) => {
  const username = typeof req.body.username === 'string' ? req.body.username.trim() : '';
  const password = typeof req.body.password === 'string' ? req.body.password : '';
  if (!/^[A-Za-z0-9_]{3,32}$/.test(username) || password.length < 8 || password.length > 128) {
    return res.status(400).json({ error: 'Use a 3-32 character username and a password between 8 and 128 characters.' });
  }

  try {
    const passwordHash = await bcrypt.hash(password, 12);
    const result = db.prepare('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)')
      .run(username, passwordHash, 'User');
    res.status(201).json({ id: result.lastInsertRowid, username, role: 'User' });
  } catch (error) {
    if (error.code === 'SQLITE_CONSTRAINT_UNIQUE') return res.status(409).json({ error: 'Registration could not be completed.' });
    res.status(500).json({ error: 'Registration could not be completed.' });
  }
});

app.post('/login', async (req, res) => {
  const username = typeof req.body.username === 'string' ? req.body.username.trim() : '';
  const password = typeof req.body.password === 'string' ? req.body.password : '';
  if (!username || password.length > 128 || loginRateLimited(username)) {
    return res.status(401).json({ error: 'Invalid username or password.' });
  }
  const user = db.prepare('SELECT id, username, password_hash, role FROM users WHERE username = ?').get(username);
  const valid = user && await bcrypt.compare(password, user.password_hash);
  if (!valid) {
    recordFailedLogin(username);
    return res.status(401).json({ error: 'Invalid username or password.' });
  }

  req.session.regenerate((error) => {
    if (error) return res.status(500).json({ error: 'Login could not be completed.' });
    req.session.user = { id: user.id, username: user.username, role: user.role };
    failedLogins.delete(username);
    res.json({ message: 'Login successful.', user: req.session.user });
  });
});

app.post('/logout', requireAuth, (req, res) => {
  req.session.destroy((error) => {
    if (error) return res.status(500).json({ error: 'Logout could not be completed.' });
    res.clearCookie('connect.sid');
    res.json({ message: 'Logged out.' });
  });
});

app.get('/dashboard', requireAuth, (req, res) => res.json({ message: 'User dashboard.', user: req.session.user }));
app.get('/admin', requireRole('Admin'), (req, res) => res.json({ message: 'Admin resource.' }));

ensureAdminAccount().then(() => {
  app.listen(port, () => console.log(`Server listening on http://localhost:${port}`));
}).catch((error) => {
  console.error(error.message);
  process.exit(1);
});
