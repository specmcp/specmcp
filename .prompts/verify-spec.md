# Verify Specification Compliance

Use the SpecMCP MCP server to verify an existing OpenAPI specification follows the project constitution.

## Instructions

1. **Choose a spec file to verify** (or specify the path)
   - Example: `specs/auth-api.json`
   - Or any other OpenAPI spec in the project

2. **Parse the constitution**:
   - Use `parse_constitution` tool
   - Path: `.specify/constitution.md`

3. **Verify the specification**:
   - Use `verify_spec_compliance` tool
   - Load the spec file content
   - Compare against constitution rules

4. **Report results**:
   - Compliance score (0-100)
   - List of violations (if any)
   - Severity of each violation
   - Recommendations for fixes

## Expected Output

A detailed compliance report showing:

- ✅ Overall compliance score
- ✅ List of rules checked
- ✅ Violations found (if any)
- ✅ Suggestions for remediation

## Example Report Format
```
Specification Compliance Report
================================

File: specs/auth-api.json
Constitution: .specify/constitution.md

Score: 80/100

Violations Found: 2

1. [ERROR] Authentication Required
   - Constitution requires JWT authentication
   - Spec is missing security scheme
   - Fix: Add JWT to components.securitySchemes

2. [WARNING] Health Endpoint Required
   - Constitution requires /health endpoint
   - Not found in spec
   - Fix: Add GET /health endpoint

Recommendations:
- Add JWT bearer authentication scheme
- Add /health endpoint for monitoring
- Update security requirements on protected endpoints

