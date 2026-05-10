# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install system dependencies for OpenCV and YOLO
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

# Set the working directory to /code
WORKDIR /code

# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /code/requirements.txt

# Set up a non-root user named "user" with user ID 1000
# Hugging Face Spaces requires the container to run as a non-root user for security
RUN useradd -m -u 1000 user
USER user

# Set environment variables for the user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Change the working directory to the user's home app directory
WORKDIR $HOME/app

# Copy all the files into the container at $HOME/app, owned by the new user
COPY --chown=user . $HOME/app

# Expose port 7860 (The default expected by Hugging Face Spaces)
EXPOSE 7860

# Command to run the Fastapi application using uvicorn on port 7860
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
