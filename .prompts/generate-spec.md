# Generate OpenAPI Specification with SpecMCP

Use the SpecMCP MCP server to generate a complete, production-ready OpenAPI 3.1 specification.

## Instructions

1. **Parse the constitution** first to understand project requirements:
   - Use `parse_constitution` tool with path `.specify/constitution.md`
   - Review the tech stack, patterns, and principles

2. **Generate the specification** based on these requirements:
   
   **API Requirements:**
   - User authentication API
   - Email/password registration
   - Login with JWT token generation
   - Logout functionality
   - User profile retrieval (requires authentication)
   - Password reset flow
   
   **Technical Requirements:**
   - Follow all constitution rules
   - Use JWT authentication (from constitution)
   - Include /health endpoint (required by constitution)
   - Add proper error responses (400, 401, 403, 404, 500)
   - Include request/response schemas
   - Add security schemes
   - Use proper HTTP methods
   
   **Endpoints to Include:**
   - `POST /auth/register` - Register new user
   - `POST /auth/login` - Login and get JWT token
   - `POST /auth/logout` - Logout (requires auth)
   - `GET /auth/me` - Get current user profile (requires auth)
   - `POST /auth/forgot-password` - Request password reset
   - `POST /auth/reset-password` - Reset password with token
   - `GET /health` - Health check (no auth required)

3. **Use the generate_openapi_spec tool** with:
```
   requirements: "User authentication API with registration, login, logout, profile management, and password reset. Include all CRUD operations for user management."
   constitution_path: ".specify/constitution.md"
   title: "Authentication API"
```

4. **Save the generated specification**:
   - Use `save_spec_to_file` tool
   - Save to path: `specs/auth-complete.json`
   - Format: json

5. **Verify compliance**:
   - Use `verify_spec_compliance` tool
   - Check the generated spec against constitution
   - Report compliance score and any violations

## Expected Output

You should generate a file `specs/auth-complete.json` that includes:

✅ OpenAPI 3.1.0 specification
✅ JWT bearer authentication configured
✅ All 7 endpoints with proper schemas
✅ Health check endpoint
✅ Request validation rules
✅ Response schemas for success and errors
✅ Security requirements on protected endpoints
✅ Follows all constitution rules

## Success Criteria

- File created at `specs/auth-complete.json`
- Compliance score: 100/100
- All endpoints documented
- Authentication properly configured
- Health endpoint present
- Passes constitution verification

