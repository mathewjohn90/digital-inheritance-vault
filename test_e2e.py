from fastapi.testclient import TestClient

from main import app, state


client = TestClient(app)


def test_e2e():
    print("=" * 74)
    print(" Running End-to-End Automated Integration Tests for Seclock ")
    print("=" * 74)

    # Test 1: Root endpoint
    print("\n[1] Testing root endpoint...")
    response = client.get("/")

    assert response.status_code == 200

    print("    ✓ Root endpoint is working")
    print(f"    Content-Type: {response.headers.get('content-type')}")
    print(f"    Response length: {len(response.text)} characters")

    # Root endpoint returns HTML
    assert "text/html" in response.headers.get("content-type", "")

    # Test 2: API documentation
    print("\n[2] Testing API documentation...")
    response = client.get("/docs")

    assert response.status_code == 200

    print("    ✓ Swagger documentation is available")

    # Test 3: OpenAPI endpoint
    print("\n[3] Testing OpenAPI endpoint...")
    response = client.get("/openapi.json")

    assert response.status_code == 200

    data = response.json()

    assert "openapi" in data
    assert "paths" in data

    print("    ✓ OpenAPI endpoint is working")
    print(f"    Available API paths: {len(data['paths'])}")

    # Test 4: Application state
    print("\n[4] Checking application state...")
    assert state is not None

    print("    ✓ Application state is initialized")

    # Test 5: Root HTML content
    print("\n[5] Checking application HTML...")
    response = client.get("/")

    assert response.status_code == 200

    html = response.text.lower()

    assert "<html" in html
    assert "</html>" in html

    print("    ✓ HTML page is being served correctly")

    print("\n" + "=" * 74)
    print(" ALL END-TO-END TESTS PASSED SUCCESSFULLY ")
    print("=" * 74)
