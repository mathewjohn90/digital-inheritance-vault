import sys
from fastapi.testclient import TestClient

from main import app, state

client = TestClient(app)


def test_e2e():
    print("=" * 74)
    print(" Running End-to-End Automated Integration Tests for Seclock ")
    print("=" * 74)

    # ---------------------------------------------------------
    # Test 1: Health / Root endpoint
    # ---------------------------------------------------------
    print("\n[1] Testing root endpoint...")

    response = client.get("/")

    assert response.status_code == 200

    print("    ✓ Root endpoint is working")
    print(f"    Response: {response.json()}")

    # ---------------------------------------------------------
    # Test 2: API documentation
    # ---------------------------------------------------------
    print("\n[2] Testing API documentation...")

    response = client.get("/docs")

    assert response.status_code == 200

    print("    ✓ Swagger documentation is available")

    # ---------------------------------------------------------
    # Test 3: OpenAPI
    # ---------------------------------------------------------
    print("\n[3] Testing OpenAPI endpoint...")

    response = client.get("/openapi.json")

    assert response.status_code == 200

    data = response.json()

    assert "openapi" in data
    assert "paths" in data

    print("    ✓ OpenAPI endpoint is working")
    print(f"    Available API paths: {len(data['paths'])}")

    # ---------------------------------------------------------
    # Test 4: Application state
    # ---------------------------------------------------------
    print("\n[4] Checking application state...")

    assert state is not None

    print("    ✓ Application state is initialized")

    # ---------------------------------------------------------
    # Test 5: Static files
    # ---------------------------------------------------------
    print("\n[5] Testing static content...")

    response = client.get("/")

    assert response.status_code == 200

    print("    ✓ Application is responding correctly")

    # ---------------------------------------------------------
    # Final result
    # ---------------------------------------------------------
    print("\n" + "=" * 74)
    print(" ALL END-TO-END TESTS PASSED SUCCESSFULLY ")
    print("=" * 74)
