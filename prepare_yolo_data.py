import json
import os
import cv2
from tqdm import tqdm
import random

# YOLO requires data in a specific txt format: <class_id> <x_center> <y_center> <width> <height>
# all values normalized between 0.0 and 1.0

print("🔍 Loading training.json...")
with open('training.json') as f:
    raw_data = json.load(f)

# Map labels. Parasites generally = 0, Healthy RBC = 1
# Update based on exact categories needed for YOLO detection
CLASS_MAPPING = {
    'red blood cell': 1,
    'trophozoite': 0,
    'ring': 0,
    'schizont': 0,
    'gametocyte': 0,
    'leukocyte': 2  # White blood cell
}

OUTPUT_DIR = "datasets/malaria_yolo"
os.makedirs(f"{OUTPUT_DIR}/images/train", exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/labels/train", exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/images/val", exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/labels/val", exist_ok=True)

# We will shuffle data to create train/val split
random.seed(42)
random.shuffle(raw_data)
split_idx = int(len(raw_data) * 0.8)
train_data = raw_data[:split_idx]
val_data = raw_data[split_idx:]

def process_data(data, split_name):
    print(f"⚙️ Processing {split_name} split...")
    for entry in tqdm(data):
        img_name = entry['image']['pathname'].split('/')[-1]
        img_path = os.path.join("images", img_name)
        
        # We must load the image to get its width and height for YOLO normalization
        img = cv2.imread(img_path)
        if img is None:
            continue
            
        img_h, img_w, _ = img.shape
        
        # Create YOLO label file
        label_file = img_name.rsplit('.', 1)[0] + ".txt"
        label_path = os.path.join(OUTPUT_DIR, "labels", split_name, label_file)
        
        with open(label_path, 'w') as lf:
            for obj in entry['objects']:
                cat = obj['category']
                if cat not in CLASS_MAPPING:
                    continue
                
                class_id = CLASS_MAPPING[cat]
                
                # Bounding box coords in Pascal VOC to YOLO
                r1 = obj['bounding_box']['minimum']['r']
                r2 = obj['bounding_box']['maximum']['r']
                c1 = obj['bounding_box']['minimum']['c']
                c2 = obj['bounding_box']['maximum']['c']
                
                # YOLO format calculations
                x_center = ((c1 + c2) / 2.0) / img_w
                y_center = ((r1 + r2) / 2.0) / img_h
                box_width = abs(c2 - c1) / img_w
                box_height = abs(r2 - r1) / img_h
                
                lf.write(f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}\n")
                
        # Move/copy image to yolo structure (using symbolic link for speed/space)
        dest_img_path = os.path.join(OUTPUT_DIR, "images", split_name, img_name)
        if not os.path.exists(dest_img_path):
            # Try to symlink, fallback to copy if OS complains
            try:
                os.symlink(os.path.abspath(img_path), dest_img_path)
            except OSError:
                import shutil
                shutil.copy2(img_path, dest_img_path)

process_data(train_data, 'train')
process_data(val_data, 'val')

# Generate YOLO config file (dataset.yaml)
yaml_content = f"""path: {os.path.abspath(OUTPUT_DIR)}
train: images/train
val: images/val

names:
  0: parasite
  1: red_blood_cell
  2: leukocyte
"""
with open("dataset.yaml", "w") as f:
    f.write(yaml_content)

print(f"\n✅ YOLO Data Preparation Complete! Dataset configuration written to dataset.yaml")
print("To train yolo, run: yolo task=detect mode=train model=yolov8n.pt data=dataset.yaml epochs=25 imgsz=640")
