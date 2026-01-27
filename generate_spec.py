#!/usr/bin/env python3
"""
Generate OpenAPI spec for Authentication API using SpecMCP tools
"""

import json
from pathlib import Path

# Import the SpecMCP server functions directly
from specmcp_server import (
    parse_constitution,
    generate_openapi_spec,
    verify_spec_compliance,
    save_spec_to_file
)

def main():
    print("🚀 Generating OpenAPI Specification with SpecMCP")
    print("=" * 70)
    
    # Step 1: Parse Constitution
    print("\n📋 Step 1: Parsing constitution...")
    constitution_result = parse_constitution(".specify/constitution.md")
    
    if not constitution_result.get("success"):
        print(f"❌ Error parsing constitution: {constitution_result.get('error')}")
        return
    
    print("✅ Constitution parsed successfully")
    print(f"   Summary: {constitution_result['summary']}")
    
    # Step 2: Generate OpenAPI Spec
    print("\n📝 Step 2: Generating OpenAPI 3.1 specification...")
    
    requirements = """User authentication API with registration, login, logout, profile management, and password reset. 
    Include all CRUD operations for user management.
    
    Endpoints:
    - POST /auth/register - Register new user with email and password
    - POST /auth/login - Login and get JWT token
    - POST /auth/logout - Logout (requires authentication)
    - GET /auth/me - Get current user profile (requires authentication)
    - POST /auth/forgot-password - Request password reset with email
    - POST /auth/reset-password - Reset password with token
    - GET /health - Health check endpoint (no auth required)"""
    
    spec_result = generate_openapi_spec(
        requirements=requirements,
        constitution_path=".specify/constitution.md",
        title="Authentication API"
    )
    
    if not spec_result.get("success"):
        print(f"❌ Error generating spec: {spec_result.get('error')}")
        return
    
    print("✅ OpenAPI specification generated successfully")
    
    # Get the generated spec and enhance it with detailed schemas
    spec = spec_result["specification"]
    
    # Add detailed schemas and endpoints
    print("\n📐 Step 2b: Enhancing specification with schemas...")
    
    # Add request/response schemas
    spec["components"]["schemas"] = {
        "User": {
            "type": "object",
            "required": ["id", "email", "username", "created_at"],
            "properties": {
                "id": {"type": "string", "format": "uuid", "description": "User unique identifier"},
                "email": {"type": "string", "format": "email", "description": "User email address"},
                "username": {"type": "string", "description": "User username"},
                "first_name": {"type": "string", "description": "User first name"},
                "last_name": {"type": "string", "description": "User last name"},
                "created_at": {"type": "string", "format": "date-time", "description": "Account creation timestamp"},
                "updated_at": {"type": "string", "format": "date-time", "description": "Last update timestamp"}
            }
        },
        "RegisterRequest": {
            "type": "object",
            "required": ["email", "password", "username"],
            "properties": {
                "email": {"type": "string", "format": "email", "description": "Email address"},
                "password": {"type": "string", "minLength": 8, "description": "Password (min 8 characters)"},
                "username": {"type": "string", "minLength": 3, "description": "Username"},
                "first_name": {"type": "string", "description": "First name (optional)"},
                "last_name": {"type": "string", "description": "Last name (optional)"}
            }
        },
        "LoginRequest": {
            "type": "object",
            "required": ["email", "password"],
            "properties": {
                "email": {"type": "string", "format": "email", "description": "Email address"},
                "password": {"type": "string", "description": "Password"}
            }
        },
        "LoginResponse": {
            "type": "object",
            "required": ["access_token", "token_type", "user"],
            "properties": {
                "access_token": {"type": "string", "description": "JWT access token"},
                "token_type": {"type": "string", "enum": ["bearer"], "description": "Token type"},
                "user": {"$ref": "#/components/schemas/User"}
            }
        },
        "ForgotPasswordRequest": {
            "type": "object",
            "required": ["email"],
            "properties": {
                "email": {"type": "string", "format": "email", "description": "Email address"}
            }
        },
        "ResetPasswordRequest": {
            "type": "object",
            "required": ["token", "new_password"],
            "properties": {
                "token": {"type": "string", "description": "Password reset token"},
                "new_password": {"type": "string", "minLength": 8, "description": "New password (min 8 characters)"}
            }
        },
        "HealthResponse": {
            "type": "object",
            "required": ["status"],
            "properties": {
                "status": {"type": "string", "enum": ["ok", "healthy"], "description": "Service status"}
            }
        },
        "Error": {
            "type": "object",
            "required": ["error", "message"],
            "properties": {
                "error": {"type": "string", "description": "Error code"},
                "message": {"type": "string", "description": "Error message"},
                "details": {"type": "object", "description": "Additional error details (optional)"}
            }
        }
    }
    
    # Add detailed endpoints
    spec["paths"]["/auth/register"] = {
        "post": {
            "summary": "Register a new user",
            "description": "Create a new user account with email and password",
            "tags": ["Authentication"],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/RegisterRequest"}
                    }
                }
            },
            "responses": {
                "201": {
                    "description": "User registered successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/User"}
                        }
                    }
                },
                "400": {
                    "description": "Invalid request (missing fields, weak password, etc.)",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Error"}
                        }
                    }
                },
                "409": {
                    "description": "Email or username already exists",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Error"}
                        }
                    }
                }
            }
        }
    }
    
    spec["paths"]["/auth/login"] = {
        "post": {
            "summary": "Login user",
            "description": "Authenticate user and get JWT token",
            "tags": ["Authentication"],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/LoginRequest"}
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "Login successful",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/LoginResponse"}
                        }
                    }
                },
                "401": {
                    "description": "Invalid credentials",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Error"}
                        }
                    }
                }
            }
        }
    }
    
    spec["paths"]["/auth/logout"] = {
        "post": {
            "summary": "Logout user",
            "description": "Invalidate user session (requires authentication)",
            "tags": ["Authentication"],
            "security": [{"bearerAuth": []}],
            "responses": {
                "204": {
                    "description": "Logout successful"
                },
                "401": {
                    "description": "Unauthorized",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Error"}
                        }
                    }
                }
            }
        }
    }
    
    spec["paths"]["/auth/me"] = {
        "get": {
            "summary": "Get current user profile",
            "description": "Retrieve the authenticated user's profile information",
            "tags": ["Authentication"],
            "security": [{"bearerAuth": []}],
            "responses": {
                "200": {
                    "description": "User profile retrieved successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/User"}
                        }
                    }
                },
                "401": {
                    "description": "Unauthorized - missing or invalid token",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Error"}
                        }
                    }
                }
            }
        }
    }
    
    spec["paths"]["/auth/forgot-password"] = {
        "post": {
            "summary": "Request password reset",
            "description": "Send a password reset token to user's email",
            "tags": ["Authentication"],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/ForgotPasswordRequest"}
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "Password reset email sent",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "Password reset instructions sent to email"
                                    }
                                }
                            }
                        }
                    }
                },
                "404": {
                    "description": "User not found",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Error"}
                        }
                    }
                }
            }
        }
    }
    
    spec["paths"]["/auth/reset-password"] = {
        "post": {
            "summary": "Reset password",
            "description": "Reset user password using reset token",
            "tags": ["Authentication"],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/ResetPasswordRequest"}
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "Password reset successful",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "Password has been reset successfully"
                                    }
                                }
                            }
                        }
                    }
                },
                "400": {
                    "description": "Invalid or expired token",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Error"}
                        }
                    }
                }
            }
        }
    }
    
    # Health endpoint already exists, but let's ensure it's not requiring auth
    spec["paths"]["/health"]["get"]["security"] = []
    
    print("✅ Specification enhanced with detailed schemas")
    
    # Step 3: Save Spec to File
    print("\n💾 Step 3: Saving specification to file...")
    
    spec_json = json.dumps(spec)
    save_result = save_spec_to_file(
        spec_content=spec_json,
        output_path="specs/auth-complete.json",
        format="json"
    )
    
    if not save_result.get("success"):
        print(f"❌ Error saving spec: {save_result.get('error')}")
        return
    
    print(f"✅ {save_result['message']}")
    print(f"   File: {save_result['file_path']}")
    
    # Step 4: Verify Compliance
    print("\n✔️  Step 4: Verifying compliance with constitution...")
    
    compliance_result = verify_spec_compliance(
        spec_content=spec_json,
        constitution_path=".specify/constitution.md"
    )
    
    print(f"   Compliance Score: {compliance_result['compliance_score']}/100")
    print(f"   Status: {compliance_result['summary']}")
    
    if compliance_result.get("violations"):
        print("\n   Violations found:")
        for violation in compliance_result["violations"]:
            print(f"   - [{violation['severity'].upper()}] {violation['message']}")
            print(f"     Suggestion: {violation['suggestion']}")
    else:
        print("   ✅ No violations found!")
    
    if compliance_result.get("recommendations"):
        print("\n   Recommendations:")
        for rec in compliance_result["recommendations"]:
            print(f"   - {rec}")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 GENERATION SUMMARY")
    print("=" * 70)
    print(f"✅ OpenAPI specification generated successfully!")
    print(f"✅ File saved: specs/auth-complete.json")
    print(f"✅ Compliance score: {compliance_result['compliance_score']}/100")
    print(f"✅ Constitution requirements: {'✅ PASSED' if compliance_result['compliance_score'] >= 80 else '⚠️ NEEDS REVIEW'}")
    print("\n📋 Included Endpoints:")
    print("   - POST /auth/register")
    print("   - POST /auth/login")
    print("   - POST /auth/logout (requires auth)")
    print("   - GET /auth/me (requires auth)")
    print("   - POST /auth/forgot-password")
    print("   - POST /auth/reset-password")
    print("   - GET /health (no auth required)")
    print("\n🔐 Security Configuration:")
    print("   - JWT Bearer authentication enabled")
    print("   - Protected endpoints require bearerAuth")
    print("\n📚 Specification Format:")
    print("   - OpenAPI 3.1.0")
    print("   - Detailed request/response schemas")
    print("   - Error responses (400, 401, 404, 409, 500)")
    print("=" * 70)

if __name__ == "__main__":
    main()
