 🌍 Map of Content (MoC): Malaria AI Project

This file serves as the central hub for the Obsidian Graph View. By branching out from this file, you can visualize the relationships between the project's codebase, architecture, and theoretical concepts.

## 📌 Core Documentation
- [[PROJECT_SUMMARY.md|Full Project Journey & Technical Summary]]
- [[README.md|Main Project Documentation]]

## 🧬 Data & Preprocessing
- **Raw Data**: `training.json`
- **Transformation Script**: [[prepare_yolo_data.py]] (Converts JSON coordinates to [[YOLO Format]])
- **Dataset Config**: [[dataset.yaml]]
- **Data Categories**: [[Infected Cells]] and [[Uninfected Cells]]

## 🧠 AI & Model Architecture
- **Phase 1 Approach**: [[Image Classification]] using [[TensorFlow]] & [[Keras]]
  - *Legacy Model*: `malaria_cell_classifier.h5`
- **Current Approach**: [[Object Detection]] using [[Ultralytics YOLOv8]]
  - *Current Model Weights*: `best.pt` / `yolov8s.pt`
  - *Hardware Optimization*: [[Apple Silicon MPS]] / [[Unified Memory]]

## ⚙️ Backend API & Services
- **Web Framework**: [[FastAPI]]
- **Main Application**: [[app.py]] (Serves the YOLOv8 model via `/predict` endpoint)
- **Model Tracking**: [[log_model.py]] using [[MLflow]]
- **Integration**: [[Notion Sync]] via [[sync_notion.py]]

## 🎨 Frontend UI
- **Location**: [[static]] directory
- **Design Paradigm**: [[Glassmorphism]] / [[Dark Mode]]
- **Core Files**: `index.html`, `script.js` (Reactive bounding box mapping), `style.css`

## 🚀 Deployment & DevOps
- **Containerization**: [[Dockerfile]]
- **Cloud Hosting**: [[Hugging Face Spaces]]
- **Dependencies**: [[requirements.txt]] (Includes Headless OpenCV & PyTorch)
- **CI/CD & Testing**: [[tests]] directory / [[test_app.py]] / [[test_live_api.py]] / [[GitHub Actions]]

---
*Tags:* #malaria #computervision #deeplearning #yolov8 #fastapi #docker #huggingface #apple-silicon
