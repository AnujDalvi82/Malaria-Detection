 🌍 Map of Content (MoC): Malaria AI Project

This file serves as the central hub for the Obsidian Graph View. By branching out from this file, you can visualize the relationships between the project's codebase, architecture, and theoretical concepts.

## 📌 Core Documentation
- [[PROJECT_SUMMARY.md|Full Project Journey & Technical Summary]]
- [[README.md|Main Project Documentation]] (Featuring AI-generated banner and tech badges)

## 🧬 Data & Preprocessing
- **Raw Data**: `training.json`
- **Transformation Script**: [[prepare_yolo_data.py]] (Converts JSON coordinates to [[YOLO Format]])
- **Dataset Config**: [[dataset.yaml]]
- **Data Categories**: [[Infected Cells]] and [[Uninfected Cells]]

## 🧠 AI & Model Architecture
- **Phase 1 Approach**: [[Image Classification]] using [[TensorFlow]] & [[Keras]] (Legacy)
- **Current Approach**: [[Object Detection]] using [[Ultralytics YOLOv8]]
  - *Current Model Weights*: `best.pt` (Achieved 91.1% Precision, 78.6% mAP50)
  - *Automated Training*: [[train_loop.py]] (Handles PyTorch memory leaks via scheduled restarts)
  - *Hardware Optimization*: [[Apple Silicon MPS]] / [[Unified Memory]]

## ⚙️ Backend API & Services
- **Web Framework**: [[FastAPI]]
- **Main Application**: [[app.py]] (Serves the YOLOv8 model via `/predict` endpoint)
- **Model Tracking**: [[log_model.py]] using [[MLflow]]
- **Integration**: [[Notion Sync]] via [[sync_notion.py]] (Token securely redacted for public deployment)

## 🎨 Frontend UI
- **Location**: [[static]] directory
- **Design Paradigm**: [[Glassmorphism]] / [[Dark Mode]]
- **Core Files**: `index.html`, `script.js` (Reactive bounding box mapping), `style.css`

## 🚀 Deployment & DevOps
- **Containerization**: [[Dockerfile]] (Configured for OpenCV C++ headless bindings)
- **Version Control**: [[GitHub]] (Massive data and logs safely ignored via `.gitignore`)
- **Cloud Hosting**: [[Hugging Face Spaces]] (Imported and auto-deployed directly from GitHub)
- **Dependencies**: [[requirements.txt]]
- **Testing**: [[tests]] directory / [[test_app.py]] / [[test_live_api.py]]

---
*Tags:* #malaria #computervision #deeplearning #yolov8 #fastapi #docker #huggingface #apple-silicon #github
