import requests
import json
import ssl
import urllib.request

# ==========================================
# 🛑 PASTE YOUR NOTION CREDENTIALS HERE 🛑
# ==========================================
NOTION_TOKEN = "YOUR_NOTION_TOKEN_HERE"
PAGE_ID = "YOUR_PAGE_ID_HERE"
# ==========================================

# Make sure you format the PAGE_ID correctly. 
# It's the 32-character string at the end of your Notion URL.
# If your URL is: https://www.notion.so/My-Project-1234567890abcdef1234567890abcdef
# Then your PAGE_ID is: 1234567890abcdef1234567890abcdef

def create_heading(content):
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": content}}]
        }
    }

def create_bullet(content):
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": content}}]
        }
    }

def create_todo(content, checked=False):
    return {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [{"type": "text", "text": {"content": content}}],
            "checked": checked
        }
    }

def create_divider():
    return {
        "object": "block",
        "type": "divider",
        "divider": {}
    }


def push_to_notion():
    url = f"https://api.notion.com/v1/blocks/{PAGE_ID}/children"

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    # Our beautiful generated list
    blocks = [
        create_divider(),
        create_heading("✅ What We've Accomplished (Recent Milestones)"),
        create_bullet("Architectural Pivot: Transitioned from rigid Image Classification CNN to a dynamic Object Detection framework (Ultralytics YOLOv8)."),
        create_bullet("Data Preparation: Wrote automated scripts to convert traditional polygon JSON coordinates into normalized YOLO formats."),
        create_bullet("Apple Silicon Training Optimization: Engineered around severe memory limit issues on Mac hardware by clamping batch sizes and using yolov8s."),
        create_bullet("Diagnosed PyTorch MPS Bugs: Identified a difficult Apple Silicon PyTorch bug where multi-dimensional boolean indexing silently corrupts tensor shapes."),
        create_bullet("Custom Ultralytics Patching: Manually edited 'tal.py' (TaskAlignedAssigner) source code locally, creating a custom defensive CPU fallback to protect GPU training runs from crashing."),
        create_bullet("Checkpoint Resumption: Mastered PyTorch checkpoints to safely restart frozen training runs securely without losing parameters."),
        create_divider(),
        create_heading("🚀 Further Tasks to Execute"),
        create_todo("Complete YOLO Training: Allow the backend process to finish its 100 Epoch execution safely.", checked=False),
        create_todo("Validate the Final Model: Test best.pt on unseen raw microscope slides to visually verify glowing red bounding boxes.", checked=False),
        create_todo("Export to production (Optional): Convert trained .pt model to ONNX format for faster execution speed.", checked=False),
        create_todo("API Integration: Hook up the final best.pt object detection model endpoint to app.py.", checked=False),
        create_todo("Frontend Bounding Box Logic: Ensure script.js mathematically calculates coordinates perfectly back onto the scaled UI.", checked=False),
        create_todo("Containerization: Run final Dockerfile specifically patched for PyTorch/OpenCV C++ graphics libraries (libgl1).", checked=False),
        create_todo("Hugging Face Deployment: Push FastAPI + YOLO + Dockerfile to cloud Spaces for the final live production release!", checked=False)
    ]

    payload = {"children": blocks}

    print("🚀 Pushing project data to Notion API...")
    try:
        response = requests.patch(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            print("✅ Successfully added all items to your Notion page!")
        else:
            print(f"❌ Failed to add to Notion. Status Code: {response.status_code}")
            print(f"Error Details: {response.text}")
            print("\nDid you remember to:")
            print("1. Insert your Integration Token?")
            print("2. Insert your Page ID?")
            print("3. Add your Bot as a connection to the specific Notion page (via the '...' menu -> 'Add connections')?")
    except requests.exceptions.RequestException as e:
        print(f"A network error occurred: {e}")

if __name__ == "__main__":
    push_to_notion()
