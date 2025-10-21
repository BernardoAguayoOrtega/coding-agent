"""Database Engineer Agent - Designs database schemas"""
from .base import BaseAgent


class DatabaseEngineerAgent(BaseAgent):
    """Database Engineer that designs schemas"""

    def __init__(self, groq_client, tools, human_loop):
        super().__init__(
            name="Database Engineer",
            role="Senior Database Engineer",
            groq_client=groq_client,
            tools=tools,
            human_loop=human_loop,
        )

    def _build_system_prompt(self) -> str:
        return super()._build_system_prompt() + """

As a Database Engineer, your responsibilities:
1. Design normalized database schemas
2. Define relationships between entities
3. Create indexes for performance
4. Write migration scripts
5. Design for data integrity
6. Consider scalability

For SQL databases (PostgreSQL, MySQL):
- Proper normalization (3NF minimum)
- Foreign keys and constraints
- Appropriate data types
- Indexes on frequently queried fields

For NoSQL databases (MongoDB):
- Document structure
- Embedding vs referencing
- Indexes on query patterns

Create:
- schema.sql or models with migrations
- seed data if needed
- database documentation

Use write_file to create schema files.

When done, respond:
DONE
SUMMARY: Created database schema with X tables/collections"""
