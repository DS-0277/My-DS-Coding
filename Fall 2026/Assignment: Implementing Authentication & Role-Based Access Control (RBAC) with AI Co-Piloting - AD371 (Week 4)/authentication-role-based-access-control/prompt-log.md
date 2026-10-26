# AI Prompt Log

## Step 1: Initial Draft

- **AI tool:** ChatGPT
- **Date:** October 25, 2026
- **Technology requested:** Node.js, Express, SQLite, bcrypt, and express-session

### Exact prompt

> Act as a senior security engineer and instructor. Design a small Node.js and Express application that demonstrates secure authentication and role-based access control for an educational assignment.
>
> Use:
> - Node.js
> - Express
> - SQLite
> - bcrypt for password hashing
> - express-session for session-based authentication
> - A minimal HTML/CSS/JavaScript frontend
>
> The application must include:
> 1. User registration with username, password, and role.
> 2. Login and logout.
> 3. Two roles: User and Admin.
> 4. A public page accessible to everyone.
> 5. A protected dashboard accessible to any authenticated user.
> 6. An Admin-only page or endpoint.
> 7. Server-side authentication middleware.
> 8. Server-side role-checking middleware.
> 9. Input validation on both registration and login.
> 10. Generic login errors that do not reveal whether a username exists.
> 11. Environment variables for sensitive configuration.
> 12. Responses that never expose password hashes.
> 13. Appropriate 401 and 403 HTTP responses.
> 14. Protection against common insecure defaults.
>
> Public registration must always create a regular `User` account. Users must not be allowed to choose the `Admin` role from the registration form. An Admin account should be created through a controlled setup process.
>
> Explain the architecture, file responsibilities, security decisions, and any assumptions. Do not use plaintext passwords, MD5, ordinary SHA-256 password storage, client-only authorization, or hardcoded secrets. Produce a starter implementation that can be audited line by line.

## Step 1 output summary

The initial draft created a Node.js and Express server with:

- Registration and login endpoints
- bcrypt password hashing
- Session-based authentication
- User and Admin role checks
- Public, authenticated, and Admin-only endpoints
- Generic login failure messages
- Environment-based session configuration

## Step 2 audit findings

- **Password storage:** PASS. Passwords are hashed with bcrypt using a cost factor of 12. Password hashes are not returned in responses.
- **Server-side enforcement:** PASS. `requireAuth` protects the User dashboard, and `requireRole('Admin')` protects the Admin endpoint.
- **Generic login errors:** PASS. Failed login attempts return `Invalid username or password.` without revealing whether the username exists.
- **Secret handling:** PASS for the session secret. The server requires `SESSION_SECRET` from the environment instead of hardcoding it.
- **Role escalation prevention:** PASS for public registration. The server always assigns the `User` role and does not trust a role from the request body.
- **Required frontend:** GAP. No HTML/JavaScript interface currently exists for browser-based registration, login, logout, and role testing.
- **Admin test account:** GAP. There is no controlled setup process yet for creating an Admin account for testing.
- **Session fixation protection:** IMPROVEMENT NEEDED. Login should regenerate the session identifier after successful authentication.
- **Session storage:** IMPROVEMENT NEEDED. Express's default in-memory session store is suitable only for development and should be replaced or explicitly documented for production.
- **Cookie security:** IMPROVEMENT NEEDED. `secure: false` is appropriate for local HTTP testing but must be enabled when deployed over HTTPS.
- **Input validation:** IMPROVEMENT NEEDED. The current checks enforce a username presence and minimum password length, but should also enforce reasonable username length and format limits.
- **Abuse protection:** IMPROVEMENT NEEDED. Login has no rate limiting or lockout protection against repeated password guesses.
- **CSRF protection:** IMPROVEMENT NEEDED. Because the application uses cookie-based sessions, state-changing requests should use CSRF protection or an equivalent defense when deployed.
- **Error handling:** IMPROVEMENT NEEDED. Logout should handle session-destruction errors explicitly instead of always returning success.

### Audit conclusion

The draft demonstrates the required authentication and backend authorization concepts, but it needs the frontend, controlled Admin setup, and selected security hardening before Step 3 QA testing.

## Step 2 corrections

- Added `public/index.html` with browser controls for registration, login, logout, the User dashboard, and the Admin endpoint.
- Added controlled Admin provisioning through `ADMIN_USERNAME` and `ADMIN_PASSWORD` environment variables. Public registration still always creates `User` accounts.
- Added username format and length validation and password length limits.
- Added session regeneration after successful login to reduce session-fixation risk.
- Added configurable secure cookies: local development uses HTTP, while production enables the `secure` cookie flag.
- Added a basic development login-attempt throttle.
- Added explicit logout error handling and cookie clearing.

Remaining deployment considerations: replace the default in-memory session store with a persistent store, use HTTPS in production, and add a robust CSRF strategy and production-grade rate limiting before public deployment.
