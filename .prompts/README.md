# SpecMCP Prompts

Ready-to-use prompts for Claude Code to interact with the SpecMCP MCP server.

## Available Prompts

### 1. Generate OpenAPI Specification
**File:** `generate-spec.md`

**Use when:** You need to create a new API specification from scratch

**What it does:**
- Parses your constitution
- Generates complete OpenAPI 3.1 spec
- Includes all required endpoints
- Adds authentication and security
- Saves to file
- Verifies compliance

**Quick use:**
```
"Follow the instructions in .prompts/generate-spec.md"
```

### 2. Verify Specification Compliance
**File:** `verify-spec.md`

**Use when:** You want to check if a spec follows your constitution

**What it does:**
- Loads existing spec file
- Compares against constitution rules
- Reports violations and score
- Provides fix recommendations

**Quick use:**
```
"Follow the instructions in .prompts/verify-spec.md to check specs/auth-api.json"
```

### 3. Parse Constitution
**File:** `parse-constitution.md`

**Use when:** You want to understand the project's technical requirements

**What it does:**
- Reads constitution file
- Extracts tech stack, patterns, principles
- Summarizes key requirements

**Quick use:**
```
"Follow the instructions in .prompts/parse-constitution.md"
```

## How to Use

### Method 1: Reference the file
```
"Please follow the instructions in .prompts/generate-spec.md"
```

### Method 2: Copy-paste the prompt
Copy the content from any `.md` file and paste it into Claude Code

### Method 3: Quick command
```
"Use SpecMCP to generate an auth API spec following .prompts/generate-spec.md"
```

## Tips

- **Be specific:** The more details you provide, the better the output
- **Use constitution:** Always reference the constitution for consistency
- **Verify after generating:** Check compliance to catch issues early
- **Iterate:** Generate, verify, fix, repeat until 100% compliant

## Examples

### Generate a complete auth API
```
Follow .prompts/generate-spec.md to create a complete authentication API 
with registration, login, logout, and password reset
```

### Quick compliance check
```
Use SpecMCP to verify specs/my-api.json against the constitution 
and report any violations
```

### Understand project rules
```
Parse the constitution and tell me what authentication method 
and API style we must use
```

## Customizing Prompts

Feel free to modify these prompts for your needs:

1. Edit the `.md` files in this directory
2. Add your own requirements
3. Specify different endpoints or features
4. Adjust compliance criteria

## Need Help?

If Claude Code has trouble using the MCP server:

1. Check the server is configured: `cat .claude/config.json`
2. Verify venv is activated: `source venv/bin/activate`
3. Test manually: `python test_specmcp.py`
4. Check logs for errors

---

**Happy spec generation!** 🚀
