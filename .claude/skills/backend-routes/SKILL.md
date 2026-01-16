---
name: backend-routes
description: Build backend functionality by generating API routes, handling requests/responses, and connecting to databases.
---

# Backend API Development

## Instructions

1. **Routing**
   - Define RESTful API endpoints
   - Use clear URL naming conventions
   - Separate routes by feature/module

2. **Request & Response Handling**
   - Parse request body, params, and query
   - Validate incoming data
   - Return structured JSON responses
   - Handle errors with proper status codes

3. **Database Integration**
   - Connect to database (SQL / NoSQL)
   - Perform CRUD operations
   - Use models or schemas
   - Handle connection errors safely

## Best Practices
- Follow REST conventions
- Use proper HTTP status codes
- Keep controllers thin and reusable
- Secure routes with validation and auth
- Use environment variables for secrets

## Example Structure
```js
// Express.js example
import express from "express";
import mongoose from "mongoose";

const app = express();
app.use(express.json());

app.get("/api/users", async (req, res) => {
  const users = await User.find();
  res.status(200).json(users);
});

app.post("/api/users", async (req, res) => {
  const user = new User(req.body);
  await user.save();
  res.status(201).json(user);
});
