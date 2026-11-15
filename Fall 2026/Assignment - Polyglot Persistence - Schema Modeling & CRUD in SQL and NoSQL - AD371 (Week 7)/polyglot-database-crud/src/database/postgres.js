import pg from 'pg';
const { Pool } = pg;
export const pool = new Pool({
  connectionString: process.env.POSTGRES_URL || 'postgresql://polyglot:polyglot@127.0.0.1:55432/polyglot'
});
