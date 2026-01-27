# SpecMCP

**Spec-Driven Development that actually works.**

Generate production-ready API specifications from simple markdown rules. Enforce them automatically. No drift. No manual work.

[![PyPI](https://badge.fury.io/py/specmcp.svg)](https://pypi.org/project/specmcp/)
[![npm](https://badge.fury.io/js/specmcp.svg)](https://www.npmjs.com/package/specmcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Stars](https://img.shields.io/github/stars/specmcp/core)](https://github.com/specmcp/core)

---

## The Problem

You write OpenAPI specs by hand. Your team writes them differently. Six months later, you have 50 APIs with 50 different patterns. Nobody knows what's standard anymore.

**The old solution:** Write a style guide. Hope people read it. They don't.

**The new solution:** Define rules once in markdown. Generate specs automatically. Enforce with tooling.

---

## What SpecMCP Does

### 1. You write rules in plain markdown
```markdown
# constitution.md

## Tech Stack
- Language: Python
- Framework: FastAPI
- Auth: JWT

## Rules
- All APIs need authentication
- Health endpoints required
- Use UUIDs for IDs
```

### 2. Your AI assistant generates specs that follow those rules
```bash
You: "Generate an auth API spec"

AI: [reads constitution.md]
    [generates OpenAPI 3.1 spec]
    
    ✅ JWT auth configured
    ✅ Health endpoint included
    ✅ UUID schemas defined
    ✅ Saved to specs/auth-api.json
```

### 3. SpecMCP enforces the rules in CI/CD
```bash
# In your CI pipeline
specmcp verify specs/*.json

# Output:
✅ auth-api.json: 100/100 compliance
❌ orders-api.json: 75/100 compliance
   - Missing health endpoint
   - Using integers instead of UUIDs
   BUILD FAILED
```

**That's it. Rules → Generation → Enforcement.**

---

## Installation
```bash
pip install specmcp        # Python
npm install -g specmcp     # JavaScript/TypeScript
brew install specmcp       # macOS
docker pull specmcp/specmcp # Docker
```

---

## Quick Start

### Create constitution.md
```bash
mkdir -p .specify
cat > .specify/constitution.md << 'EOF'
# Tech Stack
- Framework: FastAPI
- Auth: JWT
- Database: PostgreSQL

# Rules
- Type hints required
- Health checks required
- All endpoints need auth
EOF
```

### Run the MCP server
```bash
specmcp
```

### Configure your AI (Claude, Copilot, Cursor, etc)
```json
{
  "mcpServers": {
    "specmcp": {
      "command": "specmcp"
    }
  }
}
```

### Generate specs
```
You: "Generate a user management API spec"

AI: ✅ Generated specs/users-api.json
    - JWT auth: configured
    - Health endpoint: included
    - Type definitions: complete
    - Compliance: 100/100
```

**From zero to production-ready spec in 60 seconds.**

---

## Why This Matters

### Before SpecMCP
```
Developer A: Uses OAuth2, integers for IDs, custom error format
Developer B: Uses JWT, UUIDs, RFC 7807 errors
Developer C: Uses API keys, strings for IDs, no error standard

6 months later: $500K to standardize
```

### After SpecMCP
```
constitution.md: "Use JWT, UUIDs, RFC 7807"

Every generated spec:
✅ Uses JWT
✅ Uses UUIDs
✅ Uses RFC 7807

Drift: Impossible
Cost: $0
```

---

## The Four Tools

SpecMCP provides four MCP tools your AI assistant can use:

### `parse_constitution`
Read constitution.md and extract rules.
```python
{
  "tech_stack": {"language": "Python", "auth": "JWT"},
  "patterns": {"api_style": "REST"},
  "principles": ["Type hints required"]
}
```

### `generate_openapi_spec`
Generate OpenAPI 3.1 specs that follow your rules.
```python
# AI calls this with your requirements
# Returns valid spec with all rules applied
# JWT configured, health endpoint included, etc.
```

### `verify_spec_compliance`
Check if a spec follows your rules.
```python
{
  "compliance_score": 85,
  "violations": [
    "Missing health endpoint",
    "Using integers instead of UUIDs"
  ]
}
```

### `save_spec_to_file`
Save generated specs to files.
```python
# Writes to specs/ directory
# Creates parent dirs
# Ready for git commit
```

---

## Real Examples

### Solo Developer
```bash
# Write rules once
echo "Auth: JWT" > .specify/constitution.md

# Generate 10 APIs
# All use JWT automatically
# Zero manual configuration

# Ship faster
```

### 10-Person Team
```bash
# Tech lead writes constitution.md
# Defines: Python, FastAPI, PostgreSQL, JWT

# Everyone's AI reads it
# Everyone generates compliant specs
# No code review arguments
# Perfect consistency
```

### Enterprise (100+ APIs)
```yaml
# .github/workflows/verify.yml
- name: Verify specs
  run: |
    pip install specmcp
    specmcp verify specs/*.json

# Result:
# - 100 APIs
# - 1 constitution
# - Automated enforcement
# - Zero drift
```

---

## Architecture
```
AI Assistant (Claude, Copilot, etc)
           ↓
    MCP Protocol
           ↓
    SpecMCP Server
           ↓
   constitution.md
```

Simple. No magic. Just tools.

---

## How It Works

### The Markdown Convention

SpecMCP uses the `.specify/` directory convention for storing rules in markdown. This is simple, readable, and version-controllable.
```
.specify/
├── constitution.md    # Your project rules
├── agents.md          # AI agent definitions (optional)
└── tasks.md           # Workflow definitions (optional)
```

GitHub's SpecKit project popularized this convention. We think it's a good pattern, so we use it. But there's no dependency - SpecMCP just reads markdown files.

### The MCP Layer

MCP (Model Context Protocol) is how AI assistants discover and use tools. SpecMCP implements MCP, which means:

- Works with Claude Desktop
- Works with GitHub Copilot
- Works with Cursor
- Works with any MCP-compatible AI

Your AI assistant sees four tools. It can call them. That's the whole integration.

### The Enforcement

Constitution rules are checked programmatically:
```python
def verify_spec(spec, constitution):
    if constitution.requires_jwt and not spec.has_jwt:
        return violation("Missing JWT")
    if constitution.requires_health and not spec.has_health:
        return violation("Missing health endpoint")
    # ... more checks
    return compliance_score
```

No magic. Just code checking JSON against rules.

---

## Roadmap

**v0.1 (Now):** Constitution parsing, OpenAPI generation, compliance verification

**v0.2 (Q1 2026):** AsyncAPI support, task execution, agents.md parsing

**v0.3 (Q2 2026):** gRPC/Protobuf, GraphQL, spec versioning

**v1.0 (Q2 2026):** Stable API, production-ready

We ship fast. We listen to users. We break things in minor versions until 1.0.

---

## Philosophy

**Specs should be generated, not written.**

Writing JSON by hand is tedious. Computers should do it.

**Rules should be enforced, not suggested.**

A style guide nobody reads doesn't prevent drift. CI/CD that fails the build does.

**Markdown over GUIs.**

Plain text files in git beat proprietary formats in databases.

**Tools over frameworks.**

Four simple tools beat 1000-page documentation.

---

## Contributing

SpecMCP is MIT licensed. Fork it. Change it. Ship it.
```bash
git clone https://github.com/specmcp/core
cd core
./setup.sh
python test_specmcp.py
```

PRs welcome. No CLA. No corporate nonsense.

---

## Community

- **GitHub:** [github.com/specmcp/core](https://github.com/specmcp/core)
- **Discord:** [discord.gg/specmcp](https://discord.gg/specmcp)
- **Email:** [kevin@specmcp.ai](mailto:kevin@specmcp.ai)

---

## FAQ

**Why not just use Swagger/Redoc/etc?**  
Those are for viewing specs. We're for generating and enforcing them.

**Do I need to use SpecKit?**  
No. SpecMCP just reads `.specify/constitution.md`. Call it whatever you want.

**Does this replace writing code?**  
No. This generates specifications. You still write implementations.

**What about breaking changes?**  
Update constitution.md, regenerate specs, git shows you the diff.

**Is this production-ready?**  
Yes. We use semantic versioning. v0.x = features may change. v1.0 = stable.

**License?**  
MIT. Free forever.

---

## Credits

Built on [FastMCP](https://gofastmcp.com) by Prefect.

Inspired by [SpecKit](https://github.com/github/spec-kit) by GitHub.

Part of the [MCP ecosystem](https://modelcontextprotocol.io) by Anthropic.

---

## Author

**Kevin Ryan** - [kevin@specmcp.ai](mailto:kevin@specmcp.ai)

20+ years building systems. CERN, Financial Times, NatWest, McKinsey. Currently Interim Head of DevOps EMEA at Cprime.

Author of "AI Immigrants" - [sddbook.com](https://sddbook.com)

---

<div align="center">

**SpecMCP: Spec-Driven Development that actually works**

[⭐ Star on GitHub](https://github.com/specmcp/core) • [📖 Docs](https://specmcp.ai/docs) • [💬 Discord](https://discord.gg/specmcp)

*From rules to enforcement. No drift. No manual work.*

</div>
