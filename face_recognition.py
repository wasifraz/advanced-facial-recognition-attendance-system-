from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np

class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")        
        
        title_lbl = Label(self.root, text="FACE DETECTOR", 
                        font=("times new roman", 35, "bold"), 
                        bg="white", fg="green")
        title_lbl.place(x=0, y=0, width=1530, height=45)
        
        # TOP IMAGE - with error handling
        try:
            img_Top = Image.open(r"college images\face detector.webp")
            img_Top = img_Top.resize((650, 700), Image.Resampling.LANCZOS)
            self.photoimg_Top = ImageTk.PhotoImage(img_Top) 
            
            f_lbl = Label(self.root, image=self.photoimg_Top)
            f_lbl.place(x=0, y=55, width=650, height=700)
        except Exception as e:
            print(f"Could not load top image: {e}")
        
        # SIDE IMAGE - with error handling
        try:
            img_side = Image.open(r"college images\image 6.png")
            img_side = img_side.resize((950, 700), Image.Resampling.LANCZOS)
            self.photoimg_side = ImageTk.PhotoImage(img_side) 
            
            f_lbl = Label(self.root, image=self.photoimg_side)
            f_lbl.place(x=650, y=55, width=950, height=700)
        except Exception as e:
            print(f"Could not load side image: {e}")
        
        # Detect Face Button
        b1_1 = Button(self.root, text="DETECT FACE", 
                    command=self.face_recog, cursor="hand2", 
                    font=("times new roman", 18, "bold"), 
                    bg="darkgreen", fg="white")
        b1_1.place(x=1030, y=670, width=200, height=40)

    # ================= FACE DETECTOR ==================
    def face_recog(self):
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply histogram equalization for better recognition
            gray_image = cv2.equalizeHist(gray_image)
            
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)
            
            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                
                # Extract and process face region
                face_roi = gray_image[y:y + h, x:x + w]
                
                # Resize to standard size for better recognition
                face_roi = cv2.resize(face_roi, (200, 200))
                
                # Predict with confidence
                id, confidence = clf.predict(face_roi)
                
                # Convert confidence to percentage (lower distance = higher confidence)
                confidence_percentage = int(100 * (1 - confidence / 300))
                
                print(f"Detected ID: {id}, Confidence: {confidence_percentage}%, Raw distance: {confidence}")
                
                # Adjusted threshold for better recognition
                if confidence < 100:  # Lower threshold means stricter matching
                    try:
                        conn = mysql.connector.connect(
                            host="localhost",
                            username="root",
                            password="Raza@Khan2002",
                            database="face_recog"
                        )
                        my_cursor = conn.cursor()
                        
                        # Fetch student details using parameterized query (safer)
                        my_cursor.execute("SELECT StudentName, RollNo, Department FROM student WHERE StudentID=%s", (id,))
                        result = my_cursor.fetchone()
                        
                        if result:
                            n = str(result[0])
                            r = str(result[1])
                            d = str(result[2])
                            
                            # Display information with confidence
                            cv2.putText(img, f"Name: {n}", (x, y - 75), 
                                      cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                            cv2.putText(img, f"Roll: {r}", (x, y - 50), 
                                      cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                            cv2.putText(img, f"Dept: {d}", (x, y - 25), 
                                      cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                            cv2.putText(img, f"Confidence: {confidence_percentage}%", (x, y - 5), 
                                      cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
                        else:
                            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                            cv2.putText(img, "Unknown Face", (x, y - 5), 
                                    cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 3)
                        
                        conn.close()
                        
                    except mysql.connector.Error as err:
                        print(f"Database error: {err}")
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                        cv2.putText(img, "DB Error", (x, y - 5), 
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 3)
                else:
                    # Unknown face - low confidence
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y - 5), 
                            cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 3)
                    cv2.putText(img, f"Low Conf: {confidence_percentage}%", (x, y + h + 25), 
                            cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
            
            return img
        
        def recognize(img, clf, faceCascade):
            # Optimized parameters for better face detection
            img = draw_boundary(img, faceCascade, 1.1, 5, (255, 255, 255), "Face", clf)
            return img
        
        # Check if classifier file exists
        if not os.path.exists("classifier/classifier.xml") and not os.path.exists("classifier.xml"):
            messagebox.showerror("Error", "Trained model not found! Please train the model first.")
            return
        
        # Load Haar Cascade
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        
        if faceCascade.empty():
            messagebox.showerror("Error", "Could not load Haar Cascade classifier!")
            return
        
        # Load trained model
        clf = cv2.face.LBPHFaceRecognizer_create()
        
        try:
            if os.path.exists("classifier/classifier.xml"):
                clf.read("classifier/classifier.xml")
            else:
                clf.read("classifier.xml")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load trained model: {str(e)}")
            return
        
        # Open camera with better compatibility
        video_cap = cv2.VideoCapture(0)
        
        if not video_cap.isOpened():
            # Try without CAP_DSHOW
            video_cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        if not video_cap.isOpened():
            messagebox.showerror("Error", "Cannot access camera!")
            return
        
        # Set camera properties for better quality
        video_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        video_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        video_cap.set(cv2.CAP_PROP_FPS, 30)
        
        print("Press ENTER to exit...")
        
        while True:
            ret, img = video_cap.read()
            if not ret:
                print("Camera not accessible.")
                break

            img = recognize(img, clf, faceCascade)
            cv2.imshow("Face Recognition System - Press ENTER to Exit", img)
            
            # Press ENTER (13) to exit
            if cv2.waitKey(1) == 13:
                break
                
        video_cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()

