import cv2
import mediapipe as mp
import time
import pyautogui
import tkinter as tk



# lớp cha
class Event:
    def __init__(self):
        self.mouse_down = False
        self.count = 0
        self.target_count = 0

    def spuat(self, distance1):
        if distance1 < 125 and not self.mouse_down:
            pyautogui.mouseDown() 
            
            self.mouse_down = True
        elif distance1 >= 130 and self.mouse_down:
            pyautogui.mouseUp()
            self.mouse_down = False
            self.count += 1

            if self.count == self.target_count:
                
                # Gọi phương thức trừu tượng
                self.mission_complete()  
                 
                
    # Phương thức này sẽ được ghi đè trong các lớp con    
    def mission_complete(self):
        pass  

# Kế thừa từ lớp cha Event
class complete(Event):
    def mission_complete(self):
        print("Mission complete")
        
# Đa hình     
class Another(Event):
    def mission_complete(self):
        cv2.putText(img, "Mission complete", (40, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
        cv2.imshow("Train Spuat", img)
        cv2.waitKey(3000)
        cv2.destroyWindow("Train Spuat")
        

# nhận diện pose
mpPose = mp.solutions.pose
pose = mpPose.Pose( model_complexity=2,min_detection_confidence=0.9, min_tracking_confidence=0.9)

# vẽ các khớp nối ra
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(1)
pTime = 0

# Sử dụng đóng gói để tạo đối tượng
sukien = complete()

# Sử dụng đa hình
sukien = Another()

h, w, c = 0, 0, 0

def set_count():
    sukien.target_count = int(entry.get())

root = tk.Tk()

root.title("calculator Count")
root.geometry("250x200") 
label = tk.Label(root, text="Enter count:")
label.pack()
entry = tk.Entry(root)
entry.pack()
button = tk.Button(root, text="Set count", command=set_count)
button.pack()

cv2.namedWindow("Real", cv2.WINDOW_NORMAL)


while cap.isOpened():
    root.update()
    success,img=cap.read()
    if not success:
        continue

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    results = pose.process(imgRGB)

    
    # ghi các điểm kết quả ra
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h , w, c = img.shape
            cx, cy = int(w * lm.x), int(h * lm.y)
            
            if id == 24:
                left_hip = [cx, cy]
            if id == 28:
                right_anke = [cx, cy]
                
     # công thức pytago không gian   
        distance1 = ((left_hip[0] - right_anke[0]) ** 2 + (left_hip[1] - right_anke[1]) ** 2) ** 0.5
        sukien.spuat(distance1)
                
    cTime=time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(0,240,5),3)
    
    # Ghi lại số lần spuat
    cv2.rectangle(img, (10, h - 40), (250, h - 10), (55, 20, 255), -1)
    cv2.putText(img, f"Counted: {sukien.count}", (20, h - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    
    cv2.imshow("Real", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
