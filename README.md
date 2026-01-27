# SpecMCP - AI Tools for Building Better APIs

SpecMCP helps you build APIs the right way by keeping your specifications and code in sync.

## What Does This Do?

Imagine you're building an API (like a website backend). Usually:
- ❌ You write code first, document it later (or never)
- ❌ Your documentation gets out of date
- ❌ Other developers don't know what changed
- ❌ Things break and nobody knows why

**SpecMCP fixes this by:**
- ✅ Starting with a "constitution" - your project's rules
- ✅ Generating API specs that follow those rules
- ✅ Checking that everything stays consistent
- ✅ Saving specs as files you can share

## Quick Example

**1. You create rules for your project** (a "constitution"):
```
We use Python and FastAPI
All APIs need JWT authentication
Every service needs a /health endpoint
```

**2. SpecMCP reads those rules:**
```bash
parse_constitution → Understands your tech stack
```

**3. Generate an API spec:**
```bash
generate_openapi_spec → Creates a complete API specification
```

**4. Check if a spec follows the rules:**
```bash
verify_spec_compliance → Scores your spec (0-100)
```

**5. Save it to a file:**
```bash
save_spec_to_file → Saves as JSON or YAML
```

## Installation (5 Minutes)

### What You Need
- Python 3.11+ ([Download here](https://www.python.org/downloads/))
- That's it!

### Setup Steps

**Option 1: Automatic (Easy)**
```bash
# Download this project
# Open terminal in the project folder
# Run:
./setup.sh
```

**Option 2: Manual (Step by Step)**
```bash
# 1. Create a "virtual environment" (isolated Python)
python3 -m venv venv

# 2. Turn it on
source venv/bin/activate
# You'll see (venv) in your terminal

# 3. Install the tool we need
pip install fastmcp

# 4. Test it works
python test_specmcp.py
```

If you see `✅ SpecMCP Server Tests Complete!` - **you're done!** 🎉

## How to Use It

### Basic Test
```bash
# Make sure (venv) is showing in your terminal
# If not, run: source venv/bin/activate

# Run the test
python test_specmcp.py
```

This will:
1. Read the example constitution in `.specify/constitution.md`
2. Generate an API spec
3. Check if it's valid
4. Save it to `specs/auth-api.json`

### Use with Claude Desktop

**What's Claude Desktop?** It's like ChatGPT but can use tools. SpecMCP is a tool!

**Setup (3 minutes):**

1. Open this file (create if it doesn't exist):
   - **Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add this (replace `/path/to/` with your actual path):
```json
{
  "mcpServers": {
    "specmcp": {
      "command": "python",
      "args": ["/path/to/specmcp/specmcp_server.py"]
    }
  }
}
```

3. Restart Claude Desktop completely

4. Start a new chat and look for the 🔨 icon

**Now you can ask Claude:**
```
"Read my constitution from .specify/constitution.md 
and tell me what tech stack I'm using"

"Generate an OpenAPI spec for a user authentication API 
that follows my constitution"

"Check if this spec follows my constitution rules"
```

## Understanding the Files
```
specmcp/
├── README.md               ← You are here
├── setup.sh                ← Run this to install everything
├── specmcp_server.py       ← The main program (4 tools)
├── test_specmcp.py         ← Tests to make sure it works
├── .specify/               
│   └── constitution.md     ← Your project rules (example included)
└── specs/                  
    └── auth-api.json       ← Generated API spec (example)
```

## The 4 Tools Explained

### 1. parse_constitution
**What it does:** Reads your project rules and extracts the important parts

**Example constitution:**
```markdown
## Tech Stack
- Language: Python
- Framework: FastAPI
- Authentication: JWT
```

**What it extracts:**
- Language: Python ✓
- Framework: FastAPI ✓
- Auth: JWT ✓

### 2. generate_openapi_spec
**What it does:** Creates an API specification from your description

**You say:** 
> "Build a user authentication API with login and registration"

**It creates:**
- POST /auth/register endpoint
- POST /auth/login endpoint
- JWT authentication configured
- Health check endpoint
- Follows your constitution rules

### 3. verify_spec_compliance
**What it does:** Checks if an API spec follows your rules

**Example:**
```
Constitution says: "Must use JWT authentication"
Your spec: Missing authentication

Score: 80/100 ⚠️
Problem: No JWT security scheme found
Fix: Add JWT to components.securitySchemes
```

### 4. save_spec_to_file
**What it does:** Saves your API spec to a file

**Why?** So you can:
- Share it with your team
- Put it in version control (Git)
- Use it with other tools
- Document your API

## Common Questions

### "What's a constitution?"
A simple text file with your project's rules. Example:
```markdown
# My Project Rules

## Tech Stack
- Use Python 3.11
- Use FastAPI framework
- Use PostgreSQL database

## Security Rules
- All APIs need JWT tokens
- Every endpoint needs authentication
```

### "What's an OpenAPI spec?"
A standard way to describe an API. It's like a blueprint. Tools can read it to:
- Generate documentation
- Create tests automatically
- Build client code
- Validate requests

### "Do I need to know Python?"
To **use** it: No! Just run the commands above.

To **modify** it: Basic Python helps but isn't required.

### "What if something breaks?"
```bash
# 1. Make sure you're in the right folder
pwd

# 2. Make sure virtual environment is on
source venv/bin/activate

# 3. Make sure FastMCP is installed
pip list | grep fastmcp

# 4. Try running tests
python test_specmcp.py

# Still stuck? Open an issue on GitHub!
```

## What's Next?

1. ✅ **You are here:** Got it installed and working
2. 📝 **Next:** Create your own constitution in `.specify/constitution.md`
3. 🚀 **Then:** Generate specs for your real projects
4. 🤝 **Finally:** Share with your team!

## Real World Example

**Before SpecMCP:**
```
You: "Hey, does our API use OAuth or JWT?"
Teammate: "Uh... check the code? Maybe the old docs?"
You: *Spends 2 hours digging through code*
```

**With SpecMCP:**
```
You: "Claude, what auth does our constitution specify?"
Claude: *reads constitution.md* "JWT authentication"
You: "Generate a spec for the new endpoints following that"
Claude: *generates spec with JWT already configured*
You: *Ships in 10 minutes*
```

## Need Help?

- 📧 Email: kevin@specmcp.ai
- 🐛 Found a bug? [Open an issue](https://github.com/specmcp/core/issues)
- 💬 Questions? [Start a discussion](https://github.com/specmcp/core/discussions)

## License

MIT - Use it however you want!

## Credits

Built by [Kevin Ryan](https://kevinryan.io)
- Author of "AI Immigrants"
- 20+ years building systems at CERN, Financial Times, NatWest
- Currently: Helping companies adopt AI responsibly

Made with [FastMCP](https://gofastmcp.com) 🚀


