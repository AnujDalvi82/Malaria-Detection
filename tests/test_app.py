from fastapi.testclient import TestClient
from app import app

# Create a test client using your FastAPI app
client = TestClient(app)

def test_read_root():
    """Test that the root endpoint returns the correct welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

def test_predict_endpoint_no_file():
    """Test that the predict endpoint properly rejects requests without an image."""
    response = client.post("/predict")
    # 422 is the standard HTTP status code for Validation Error (missing file)
    assert response.status_code == 422 
