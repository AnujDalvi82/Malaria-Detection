import mlflow
import tensorflow as tf
import os

# 1. Initialize MLflow Experiment
experiment_name = "Malaria_Cell_Classification"
mlflow.set_experiment(experiment_name)

# 2. Load the existing Keras model
model_path = "malaria_cell_classifier.h5"

if not os.path.exists(model_path):
    print(f"Error: {model_path} not found.")
    exit(1)

model = tf.keras.models.load_model(model_path)

# 3. Start an MLflow run to log the model and its metadata
with mlflow.start_run(run_name="Initial_Model_Upload") as run:
    # Log hyperparameters used during your training
    mlflow.log_param("architecture", "Baseline CNN")
    mlflow.log_param("image_size", "128x128")
    mlflow.log_param("color_mode", "RGB")
    mlflow.log_param("optimizer", "adam")
    mlflow.log_param("loss", "binary_crossentropy")
    
    # Log the actual model to the registry
    mlflow.tensorflow.log_model(
        model=model, 
        artifact_path="model", 
        registered_model_name="MalariaCellClassifier"
    )
    
    print("✅ Model successfully logged and registered in MLflow!")
    print(f"Run ID: {run.info.run_id}")

# To view the MLflow UI, run this in your terminal:
# mlflow ui
