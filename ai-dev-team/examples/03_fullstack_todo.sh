#!/bin/bash
# Example 3: Full-stack Todo App

source ../.venv/bin/activate

python -m ai_dev_team "Build a full-stack todo application with:

Frontend:
- React with functional components and hooks
- Material-UI or Tailwind CSS for styling
- State management with Context API
- CRUD operations for todos
- Filter by status (all/active/completed)
- Responsive design

Backend:
- Node.js with Express
- RESTful API endpoints
- JWT authentication
- Input validation
- Error handling middleware

Database:
- PostgreSQL
- User table (id, email, password_hash)
- Todo table (id, user_id, title, description, status, created_at)
- Proper relationships and indexes

Features:
- User registration and login
- Protected routes
- Mark todos as complete/incomplete
- Delete todos
- Search/filter todos

Include:
- README with setup instructions
- Environment variable examples
- API documentation
- Test files for key functionality"
