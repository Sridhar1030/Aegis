-- Create SonarQube database
CREATE DATABASE sonar;
-- Enable pgvector on the main application database
\c aegis
CREATE EXTENSION IF NOT EXISTS vector;