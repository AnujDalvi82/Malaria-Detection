import requests

# ⚠️ REPLACE this URL with your actual Hugging Face Space URL!
# Example format: "https://your-username-malaria-classifier-api.hf.space/predict"
API_URL = "https://<YOUR_HUGGINGFACE_USERNAME>-malaria-classifier-api.hf.space/predict"

# Path to a locally saved cell image you want to test
IMAGE_PATH = "processed_cells/parasite/cell_0.png" # You may need to update this name based on existing files

def test_api():
    try:
        with open(IMAGE_PATH, 'rb') as f:
            # The key 'file' must match the parameter name in our Fastapi app: file: UploadFile = File(...)
            files = {'file': (IMAGE_PATH, f, 'image/png')}
            
            print(f"Sending request to {API_URL}...")
            response = requests.post(API_URL, files=files)
            
            # Print the result
            if response.status_code == 200:
                print("✅ Success!")
                print("Prediction Data:", response.json())
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                
    except FileNotFoundError:
        print(f"Please update IMAGE_PATH. Could not find file at: {IMAGE_PATH}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_api()
