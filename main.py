import cv2
import os
from detection import TrafficDetector
from traffic_violation import ViolationChecker

def run_system():
    detector = TrafficDetector()
    
    # BƯỚC QUAN TRỌNG: Chỉnh con số này để vạch kẻ nằm đúng vạch sơn thực tế
    # Nếu vạch thực tế ở thấp hơn, hãy tăng lên 600, 650...
    checker = ViolationChecker(stop_line_y=580) 
    
    video_path = "16h15.15.9.22.mp4"
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        detections, lights = detector.detect_all(frame)
        result_frame = checker.process(frame, detections, lights)

        cv2.imshow("He Thong Phat Nguoi - Bam Q de thoat", result_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_system() 