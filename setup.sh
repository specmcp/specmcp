#!/bin/bash

echo "🚀 Setting up SpecMCP..."
echo ""

# 1. Create virtual environment
echo "1️⃣  Creating virtual environment..."
python3 -m venv venv

# 2. Activate it
echo "2️⃣  Activating virtual environment..."
source venv/bin/activate

# 3. Install FastMCP
echo "3️⃣  Installing FastMCP..."
pip install --quiet fastmcp

# 4. Verify installation
echo "4️⃣  Verifying installation..."
python -c "import fastmcp; print(f'   ✅ FastMCP {fastmcp.__version__} installed')"

# 5. Test it works
echo "5️⃣  Running tests..."
echo ""
python test_specmcp.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment in the future:"
echo "  source venv/bin/activate"
echo ""
echo "To run tests:"
echo "  python test_specmcp.py"
echo ""
echo "To use with Claude Desktop, add to config:"
echo "  $(pwd)/specmcp_server.py"