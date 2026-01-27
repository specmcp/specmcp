# Parse Project Constitution

Use the SpecMCP MCP server to parse and understand the project's constitution.

## Instructions

1. **Parse the constitution file**:
   - Use `parse_constitution` tool
   - Path: `.specify/constitution.md`

2. **Display the extracted information**:
   - Tech stack (language, framework, database, deployment)
   - Architectural patterns (microservices/monolith, REST/GraphQL/gRPC)
   - Authentication method (JWT, OAuth2, etc.)
   - Coding standards and principles
   - Any non-negotiable rules

3. **Summarize key points**:
   - What technology choices are mandated?
   - What patterns must be followed?
   - What are the quality requirements?

## Expected Output

A clear summary of the project's technical constitution:
```
Project Constitution Summary
============================

Tech Stack:
- Language: Python 3.11
- Framework: FastAPI
- Database: PostgreSQL
- Deployment: Docker

Architectural Patterns:
- Architecture: Microservices
- API Style: REST
- Authentication: JWT

Principles:
- Security first
- 100% test coverage required
- Type hints mandatory
- All endpoints require authentication
- Performance over convenience

Standards:
- Testing: Required
- Type hints: Required
- Documentation: Required

