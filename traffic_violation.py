import cv2
import datetime
import os
import winsound

class ViolationChecker:
    def __init__(self, stop_line_y=550):
        self.stop_line_y = stop_line_y
        if not os.path.exists('evidence'): 
            os.makedirs('evidence')

    def process(self, frame, detections, lights):
        current_status = "none" 
        if lights:
            current_status = lights[0]['status']
        
        # ĐỊNH NGHĨA BIẾN MÀU SẮC Ở ĐÂY
        color_to_use = (0, 0, 255) if current_status.lower() == "red" else (0, 255, 0)
        
        # Vẽ vạch dừng ảo
        cv2.line(frame, (0, self.stop_line_y), (frame.shape[1], self.stop_line_y), color_to_use, 3)
        
        # SỬA LỖI NAMEERROR: Thay 'color_line' bằng 'color_to_use'
        cv2.putText(frame, f"LIGHT: {current_status.upper()}", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color_to_use, 2)

        for v in detections:
            x1, y1, x2, y2 = v['box']
            
            # Kiểm tra vi phạm vượt đèn đỏ
            if current_status.lower() == "red" and y2 > (self.stop_line_y - 5):
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 4)
                cv2.putText(frame, "VI PHAM: VUOT DEN DO", (x1, y1-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                
                # Lưu bằng chứng
                now = datetime.datetime.now().strftime("%H%M%S_%f")
                cv2.imwrite(f"evidence/red_light_{now}.jpg", frame)
                winsound.Beep(1000, 400)

            # Kiểm tra mũ bảo hiểm
            if v.get('has_helmet') == 'no_helmet':
                cv2.putText(frame, "NO HELMET", (x1, y1-30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

        return frame