---
name: database-schema-design
description: Design relational database schemas, create tables, and manage migrations efficiently.
---
Database Schema Design
Instructions
Schema planning

Identify entities and relationships

Define primary and foreign keys

Normalize data (avoid redundancy)

Table creation

Use appropriate data types

Apply constraints (NOT NULL, UNIQUE)

Index frequently queried columns

Migrations

Version-controlled schema changes

Forward and rollback support

Safe, incremental updates

Best Practices
Follow naming conventions consistently

Prefer migrations over manual DB changes

Keep tables small and focused

Document schema decisions

Avoid over-normalization

Example Structure
sql
Copy code
-- users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- posts table
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  title VARCHAR(200) NOT NULL,
  content TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);