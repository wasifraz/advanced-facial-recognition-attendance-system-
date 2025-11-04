import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import * # Still needed for messagebox
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import pooling, Error
import cv2
import os
import numpy as np
from collections import deque, Counter
import threading
import time
import csv
from datetime import datetime
from time import strftime

class Face_Recognition:
    def __init__(self, root):
        self.root = root
        
        # --- UI/UX CHANGE: Set window to open maximized ---
        self.root.state('zoomed')
        self.root.minsize(1280, 720)
        self.root.title("Face Recognition System")

        # --- UI/UX CHANGE: Modern Header ---
        header_frame = ttk.Frame(self.root, bootstyle="primary")
        header_frame.pack(fill=X, side=TOP)
        
        title_lbl = ttk.Label(
            header_frame, 
            text="FACE RECOGNITION SYSTEM", 
            font=("Segoe UI", 24, "bold"), 
            bootstyle="inverse-primary"
        )
        title_lbl.pack(side=LEFT, padx=20, pady=10)
        
        self.time_lbl = ttk.Label(
            header_frame, 
            font=("Segoe UI", 16, "bold"), 
            bootstyle="inverse-primary"
        )
        self.time_lbl.pack(side=RIGHT, padx=20, pady=10)
        self.update_time()

        # --- UI/UX CHANGE: Load original PIL images (for resizing) ---
        try:
            self.original_img_top = Image.open(r"college images\face detector.webp")
        except Exception as e:
            print(f"Error loading left image: {e}")
            self.original_img_top = None
        
        try:
            self.original_img_side = Image.open(r"college images\image 8.png")
        except Exception as e:
            print(f"Error loading right image: {e}")
            self.original_img_side = None

        # --- UI/UX CHANGE: Main frame to hold the 50/50 split ---
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=BOTH, expand=YES)

        # --- UI/UX CHANGE: Left 50% Frame ---
        self.left_frame = ttk.Frame(main_frame)
        self.left_frame.place(relx=0, rely=0, relwidth=0.46, relheight=1.0)
        
        self.f_lbl_top = ttk.Label(self.left_frame)
        self.f_lbl_top.place(relwidth=1, relheight=1)
        
        # --- UI/UX CHANGE: Right 50% Frame ---
        self.right_frame = ttk.Frame(main_frame)
        self.right_frame.place(relx=0.46, rely=0, relwidth=0.6, relheight=1.0)
        
        self.f_lbl_side = ttk.Label(self.right_frame)
        self.f_lbl_side.place(relwidth=1, relheight=1)

        # --- UI/UX CHANGE: Buttons (Placed relative to right_frame) ---
        # Placed near "78% scanning" area as requested
        b1_1 = ttk.Button(self.right_frame, text="▶ START FACE RECOGNITION",
                          cursor="hand2",
                          bootstyle="success-outline",
                          command=self.start_recognition_thread,
                          width=45,
                          padding=4)
        b1_1.place(relx=0.50, rely=0.90, anchor=CENTER) 

        b1_2 = ttk.Button(self.right_frame, text="🔍 CHECK DATABASE", 
                          cursor="hand2",
                          bootstyle="info-outline",
                          command=self.check_database,
                          width=39,
                          padding=4)
        b1_2.place(relx=0.50, rely=0.94, anchor=CENTER)

        # --- UI/UX CHANGE: Bind resize events to make images responsive ---
        self.left_frame.bind("<Configure>", self.on_left_resize)
        self.right_frame.bind("<Configure>", self.on_right_resize)

        # Store PhotoImage references to prevent garbage collection
        self.photoimg_Top = None 
        self.photoimg_side = None

        # Configuration
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.CASCADE_PATH = os.path.join(self.BASE_DIR, "haarcascade_frontalface_default.xml")
        self.CLASSIFIER_DIR = os.path.join(self.BASE_DIR, "classifier")
        self.CLASSIFIER_PATH = os.path.join(self.CLASSIFIER_DIR, "classifier.xml")
        self.CLASSIFIER_PATH_ALT = os.path.join(self.BASE_DIR, "classifier.xml")

        # Database connection pool configuration
        self.db_pool = None
        self.init_database_pool()

        # Recognition state
        self.recognition_running = False
        self.recognition_lock = threading.Lock()
        self.stop_flag = False

        # Smoothing and caching
        self.face_tracking = {}
        self.student_cache = {}
        self.last_recognized = {}

        print("✓ Face Recognition System Initialized Successfully")


    def on_left_resize(self, event):
        """Resizes the left image to fit its frame."""
        if not self.original_img_top:
            return
        width = event.width
        height = event.height
        

        if width < 2 or height < 2:
            return
            
        try:
            img = self.original_img_top.resize((width, height), Image.Resampling.LANCZOS)
            self.photoimg_Top = ImageTk.PhotoImage(img)
            self.f_lbl_top.config(image=self.photoimg_Top)
        except Exception as e:
            print(f"Error resizing left image: {e}")

    def on_right_resize(self, event):
        """Resizes the right image to fit its frame."""
        if not self.original_img_side:
            return
        width = event.width
        height = event.height
        
        # Prevent resizing to 1x1 on minimize
        if width < 2 or height < 2:
            return
    
        try:
            img = self.original_img_side.resize((width, height), Image.Resampling.LANCZOS)
            self.photoimg_side = ImageTk.PhotoImage(img)
            self.f_lbl_side.config(image=self.photoimg_side)
        except Exception as e:
            print(f"Error resizing right image: {e}")

    # --- UI/UX FIX: Thread-safe message box handler ---
    def show_message(self, type, title, message):
        """
        Shows a messagebox from the main thread to prevent crashes.
        Called from the recognition thread.
        """
        if type == "error":
            self.root.after(0, lambda: messagebox.showerror(title, message, parent=self.root))
        elif type == "warning":
            self.root.after(0, lambda: messagebox.showwarning(title, message, parent=self.root))
        else:
            self.root.after(0, lambda: messagebox.showinfo(title, message, parent=self.root))

    def init_database_pool(self):
        """Initialize MySQL connection pool for efficient database access"""
        try:
            self.db_pool = pooling.MySQLConnectionPool(
                pool_name="face_recog_pool",
                pool_size=5,
                pool_reset_session=True,
                host="localhost",
                user="root",
                password="Raza@Khan2002",
                database="face_recog",
                autocommit=True
            )
            print("✓ Database connection pool created successfully")
        except Error as e:
            print(f"✗ Database pool creation failed: {e}")
            self.db_pool = None

    def get_db_connection(self):
        """Get connection from pool with error handling"""
        try:
            if self.db_pool:
                return self.db_pool.get_connection()
        except Error as e:
            print(f"✗ Failed to get connection from pool: {e}")
        return None

    def check_database(self):
        """Debug function to check database contents using the connection pool."""
        print("\nRunning database diagnostic...")
        conn = self.get_db_connection()
        if not conn:
            messagebox.showerror("Database Error", "Failed to get a connection from the pool.\nCheck console for details.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT StudentID, StudentName, RollNo, Department FROM student")
            rows = cursor.fetchall()
            
            if not rows:
                messagebox.showwarning("Database Check", "❌ No students found in the database!\n\nPlease add students first.")
                return

            msg = f"✅ Found {len(rows)} student(s) in database:\n\n"
            for row in rows:
                msg += f"ID: {row[0]} | Name: {row[1]} | Roll: {row[2]} | Dept: {row[3]}\n"

            print("\n" + "="*70)
            print("DATABASE CONTENTS:")
            print("="*70)
            for row in rows:
                print(f"StudentID: {row[0]} (type: {type(row[0])}) | Name: {row[1]}")
            print("="*70 + "\n")

            messagebox.showinfo("Database Check", msg)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to query the database:\n{e}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close() 
                print("✓ Diagnostic finished, connection returned to pool.")

    def get_student_info(self, student_id):
        """Fetch student information with caching and error handling"""
        if student_id in self.student_cache:
            return self.student_cache[student_id]

        conn = self.get_db_connection()
        if not conn:
            return {"Name": "DB Error", "Roll": "N/A", "Dep": "N/A"}

        try:
            cursor = conn.cursor()
            query = "SELECT StudentName, RollNo, Department FROM student WHERE StudentID = %s"
            cursor.execute(query, (student_id,))
            result = cursor.fetchone()
            if result:
                info = {
                    "Name": str(result[0]) if result[0] else "Unknown",
                    "Roll": str(result[1]) if result[1] else "N/A",
                    "Dep": str(result[2]) if result[2] else "N/A"
                }
                print(f"✓ Loaded student: ID={student_id}, Name={info['Name']}")
            else:
                info = {"Name": "Not Found", "Roll": "N/A", "Dep": "N/A"}
                print(f"✗ Student ID {student_id} not found in database")
            
            self.student_cache[student_id] = info
            return info

        except Error as e:
            print(f"✗ Database query error: {e}")
            return {"Name": "DB Error", "Roll": "N/A", "Dep": "N/A"}
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def start_recognition_thread(self):
        """Start recognition in separate thread to prevent UI freeze"""
        with self.recognition_lock:
            if self.recognition_running:
                messagebox.showinfo("Info", "Recognition is already running!")
                return
            self.recognition_running = True
            self.stop_flag = False
        thread = threading.Thread(target=self.face_recog, daemon=True)
        thread.start()
        print("✓ Recognition thread started")
    
    def face_recog(self):
        """Main face recognition function with maximum accuracy and reliability"""
        print("\n" + "="*60)
        print("STARTING FACE RECOGNITION SYSTEM")
        print("="*60)

        if not os.path.exists(self.CASCADE_PATH):
            cascade_builtin = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
            if os.path.exists(cascade_builtin):
                self.CASCADE_PATH = cascade_builtin
                print(f"✓ Using built-in Haar Cascade: {cascade_builtin}")
            else:
                self.show_message("error", "Error",
                                  f"Haar Cascade not found!\n\nSearched in:\n1. {self.CASCADE_PATH}\n2. {cascade_builtin}\n\nPlease ensure the file exists.")
                self.recognition_running = False
                return
        else:
            print(f"✓ Haar Cascade found: {self.CASCADE_PATH}")

        classifier_loaded = False
        classifier_file = None
        for path in [self.CLASSIFIER_PATH, self.CLASSIFIER_PATH_ALT]:
            if os.path.exists(path):
                classifier_file = path
                file_size = os.path.getsize(path)
                print(f"✓ Classifier found: {path} (Size: {file_size} bytes)")
                if file_size < 100:
                    print(f"✗ WARNING: Classifier file is too small ({file_size} bytes)")
                    self.show_message("warning", "Warning",
                                      f"Classifier file is suspiciously small ({file_size} bytes).\nPlease retrain your model with adequate training data.")
                classifier_loaded = True
                break

        if not classifier_loaded:
            self.show_message("error", "Error",
                              f"Classifier not found!\n\nSearched in:\n1. {self.CLASSIFIER_PATH}\n2. {self.CLASSIFIER_PATH_ALT}\n\nPlease train your model first!")
            self.recognition_running = False
            return

        faceCascade = cv2.CascadeClassifier(self.CASCADE_PATH)
        if faceCascade.empty():
            self.show_message("error", "Error",
                              "Failed to load Haar Cascade!\nThe cascade file may be corrupted.")
            self.recognition_running = False
            return
        print("✓ Haar Cascade loaded successfully")

        try:
            clf = cv2.face.LBPHFaceRecognizer_create(
                radius=2,
                neighbors=16,
                grid_x=8,
                grid_y=8
            )
            clf.read(classifier_file)
            print(f"✓ LBPH Classifier loaded successfully from: {classifier_file}")

        except Exception as e:
            self.show_message("error", "Error",
                              f"Failed to load classifier!\n\nError: {str(e)}\n\nPossible causes:\n1. Classifier file is corrupted\n2. Model not properly trained\n3. opencv-contrib-python not installed\n\nSolution: Retrain your model.")
            self.recognition_running = False
            return

        if not self.db_pool:
            self.show_message("error", "Error",
                              "Database connection pool not initialized!\n\nPlease check:\n1. MySQL server is running\n2. Database 'face_recog' exists\n3. Credentials are correct")
            self.recognition_running = False
            return

        test_conn = self.get_db_connection()
        if not test_conn:
            self.show_message("error", "Error",
                              "Cannot connect to database!\nFace recognition will not work properly.")
            self.recognition_running = False
            return

        try:
            cursor = test_conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM student")
            student_count = cursor.fetchone()[0]
            cursor.close()
            test_conn.close()
            print(f"✓ Database connected: {student_count} students found")
            if student_count == 0:
                self.show_message("warning", "Warning",
                                "No students found in database!\nPlease add students before recognition.")
                self.recognition_running = False
                return

        except Error as e:
            self.show_message("error", "Error", f"Database error: {e}")
            self.recognition_running = False
            return

        print("\nOpening camera...")
        video_cap = cv2.VideoCapture(0)
        if not video_cap.isOpened():
            video_cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not video_cap.isOpened():
            self.show_message("error", "Error",
                            "Cannot access camera!\n\nPlease check:\n1. Camera is connected\n2. No other application is using it\n3. Camera drivers are installed")
            self.recognition_running = False
            return

        video_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        video_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        video_cap.set(cv2.CAP_PROP_FPS, 30)
        video_cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        actual_width = video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        actual_height = video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(f"✓ Camera opened: {int(actual_width)}x{int(actual_height)}")

        SCALE_FACTOR = 1.05
        MIN_NEIGHBORS = 6
        MIN_SIZE = (60, 60)
        CONFIDENCE_THRESHOLD = 50
        WINDOW_SIZE = 10
        CONSENSUS_RATIO = 0.5

        print("\n" + "="*60)
        print("RECOGNITION ACTIVE - Press ENTER to stop")
        print("="*60 + "\n")

        frame_count = 0
        fps_start_time = time.time()
        fps = 0

        while not self.stop_flag:
            ret, frame = video_cap.read()
            if not ret:
                print("✗ Failed to read frame")
                break

            frame_count += 1
            if frame_count % 30 == 0:
                fps = 30 / (time.time() - fps_start_time)
                fps_start_time = time.time()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            gray_enhanced = clahe.apply(gray)
            gray_denoised = cv2.fastNlMeansDenoising(gray_enhanced, None, 10, 7, 21)

            faces = faceCascade.detectMultiScale(
                gray_denoised,
                scaleFactor=SCALE_FACTOR,
                minNeighbors=MIN_NEIGHBORS,
                minSize=MIN_SIZE,
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            for (x, y, w, h) in faces:
                face_center = (x + w//2, y + h//2)
                face_key = self.get_face_key(face_center)

                if face_key not in self.face_tracking:
                    self.face_tracking[face_key] = deque(maxlen=WINDOW_SIZE)

                margin = 10
                y1, y2 = max(0, y - margin), min(gray.shape[0], y + h + margin)
                x1, x2 = max(0, x - margin), min(gray.shape[1], x + w + margin)

                face_roi = gray[y1:y2, x1:x2]
                if face_roi.size == 0:
                    continue
                try:
                    face_resized = cv2.resize(face_roi, (200, 200))
                    face_enhanced = clahe.apply(face_resized)
                    face_normalized = cv2.normalize(face_enhanced, None, 0, 255, cv2.NORM_MINMAX)
                    
                    predicted_id, distance = clf.predict(face_normalized)
                    confidence = max(0, min(100, int(100 * (1 - distance / 300))))
                    
                    self.face_tracking[face_key].append({
                        'id': predicted_id,
                        'confidence': confidence,
                        'distance': distance
                    })
                    
                    predictions = self.face_tracking[face_key]
                    if len(predictions) >= int(WINDOW_SIZE * 0.3):
                        ids = [p['id'] for p in predictions]
                        id_counter = Counter(ids)
                        most_common_id, count = id_counter.most_common(1)[0]
                        
                        id_confidences = [p['confidence'] for p in predictions if p['id'] == most_common_id]
                        id_distances = [p['distance'] for p in predictions if p['id'] == most_common_id]
                        avg_confidence = np.mean(id_confidences)
                        avg_distance = np.mean(id_distances)
                        consensus_ratio = count / len(predictions)
                        
                        consensus_met = consensus_ratio >= CONSENSUS_RATIO
                        confidence_met = avg_confidence >= CONFIDENCE_THRESHOLD
                        distance_good = avg_distance < 100
                        is_accepted = consensus_met and confidence_met and distance_good
                        
                        if is_accepted:
                            info = self.get_student_info(most_common_id)
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                            
                            name_text = f"Name: {info['Name']}"
                            id_text = f"ID: {most_common_id}"
                            roll_text = f"Roll: {info['Roll']}"
                            dept_text = f"Dept: {info['Dep']}"
                            conf_text = f"Conf: {int(avg_confidence)}%"
                            
                            y_offset = y - 10
                            texts = [name_text, id_text, roll_text, dept_text, conf_text]
                            for idx, text in enumerate(texts):
                                y_pos = y_offset - (len(texts) - idx) * 25
                                (text_width, text_height), _ = cv2.getTextSize(
                                    text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2
                                )
                                cv2.rectangle(frame,
                                              (x, y_pos - text_height - 5),
                                              (x + text_width + 10, y_pos + 5),
                                              (0, 255, 0), -1)
                                cv2.putText(frame, text, (x + 5, y_pos),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                            
                            if most_common_id not in self.last_recognized or \
                                    time.time() - self.last_recognized.get(most_common_id, 0) > 5:
                                print(f"✓ RECOGNIZED: {info['Name']} (ID: {most_common_id}) "
                                      f"- Confidence: {int(avg_confidence)}% "
                                      f"- Distance: {avg_distance:.2f}")
                                self.last_recognized[most_common_id] = time.time()
                                try:
                                    self.mark_attendance(most_common_id, info['Name'], info['Roll'], info['Dep'])
                                except Exception as _e:
                                    print(f"✗ Attendance call failed: {_e}")
                        else:
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
                            status_text = "UNKNOWN"
                            debug_text = f"ID:{most_common_id} C:{int(avg_confidence)}% D:{int(avg_distance)}"
                            reason_text = ""
                            if not consensus_met:
                                reason_text = f"Consensus:{int(consensus_ratio*100)}%<{int(CONSENSUS_RATIO*100)}%"
                            elif not confidence_met:
                                reason_text = f"LowConf:{int(avg_confidence)}%<{CONFIDENCE_THRESHOLD}%"
                            elif not distance_good:
                                reason_text = f"HighDist:{int(avg_distance)}"
                            cv2.putText(frame, status_text, (x, y - 40),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                            cv2.putText(frame, debug_text, (x, y - 15),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                            if reason_text:
                                cv2.putText(frame, reason_text, (x, y + h + 20),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                except Exception as e:
                    print(f"✗ Prediction error: {e}")
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    cv2.putText(frame, "ERROR", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

            cv2.putText(frame, f"FPS: {int(fps)}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(frame, f"Faces: {len(faces)}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(frame, "Press ENTER to exit", (10, frame.shape[0] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            cv2.imshow("Face Recognition System", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 13:  # ENTER key
                print("\n⚠ User requested exit via ENTER key")
                self.stop_flag = True
        
        print("\n" + "="*60)
        print("SHUTTING DOWN RECOGNITION SYSTEM")
        print("="*60)
        video_cap.release()
        cv2.destroyAllWindows()
        with self.recognition_lock:
            self.recognition_running = False
        print("✓ Camera released")
        print("✓ Windows closed")
        print("✓ Recognition stopped successfully\n")

    def mark_attendance(self, student_id, student_name, roll_no, department):
        """
        Append attendance to 'attendance.csv' in the script directory.
        Ensures one entry per student per day (no duplication).
        """
        try:
            filename = "attendance_report.csv"
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                with open(filename, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["StudentID", "Name", "RollNo", "Department", "Time", "Date", "Status"])

            now = datetime.now()
            date_str = now.strftime("%d-%m-%Y")
            time_str = now.strftime("%H:%M:%S")

            already_marked = False
            with open(filename, "r", newline="") as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row:
                        continue
                    try:
                        existing_id = str(row[0]).strip()
                        existing_date = str(row[5]).strip()
                    except IndexError:
                        continue
                    if existing_id == str(student_id) and existing_date == date_str:
                        already_marked = True
                        break

            if not already_marked:
                with open(filename, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([student_id, student_name, roll_no, department, time_str, date_str, "Present"])
                print(f"✓ Attendance saved: {student_name} ({student_id}) at {time_str} on {date_str}")
            else:
                print(f"ℹ️ Attendance already marked today for ID {student_id}")

        except Exception as e:
            print(f"✗ Failed to mark attendance: {e}")

    def get_face_key(self, center, tolerance=50):
        """Generate consistent key for face tracking across frames"""
        x_key = round(center[0] / tolerance) * tolerance
        y_key = round(center[1] / tolerance) * tolerance
        return (x_key, y_key)
    
    def update_time(self):
        """Fetches the current time and updates the time label."""
        string =strftime('%H:%M:%S %p')
        self.time_lbl.config(text=string)
        self.time_lbl.after(1000, self.update_time)    
    
if __name__ == "__main__":
    root = ttk.Window(themename="vapor") 
    obj = Face_Recognition(root)
    root.mainloop()