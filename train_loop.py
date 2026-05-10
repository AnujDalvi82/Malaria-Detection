import subprocess
import time
import signal
import sys

# The command you want to run
COMMAND = [
    "yolo", 
    "task=detect", 
    "mode=train", 
    "resume=True", 
    "model=runs/detect/train5/weights/last.pt", 
    "device=mps", 
    "batch=4"
]

def run_training_loop():
    print("Starting automated training loop. Will pause training every 25 minutes to free memory.")
    while True:
        print("\n" + "="*50)
        print("Starting/Resuming YOLO Training...")
        print("="*50)
        
        # Start the YOLOv8 process
        process = subprocess.Popen(COMMAND)
        
        try:
            # Let it run for 25 minutes (1500 seconds)
            # process.wait() will block until the process finishes or timeouts
            process.wait(timeout=2500)
            
            # If wait() returns without a TimeoutExpired exception, the training 
            # either finished successfully or crashed.
            if process.returncode == 0:
                print("\nTraining finished successfully! Exiting loop.")
                break
            else:
                print(f"\nTraining exited unexpectedly with error code {process.returncode}.")
                print("Check if the model path is correct or if there was an actual error.")
                break
                
        except subprocess.TimeoutExpired:
            # 25 minutes passed, we need to interrupt it
            print("\n" + "="*50)
            print("25 minutes elapsed. Sending interrupt signal (Ctrl+C) to save checkpoint safely...")
            
            # Send SIGINT. Ultralytics YOLOv8 intercepts this and safely saves `last.pt` before exiting.
            process.send_signal(signal.SIGINT)
            
            try:
                # Give it up to 60 seconds to save state and exit gracefully
                process.wait(timeout=60)
                print("Process cleanly exited and checkpoint saved.")
            except subprocess.TimeoutExpired:
                print("YOLO process is stuck, forcing termination...")
                process.terminate()
                process.wait()
            
            # Wait a few seconds to let macOS garbage collection free up MPS and RAM memory completely
            print("Taking a 10-second breather to free up cache/memory...")
            time.sleep(10)

if __name__ == "__main__":
    try:
        run_training_loop()
    except KeyboardInterrupt:
        print("\n\nTraining loop script interrupted by user. Exiting.")
        sys.exit(0)
