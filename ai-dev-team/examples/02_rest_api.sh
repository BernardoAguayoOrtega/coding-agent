#!/bin/bash
# Example 2: REST API

source ../.venv/bin/activate

python -m ai_dev_team "Build a REST API for a bookstore with:
- FastAPI framework
- SQLite database
- CRUD endpoints for books (GET, POST, PUT, DELETE)
- Each book has: id, title, author, isbn, price, published_date
- Input validation with Pydantic models
- Error handling middleware
- OpenAPI/Swagger documentation
- README with setup instructions
- Requirements.txt file"
