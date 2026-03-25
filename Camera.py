import cv2
import torch
from ultralytics import YOLO
import time
import os

class Camera:
    def __init__(self, model_path='yolov8n.pt', camera_index=0):
        print("Trying to initialize YOLO...")

        try:
            self.model = YOLO(model_path)
            print("Model loaded successfully")

            # Optimize model for Raspberry Pi
            self.model.amp = False
            self.model.fuse()

            # Test model with a simple inference
            try:
                with torch.no_grad():
                    test_tensor = torch.zeros(1, 3, 320, 320)   # Smaller test size
                    test_result = self.model(test_tensor)
                print("Model inference test passed")
            
            except Exception as e:
                print(f"Model inference test failed: {e}")
        
        except Exception as e:
            print(f"Error loading model: {e}")
            raise  # Re-raise so the script stops if model fails to load

        # Get device info

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
        print(f"Torch threads: {torch.get_num_threads()}")

        # Optimize torch for Raspberry Pi
        torch.set_num_threads(4)    # Limit threads to avoid overloading Pi


        print(f"Initializing USB camera (index {camera_index})...")

        # Initialize camera with optimized settings for Raspberry Pi
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(self.camera_index)
        time.sleep(1.0) # Give camera time to initialize

        # Set camera properties for better performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 15)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if not self.cap.isOpened():
            print(f"Error: Could not open USB camera at index {camera_index}")
            print("Available camera indices: 0, 1, 2... Try different indices if needed.")
            return
        
        # Test camera
        self.processing_size = 320
        ret, test_frame = self.cap.read()

        if not ret:
            print("Error: Could not read from camera")
            self.cap.release()
            return

        print("USB camera initialized successfully")
        print(f"Camera resolution: {test_frame.shape[1]}x{test_frame.shape[0]}")

        

    def num_of_people(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Error reading frame from camera")
        
        original_frame = frame.copy()

        height, width = frame.shape[:2]
        scale = self.processing_size / max(height, width)
        new_width = int(width * scale)
        new_height = int(height * scale)
        frame_resized = cv2.resize(frame, (new_width, new_height))
        try:
            results = self.model(
                frame_resized,
                imgsz=self.processing_size,
                verbose=False,
                conf=0.5,
                max_det=20,
                half=False,
                device='cpu',
                classes=[0]
            )

            # Print detection info occasionally
            if len(results) > 0 and len(results[0].boxes) > 0:
                boxes = results[0].boxes
                return len(boxes)
            else:
                return 0
        
        except Exception as e:
            print(f"Inference error: {e}")
                
    def __exit__(self):
        self.cap.release()


def main():
    camera = Camera()
    try:
        while True:
            people_count = camera.num_of_people()
            print(f"People Count: {people_count}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("Exiting program...")
    finally:
        camera.__exit__()

if __name__ == "__main__":
    main()