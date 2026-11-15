import express from 'express';
import projectRoutes from './routes/projectRoutes.js';
import { connectMongo } from './database/mongo.js';

const app = express();
app.use(express.json());
app.use(express.static('public'));
app.use('/api', projectRoutes);
app.use((error, req, res, next) => {
  console.error(error);
  res.status(500).json({ error: 'Internal server error' });
});

if (process.env.NODE_ENV !== 'test') {
  connectMongo().then(() => app.listen(process.env.PORT || 3000, () => {
    console.log('API listening on port 3000');
  })).catch((error) => { console.error('Database startup failed', error); process.exitCode = 1; });
}

export default app;
