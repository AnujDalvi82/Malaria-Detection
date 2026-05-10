# Malaria AI - Full Project Journey & Technical Summary 🚀

## Introduction & Aim
The goal of this project was to build an intelligent, production-ready AI system capable of diagnosing malaria from microscope slide imagery. What started as an experimental Jupyter Notebook evolved through several architectural iterations into a robust, cloud-deployed Computer Vision microservice.

---

## Phase 1: The Initial CNN Architecture & Data Extraction
**The Starting Point:** We began with raw microscope images and a bulky `training.json` file containing bounding box coordinates mapping where cells and parasites were located.

**Our First Approach:** We approached this as an **Image Classification** problem. 
1. In a Jupyter Notebook, we wrote a Python script to iterate through the `training.json` and physically *crop* out the individual cells from the larger slides.
2. We sorted these cropped thumbnails into two massive folders: `processed_cells/parasite` and `processed_cells/uninfected`.
3. We built and trained a **TensorFlow/Keras Convolutional Neural Network (CNN)** on these perfectly centered 128x128 pixel crops.
4. The model achieved >94% accuracy and was exported as `malaria_cell_classifier.h5`.

---

## Phase 2: Deploying the CNN & Setting up MLOps
**The Problem:** The model was stuck on a local hard drive. There was no way to share it, run it on a server, or let a user interact with it.

**The Solution:** We transitioned out of the notebook into standard software engineering.
* **Backend:** We wrapped the `.h5` model inside a **FastAPI** web server, exposing a `/predict` endpoint.
* **Tracking:** We wrote `log_model.py` to register the model cleanly into **MLflow** for future version control.
* **Containerization:** We wrote a **Dockerfile** using `python:3.10-slim` and headless OpenCV so the app could run precisely identical anywhere in the world.
* **CI/CD:** We built **GitHub Actions** and wrote **Pytest** tests to automatically test the API whenever code was changed.

---

## Phase 3: The Architectural Problem & Hosting Limitations
**The Problem:** We wanted to deploy the API to a platform and give it a beautiful UI. However, standard Serverless structures have tight size limits (usually 250MB) which the massive TensorFlow library exceeded. Furthermore, the UI highlighted a deeper, fundamental flaw in our AI architecture:
* Our CNN required the user to upload a *pre-cropped, perfectly centered single cell*. 
* In the real world, doctors upload **massive, chaotic slide images** containing hundreds of overlapping cells. The CNN had no idea how to "find" the cells in the image.

**The Solution:**
* **Hosting Pivot:** We shifted to **Hugging Face Spaces**, which natively supports heavy Docker ML containers. We updated our Dockerfile to run on Port 7860 using an unprivileged non-root user to match Hugging Face’s strict security patterns.
* **UI Integration:** We built a stunning, dark-mode Glassmorphism UI (HTML/CSS/JS) and mounted it directly into the FastAPI server so the API and UI were packaged as one unit.

---

## Phase 4: The Ultimate Solution (YOLOv8 Object Detection)
**The Problem:** We needed the AI to scan a massive image, hunt down the cells, and draw boxes around the infected ones—a process the `.h5` classification model mathematically could not do.

**The Solution:** The complete pivot to **Object Detection**.
1. **Ditching TensorFlow:** We abandoned the CNN classifier approach entirely and embraced **Ultralytics YOLOv8**.
2. **Data Transformation:** We wrote `prepare_yolo_data.py` to computationally convert the JSON coordinates into math formats between `0.0` and `1.0` (YOLO format), creating `train` and `val` text files linking directly to the full-size images.
3. **Training YOLO:** The legacy `processed_cells` directory was deleted, and a new custom base model was trained natively.

---

## Phase 5: The Full-Stack Integration
**The Problem:** Integrating the new YOLO model (`best.pt`) with the UI.

**The Solution:** 
1. **API Overhaul:** We rewrote `app.py` to replace TensorFlow with Ultralytics. The API now returns large JSON arrays detailing every box it found: `[x1, y1, x2, y2, confidence, label]`. 
2. **Reactive Frontend:** We upgraded `script.js` to mathematically calculate bounding box logic and project glowing CSS components dynamically onto the target.

---

## Phase 6: Hardware Optimization & Deployment Bug Fixes
**The Problem:** Taking an ML Model to Production often exposes unforeseen bottlenecks in memory, rendering frameworks, and system dependencies deep inside Linux containers.

**The Solution:**
1. **Apple Silicon Unified Memory Overflows:** While chasing maximum accuracy with the massive `yolov8m` model, we hit an architectural bottleneck. The model requested 12.4GB of RAM, overflowing the Mac's physical memory boundaries. This triggered brutal SSD "Swap Memory" ping-ponging, slowing training to an unusable 78 seconds-per-iteration. We successfully engineered around this by stepping down to `yolov8s` (Small), dropping image bounds to `640`, and explicitly locking `batch=4` alongside `device=mps`. This clamped GPU demand at 3GB entirely inside physical RAM, boosting iteration speeds by 900%.
2. **Docker System Library Crashing:** Upon deploying the YOLO FastApi wrapper to Hugging Face via the Dockerfile, the cloud container crashed throwing `libGL.so.1` errors. OpenCV strictly relies on underlying C++ Video Rendering libraries which do not ship in minimalist Python slim environments. We patched the Dockerfile with an immediate `apt-get install libgl1 libglib2.0-0` execution layer, permanently bridging the graphics interface dependency.
3. **Frontend Spatial Math Anomalies:** When overlaying bounding boxes onto the web UI, the UI's `object-fit: contain` CSS caused image letterboxing and coordinate drift. We rewrote the coordinate transformation loop in `script.js` to cross-reference HTML Container Aspect Ratios against Raw Internal Image Aspect Ratios, extracting the exact horizontal/vertical offset required to perfectly nail the glowing boxes to the rendered cells regardless of user screen size.
4. **PyTorch Memory Leak Mitigations:** Long PyTorch Dataloader workloads on Apple Silicon sometimes fail to properly clear garbage collection, resulting in creeping SSD swap accumulation. We countered this exponential slowdown by strategically pausing the terminal and executing a YOLO `resume=True` flag against the current `last.pt` weights. This reliably flushed the physical RAM caches, dynamically restoring GPU performance to full capacity without dropping training progress.
5. **Windows NVIDIA VRAM vs Mac Unified Memory:** Designed cross-platform mitigation strategies for memory bounds. While Apple Silicon cleanly handled massive memory requests via slow SSD Unified Memory swaps, executing the same codebase on enterprise NVIDIA GPUs triggered volatile `CUDA Out Of Memory (OOM)` fatal crashes. We mathematically bounded the Tensor loads via precise `batch` size rationing to lock PyTorch footprints strictly within hardware VRAM ceilings, securing cross-ecosystem stability.

---

## The Final Tech Stack
* **AI Architecture:** Ultralytics YOLOv8s Object Detection (MPS Accelerated)
* **Backend:** Python, FastAPI, OpenCV
* **Frontend:** Vanilla HTML/CSS/JS with reactive scaling
* **Deployment System:** Docker mapping to Hugging Face Spaces
