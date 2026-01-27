# test_specmcp.py - With save_spec_to_file test

from fastmcp import Client
import asyncio
import json
from pathlib import Path
import specmcp_server

def print_result(title, result):
    """Print result nicely"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print('='*70)
    if hasattr(result, 'data'):
        try:
            data = json.loads(result.data) if isinstance(result.data, str) else result.data
            print(json.dumps(data, indent=2))
        except:
            print(result.data)
    else:
        print(result)

async def test_specmcp():
    """Test SpecMCP tools"""
    
    async with Client(specmcp_server.mcp) as client:
        
        print("🎯 TESTING SPECMCP SERVER")
        
        # Test 1: Parse Constitution
        result = await client.call_tool(
            "parse_constitution",
            {"path": ".specify/constitution.md"}
        )
        print_result("1️⃣  Parse Constitution", result)
        
        # Test 2: Generate OpenAPI Spec (with constitution)
        result = await client.call_tool(
            "generate_openapi_spec",
            {
                "requirements": "User authentication API with email/password login and JWT tokens",
                "constitution_path": ".specify/constitution.md",
                "title": "Auth API"
            }
        )
        print_result("2️⃣  Generate OpenAPI Spec (with Constitution)", result)
        
        # Save the spec from test 2
        if hasattr(result, 'data'):
            data = json.loads(result.data) if isinstance(result.data, str) else result.data
            if data.get('success') and data.get('specification'):
                spec_json = json.dumps(data['specification'])
                
                # Test 4: Save spec to file
                result = await client.call_tool(
                    "save_spec_to_file",
                    {
                        "spec_content": spec_json,
                        "output_path": "specs/auth-api.json",
                        "format": "json"
                    }
                )
                print_result("4️⃣  Save Spec to File", result)
        
        # Test 3: Verify Spec Compliance
        spec = {
            "openapi": "3.1.0",
            "info": {"title": "Test", "version": "1.0.0"},
            "paths": {},
            "components": {"schemas": {}}
        }
        result = await client.call_tool(
            "verify_spec_compliance",
            {
                "spec_content": json.dumps(spec),
                "constitution_path": ".specify/constitution.md"
            }
        )
        print_result("3️⃣  Verify Spec Compliance (No Auth - Should Fail)", result)
        
        print(f"\n{'='*70}")
        print("✅ SpecMCP Server Tests Complete!")
        print('='*70)
        
        # Check if file was created
        spec_file = Path("specs/auth-api.json")
        if spec_file.exists():
            print(f"\n📄 Spec file created!")
            print(f"   Location: {spec_file.absolute()}")
            print(f"   Size: {spec_file.stat().st_size} bytes")
            print(f"\n   View it with:")
            print(f"   cat specs/auth-api.json")
            print(f"   code specs/auth-api.json")

if __name__ == "__main__":
    asyncio.run(test_specmcp())