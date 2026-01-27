#!/usr/bin/env python3
"""
Verify OpenAPI specification compliance with constitution
"""

import json
from pathlib import Path

def verify_compliance():
    """Verify the generated spec against constitution requirements"""
    
    print("✔️  Verifying OpenAPI Specification Compliance")
    print("=" * 70)
    
    # Load the specification
    spec_path = Path("specs/auth-complete.json")
    if not spec_path.exists():
        print(f"❌ Specification file not found: {spec_path}")
        return
    
    spec = json.loads(spec_path.read_text())
    
    # Load the constitution
    const_path = Path(".specify/constitution.md")
    if not const_path.exists():
        print(f"❌ Constitution file not found: {const_path}")
        return
    
    constitution = const_path.read_text()
    
    violations = []
    checks_passed = []
    
    # Check 1: OpenAPI 3.1.0 format
    if spec.get("openapi") == "3.1.0":
        checks_passed.append("✅ OpenAPI 3.1.0 format")
    else:
        violations.append({
            "rule": "OpenAPI Version",
            "severity": "error",
            "message": f"Expected OpenAPI 3.1.0, got {spec.get('openapi')}",
            "suggestion": "Update openapi field to 3.1.0"
        })
    
    # Check 2: JWT authentication configured
    security_schemes = spec.get("components", {}).get("securitySchemes", {})
    if "bearerAuth" in security_schemes:
        bearer = security_schemes["bearerAuth"]
        if bearer.get("scheme") == "bearer" and bearer.get("bearerFormat") == "JWT":
            checks_passed.append("✅ JWT Bearer authentication configured")
        else:
            violations.append({
                "rule": "JWT Configuration",
                "severity": "error",
                "message": "JWT Bearer authentication not properly configured",
                "suggestion": "Ensure bearerAuth has scheme='bearer' and bearerFormat='JWT'"
            })
    else:
        violations.append({
            "rule": "Authentication Required",
            "severity": "error",
            "message": "JWT authentication scheme not found",
            "suggestion": "Add bearerAuth to components.securitySchemes"
        })
    
    # Check 3: Health endpoint exists
    paths = spec.get("paths", {})
    if "/health" in paths:
        checks_passed.append("✅ Health endpoint present")
    else:
        violations.append({
            "rule": "Health Endpoint Required",
            "severity": "warning",
            "message": "Health endpoint not found",
            "suggestion": "Add GET /health endpoint"
        })
    
    # Check 4: All required authentication endpoints
    required_endpoints = [
        "/auth/register",
        "/auth/login",
        "/auth/logout",
        "/auth/me",
        "/auth/forgot-password",
        "/auth/reset-password"
    ]
    
    missing_endpoints = [ep for ep in required_endpoints if ep not in paths]
    if not missing_endpoints:
        checks_passed.append(f"✅ All {len(required_endpoints)} authentication endpoints present")
    else:
        violations.append({
            "rule": "Required Endpoints",
            "severity": "error",
            "message": f"Missing endpoints: {', '.join(missing_endpoints)}",
            "suggestion": f"Add missing endpoints: {', '.join(missing_endpoints)}"
        })
    
    # Check 5: Protected endpoints have security
    protected_endpoints = ["/auth/logout", "/auth/me"]
    unprotected = []
    for endpoint in protected_endpoints:
        if endpoint in paths:
            for method in paths[endpoint]:
                if method in ["get", "post", "put", "delete"]:
                    if "security" not in paths[endpoint][method]:
                        unprotected.append(f"{endpoint} {method.upper()}")
    
    if not unprotected:
        checks_passed.append("✅ Protected endpoints require authentication")
    else:
        violations.append({
            "rule": "Authentication Enforcement",
            "severity": "warning",
            "message": f"Endpoints not requiring auth: {', '.join(unprotected)}",
            "suggestion": "Add security requirement to protected endpoints"
        })
    
    # Check 6: Error responses defined
    has_error_schemas = "Error" in spec.get("components", {}).get("schemas", {})
    error_codes_found = set()
    for path_item in paths.values():
        for operation in path_item.values():
            if isinstance(operation, dict) and "responses" in operation:
                error_codes_found.update([
                    code for code in operation["responses"].keys()
                    if code in ["400", "401", "403", "404", "500"]
                ])
    
    if has_error_schemas and error_codes_found:
        checks_passed.append(f"✅ Error responses defined ({len(error_codes_found)} error types)")
    else:
        violations.append({
            "rule": "Error Handling",
            "severity": "warning",
            "message": "Incomplete error response definitions",
            "suggestion": "Add error response schemas and include HTTP error codes"
        })
    
    # Check 7: Request/Response schemas
    schemas = spec.get("components", {}).get("schemas", {})
    required_schemas = ["User", "RegisterRequest", "LoginRequest", "LoginResponse"]
    missing_schemas = [s for s in required_schemas if s not in schemas]
    
    if not missing_schemas:
        checks_passed.append(f"✅ Request/Response schemas defined ({len(schemas)} schemas total)")
    else:
        violations.append({
            "rule": "Schema Documentation",
            "severity": "warning",
            "message": f"Missing schemas: {', '.join(missing_schemas)}",
            "suggestion": f"Add missing schemas: {', '.join(missing_schemas)}"
        })
    
    # Check 8: API versioning (from constitution: API versioning required)
    title = spec.get("info", {}).get("title", "")
    if "api" in title.lower() or "v1" in str(spec):
        checks_passed.append("✅ API versioning considered")
    
    # Check 9: Type definitions in schemas
    if schemas:
        all_have_types = all(
            "type" in schema or "$ref" in schema or "properties" in schema
            for schema in schemas.values()
        )
        if all_have_types:
            checks_passed.append("✅ All schemas have type definitions")
    
    # Calculate compliance score
    max_score = 100
    deductions = sum(20 if v["severity"] == "error" else 10 for v in violations)
    score = max(0, max_score - deductions)
    
    # Print results
    print("\n📊 COMPLIANCE CHECK RESULTS")
    print("-" * 70)
    
    if checks_passed:
        print("\n✅ PASSED CHECKS:")
        for check in checks_passed:
            print(f"   {check}")
    
    if violations:
        print("\n⚠️  VIOLATIONS FOUND:")
        for i, violation in enumerate(violations, 1):
            print(f"\n   {i}. [{violation['severity'].upper()}] {violation['rule']}")
            print(f"      Message: {violation['message']}")
            print(f"      Suggestion: {violation['suggestion']}")
    else:
        print("\n✅ No violations found!")
    
    print("\n" + "=" * 70)
    print(f"COMPLIANCE SCORE: {score}/100")
    print("=" * 70)
    
    if score >= 90:
        print("🎉 Specification is production-ready!")
    elif score >= 80:
        print("✅ Specification is mostly compliant")
    else:
        print("⚠️  Specification needs review")
    
    print("\n📋 SPECIFICATION SUMMARY")
    print("-" * 70)
    print(f"OpenAPI Version: {spec.get('openapi')}")
    print(f"API Title: {spec.get('info', {}).get('title')}")
    print(f"API Version: {spec.get('info', {}).get('version')}")
    print(f"Total Endpoints: {len(paths)}")
    print(f"Total Schemas: {len(schemas)}")
    print(f"Security Schemes: {len(security_schemes)}")
    
    print("\n📌 ENDPOINTS")
    print("-" * 70)
    for endpoint in sorted(paths.keys()):
        methods = ", ".join([m.upper() for m in paths[endpoint].keys() if m in ["get", "post", "put", "delete", "patch"]])
        print(f"   {endpoint:<30} {methods}")
    
    return score

if __name__ == "__main__":
    verify_compliance()
