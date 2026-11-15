import { MongoClient } from 'mongodb';
export const mongoClient = new MongoClient(process.env.MONGODB_URL || 'mongodb://127.0.0.1:27017');
export const mongoProjects = () => mongoClient.db('polyglot').collection('projects');
export async function connectMongo() { await mongoClient.connect(); }
export async function closeMongo() { await mongoClient.close(); }
