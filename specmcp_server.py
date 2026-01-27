# specmcp_server.py

from fastmcp import FastMCP
from pathlib import Path
from typing import Optional
import json
import re

mcp = FastMCP("SpecMCP - Spec-Driven Development Tools")

# ============================================================================
# HELPER FUNCTIONS (Not MCP tools - just regular Python functions)
# ============================================================================

def _parse_constitution_internal(path: str) -> dict:
    """Internal helper to parse constitution (not an MCP tool)"""
    constitution_path = Path(path)
    
    if not constitution_path.exists():
        return {
            "success": False,
            "error": f"Constitution file not found: {path}",
            "suggestion": "Make sure you're in a SpecKit project directory with .specify/constitution.md"
        }
    
    try:
        content = constitution_path.read_text()
        
        tech_stack = extract_tech_stack(content)
        patterns = extract_patterns(content)
        principles = extract_principles(content)
        standards = extract_standards(content)
        
        return {
            "success": True,
            "constitution": {
                "tech_stack": tech_stack,
                "patterns": patterns,
                "principles": principles,
                "standards": standards
            },
            "metadata": {
                "file_path": str(constitution_path.absolute()),
                "file_size": len(content),
                "lines": len(content.split('\n'))
            },
            "summary": generate_constitution_summary(tech_stack, patterns, principles)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "suggestion": "Check if the file is readable and properly formatted"
        }

def extract_tech_stack(content: str) -> dict:
    """Extract technology stack from constitution"""
    tech_stack = {}
    content_lower = content.lower()
    
    # Languages
    if "python" in content_lower:
        tech_stack["language"] = "Python"
    elif "typescript" in content_lower or "javascript" in content_lower:
        tech_stack["language"] = "TypeScript/JavaScript"
    elif "java" in content_lower:
        tech_stack["language"] = "Java"
    elif "go" in content_lower:
        tech_stack["language"] = "Go"
    
    # Frameworks
    if "fastapi" in content_lower:
        tech_stack["framework"] = "FastAPI"
    elif "django" in content_lower:
        tech_stack["framework"] = "Django"
    elif "express" in content_lower:
        tech_stack["framework"] = "Express"
    elif "spring" in content_lower:
        tech_stack["framework"] = "Spring"
    
    # Databases
    if "postgresql" in content_lower or "postgres" in content_lower:
        tech_stack["database"] = "PostgreSQL"
    elif "mongodb" in content_lower:
        tech_stack["database"] = "MongoDB"
    elif "mysql" in content_lower:
        tech_stack["database"] = "MySQL"
    
    # Deployment
    if "docker" in content_lower:
        tech_stack["deployment"] = "Docker"
    if "kubernetes" in content_lower:
        tech_stack["deployment"] = "Kubernetes"
    
    return tech_stack

def extract_patterns(content: str) -> dict:
    """Extract architectural patterns"""
    patterns = {}
    content_lower = content.lower()
    
    # Architecture
    if "microservices" in content_lower:
        patterns["architecture"] = "Microservices"
    elif "monolith" in content_lower:
        patterns["architecture"] = "Monolithic"
    
    # API Style
    if "rest" in content_lower or "restful" in content_lower:
        patterns["api_style"] = "REST"
    elif "graphql" in content_lower:
        patterns["api_style"] = "GraphQL"
    elif "grpc" in content_lower:
        patterns["api_style"] = "gRPC"
    
    # Auth
    if "jwt" in content_lower:
        patterns["auth"] = "JWT"
    elif "oauth" in content_lower:
        patterns["auth"] = "OAuth2"
    
    return patterns

def extract_principles(content: str) -> list:
    """Extract key principles from constitution"""
    principles = []
    
    # Look for bullet points or numbered lists
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        # Match lines starting with -, *, or numbers
        if re.match(r'^[-*•]\s+', line) or re.match(r'^\d+\.\s+', line):
            principle = re.sub(r'^[-*•\d.]\s+', '', line)
            if len(principle) > 10:  # Filter out too short
                principles.append(principle)
    
    return principles[:10]  # Return top 10

def extract_standards(content: str) -> dict:
    """Extract coding standards"""
    standards = {}
    content_lower = content.lower()
    
    if "test" in content_lower and "coverage" in content_lower:
        standards["testing"] = "Required"
    
    if "type hint" in content_lower or "typing" in content_lower:
        standards["type_hints"] = "Required"
    
    if "documentation" in content_lower or "docstring" in content_lower:
        standards["documentation"] = "Required"
    
    return standards

def generate_constitution_summary(tech_stack: dict, patterns: dict, principles: list) -> str:
    """Generate human-readable summary"""
    parts = []
    
    if tech_stack.get("language"):
        parts.append(f"Language: {tech_stack['language']}")
    if tech_stack.get("framework"):
        parts.append(f"Framework: {tech_stack['framework']}")
    if patterns.get("architecture"):
        parts.append(f"Architecture: {patterns['architecture']}")
    if patterns.get("api_style"):
        parts.append(f"API: {patterns['api_style']}")
    
    summary = " | ".join(parts) if parts else "No clear tech stack found"
    summary += f" | {len(principles)} principles defined"
    
    return summary

# ============================================================================
# MCP TOOLS (These are exposed to AI assistants)
# ============================================================================

@mcp.tool()
def parse_constitution(path: str = ".specify/constitution.md") -> dict:
    """
    Parse a SpecKit constitution.md file and extract structured information
    
    Args:
        path: Path to constitution.md file (default: .specify/constitution.md)
        
    Returns:
        Structured constitution data including tech stack, patterns, and principles
    """
    # Call internal helper function
    return _parse_constitution_internal(path)

@mcp.tool()
def generate_openapi_spec(
    requirements: str,
    constitution_path: Optional[str] = None,
    title: Optional[str] = None
) -> dict:
    """
    Generate an OpenAPI 3.1 specification from natural language requirements
    
    Args:
        requirements: Natural language description of what to build
        constitution_path: Optional path to constitution.md to follow constraints
        title: Optional API title (auto-generated if not provided)
        
    Returns:
        OpenAPI 3.1 specification
    """
    # Parse constitution if provided (use internal helper)
    constitution = None
    if constitution_path:
        result = _parse_constitution_internal(constitution_path)
        if result.get("success"):
            constitution = result["constitution"]
    
    # Generate spec
    spec = {
        "openapi": "3.1.0",
        "info": {
            "title": title or "Generated API",
            "version": "1.0.0",
            "description": requirements
        },
        "servers": [
            {"url": "https://api.example.com", "description": "Production server"}
        ],
        "paths": {},
        "components": {
            "schemas": {},
            "securitySchemes": {}
        }
    }
    
    # Add authentication based on constitution
    if constitution and constitution.get("patterns", {}).get("auth"):
        auth_type = constitution["patterns"]["auth"]
        if auth_type == "JWT":
            spec["components"]["securitySchemes"]["bearerAuth"] = {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
            spec["security"] = [{"bearerAuth": []}]
        elif auth_type == "OAuth2":
            spec["components"]["securitySchemes"]["oauth2"] = {
                "type": "oauth2",
                "flows": {
                    "authorizationCode": {
                        "authorizationUrl": "https://example.com/oauth/authorize",
                        "tokenUrl": "https://example.com/oauth/token",
                        "scopes": {}
                    }
                }
            }
    
    # Add basic health endpoint
    spec["paths"]["/health"] = {
        "get": {
            "summary": "Health check endpoint",
            "responses": {
                "200": {
                    "description": "Service is healthy",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "status": {"type": "string", "example": "ok"}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    return {
        "success": True,
        "specification": spec,
        "format": "openapi-3.1",
        "constitution_applied": constitution is not None,
        "notes": [
            "Basic OpenAPI 3.1 specification generated",
            "Add more endpoints based on your requirements",
            "Authentication configured" if constitution else "No authentication configured"
        ]
    }

@mcp.tool()
def verify_spec_compliance(
    spec_content: str,
    constitution_path: str = ".specify/constitution.md"
) -> dict:
    """
    Verify that a specification follows constitution rules
    
    Args:
        spec_content: The specification content (JSON)
        constitution_path: Path to constitution.md
        
    Returns:
        Compliance report with violations and score
    """
    # Parse constitution using internal helper (NOT the MCP tool)
    constitution_result = _parse_constitution_internal(constitution_path)
    
    if not constitution_result.get("success"):
        return {
            "success": False,
            "error": "Could not parse constitution",
            "details": constitution_result.get("error")
        }
    
    constitution = constitution_result["constitution"]
    violations = []
    
    # Try to parse spec as JSON
    try:
        spec = json.loads(spec_content)
    except:
        return {
            "success": False,
            "error": "Spec content is not valid JSON",
            "suggestion": "Make sure you're providing valid OpenAPI JSON"
        }
    
    # Check tech stack compliance
    tech_stack = constitution.get("tech_stack", {})
    spec_str = spec_content.lower()
    
    if tech_stack.get("framework"):
        framework = tech_stack["framework"].lower()
        if framework not in spec_str:
            violations.append({
                "rule": "Tech Stack Compliance",
                "severity": "warning",
                "message": f"Constitution requires {tech_stack['framework']}, not found in spec",
                "suggestion": f"Add {tech_stack['framework']} references to spec description"
            })
    
    # Check authentication
    patterns = constitution.get("patterns", {})
    if patterns.get("auth"):
        required_auth = patterns["auth"]
        has_security = "securitySchemes" in spec.get("components", {})
        
        if not has_security:
            violations.append({
                "rule": "Authentication Required",
                "severity": "error",
                "message": f"Constitution requires {required_auth} authentication",
                "suggestion": f"Add {required_auth} security scheme to components.securitySchemes"
            })
    
    # Check for health endpoint
    has_health = "/health" in spec.get("paths", {})
    if not has_health:
        violations.append({
            "rule": "Health Endpoint Required",
            "severity": "warning",
            "message": "All services should have a /health endpoint",
            "suggestion": "Add GET /health endpoint for monitoring"
        })
    
    # Calculate compliance score
    max_score = 100
    deductions = sum(20 if v["severity"] == "error" else 10 for v in violations)
    score = max(0, max_score - deductions)
    
    return {
        "success": True,
        "is_compliant": len(violations) == 0,
        "compliance_score": score,
        "violations": violations,
        "summary": f"{'✅ Fully compliant' if len(violations) == 0 else f'⚠️  {len(violations)} violation(s) found'}",
        "recommendations": [v["suggestion"] for v in violations] if violations else ["Specification follows all constitution rules"]
    }

@mcp.tool()
def save_spec_to_file(
    spec_content: str,
    output_path: str,
    format: str = "json"
) -> dict:
    """
    Save a specification to a file
    
    Args:
        spec_content: The specification content (JSON or YAML)
        output_path: Where to save the file (e.g., "specs/api.json")
        format: Output format - "json" or "yaml" (default: json)
        
    Returns:
        Success status and file location
    """
    try:
        output_file = Path(output_path)
        
        # Create parent directories if needed
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Parse spec
        try:
            spec = json.loads(spec_content)
        except:
            return {
                "success": False,
                "error": "Invalid JSON content",
                "suggestion": "Make sure spec_content is valid JSON"
            }
        
        # Write file
        if format == "json":
            output_file.write_text(json.dumps(spec, indent=2))
        elif format == "yaml":
            try:
                import yaml
                output_file.write_text(yaml.dump(spec, default_flow_style=False, sort_keys=False))
            except ImportError:
                return {
                    "success": False,
                    "error": "PyYAML not installed",
                    "suggestion": "Install with: pip install pyyaml"
                }
        else:
            return {
                "success": False,
                "error": f"Unsupported format: {format}",
                "suggestion": "Use 'json' or 'yaml'"
            }
        
        return {
            "success": True,
            "file_path": str(output_file.absolute()),
            "file_size": output_file.stat().st_size,
            "format": format,
            "message": f"✅ Spec saved to {output_path}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "suggestion": "Check file path and permissions"
        }

# ============================================================================
# Run Server
# ============================================================================

if __name__ == "__main__":
    mcp.run()