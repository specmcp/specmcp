# interactive_client.py

from fastmcp import Client
import asyncio
import json
import specmcp_server

async def interactive_shell():
    """Interactive shell for SpecMCP"""
    
    async with Client(specmcp_server.mcp) as client:
        print("🚀 SpecMCP Interactive Shell")
        print("=" * 60)
        print("Available commands:")
        print("  1. Parse constitution")
        print("  2. Generate spec")
        print("  3. Verify spec")
        print("  4. Save spec")
        print("  q. Quit")
        print("=" * 60)
        
        while True:
            print()
            choice = input("Choose command (1-4, q): ").strip()
            
            if choice == 'q':
                break
                
            elif choice == '1':
                path = input("Constitution path [.specify/constitution.md]: ").strip() or ".specify/constitution.md"
                result = await client.call_tool("parse_constitution", {"path": path})
                if hasattr(result, 'data'):
                    data = json.loads(result.data) if isinstance(result.data, str) else result.data
                    print(json.dumps(data, indent=2))
                    
            elif choice == '2':
                requirements = input("Describe the API: ").strip()
                if not requirements:
                    print("❌ Requirements cannot be empty")
                    continue
                    
                title = input("API title [Generated API]: ").strip() or "Generated API"
                const_path = input("Constitution path [.specify/constitution.md]: ").strip() or ".specify/constitution.md"
                
                result = await client.call_tool(
                    "generate_openapi_spec",
                    {
                        "requirements": requirements,
                        "title": title,
                        "constitution_path": const_path
                    }
                )
                
                if hasattr(result, 'data'):
                    data = json.loads(result.data) if isinstance(result.data, str) else result.data
                    if data.get('success'):
                        print("✅ Spec generated successfully!")
                        
                        # Ask if they want to save
                        save = input("Save to file? (y/n): ").strip().lower()
                        if save == 'y':
                            output = input("Output path [specs/api.json]: ").strip() or "specs/api.json"
                            spec_json = json.dumps(data['specification'])
                            
                            save_result = await client.call_tool(
                                "save_spec_to_file",
                                {
                                    "spec_content": spec_json,
                                    "output_path": output,
                                    "format": "json"
                                }
                            )
                            
                            if hasattr(save_result, 'data'):
                                save_data = json.loads(save_result.data) if isinstance(save_result.data, str) else save_result.data
                                if save_data.get('success'):
                                    print(f"✅ {save_data['message']}")
                    else:
                        print(f"❌ {data.get('error', 'Unknown error')}")
                        
            elif choice == '3':
                spec_file = input("Spec file to verify: ").strip()
                if not spec_file:
                    print("❌ File path required")
                    continue
                    
                try:
                    from pathlib import Path
                    spec_content = Path(spec_file).read_text()
                    const_path = input("Constitution path [.specify/constitution.md]: ").strip() or ".specify/constitution.md"
                    
                    result = await client.call_tool(
                        "verify_spec_compliance",
                        {
                            "spec_content": spec_content,
                            "constitution_path": const_path
                        }
                    )
                    
                    if hasattr(result, 'data'):
                        data = json.loads(result.data) if isinstance(result.data, str) else result.data
                        print(f"\n{data['summary']}")
                        print(f"Score: {data['compliance_score']}/100")
                        if data.get('violations'):
                            print("\nViolations:")
                            for v in data['violations']:
                                print(f"  [{v['severity'].upper()}] {v['message']}")
                        
                except FileNotFoundError:
                    print(f"❌ File not found: {spec_file}")
                except Exception as e:
                    print(f"❌ Error: {e}")
                    
            elif choice == '4':
                spec_file = input("Spec file to save from: ").strip()
                output = input("Output path: ").strip()
                
                if not spec_file or not output:
                    print("❌ Both paths required")
                    continue
                    
                try:
                    from pathlib import Path
                    spec_content = Path(spec_file).read_text()
                    
                    result = await client.call_tool(
                        "save_spec_to_file",
                        {
                            "spec_content": spec_content,
                            "output_path": output,
                            "format": "json"
                        }
                    )
                    
                    if hasattr(result, 'data'):
                        data = json.loads(result.data) if isinstance(result.data, str) else result.data
                        if data.get('success'):
                            print(f"✅ {data['message']}")
                        else:
                            print(f"❌ {data.get('error', 'Unknown error')}")
                            
                except Exception as e:
                    print(f"❌ Error: {e}")
                    
            else:
                print("❌ Invalid choice")
        
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    asyncio.run(interactive_shell())