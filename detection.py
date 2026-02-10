import cv2
import os
from ultralytics import YOLO

class TrafficDetector:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        # Đảm bảo bạn đã copy file vào folder models
        self.vehicle_model = YOLO(os.path.join(BASE_DIR, 'models', 'vehicle.pt'))
        self.light_model = YOLO(os.path.join(BASE_DIR, 'models', 'traffic_light.pt'))
        self.helmet_model = YOLO(os.path.join(BASE_DIR, 'models', 'helmet.pt'))

    def detect_all(self, frame):
        # Stage 1: Phát hiện xe (Dùng stream=True để mượt hơn trên RTX 4050)
        vehicle_results = self.vehicle_model(frame, imgsz=640, verbose=False, stream=False)[0]
        
        detections = []
        for box in vehicle_results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = self.vehicle_model.names[int(box.cls[0])]
            vehicle_data = {"box": [x1, y1, x2, y2], "type": label, "has_helmet": None}

            # Stage 4: Kiểm tra mũ bảo hiểm cho xe máy
            if label == 'motorbike':
                roi = frame[max(0, y1):y2, max(0, x1):x2]
                if roi.size > 0:
                    h_res = self.helmet_model(roi, imgsz=416, verbose=False)[0]
                    if len(h_res.boxes) > 0:
                        vehicle_data["has_helmet"] = self.helmet_model.names[int(h_res.boxes[0].cls[0])]
            detections.append(vehicle_data)

        # Stage 2: Nhận diện đèn
        light_res = self.light_model(frame, imgsz=416, verbose=False)[0]
        lights = [{"status": self.light_model.names[int(l.cls[0])], "box": map(int, l.xyxy[0])} for l in light_res.boxes]

        return detections, lights