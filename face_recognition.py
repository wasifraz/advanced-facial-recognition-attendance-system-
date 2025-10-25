from tkinter import *
from tkinter import ttk, messagebox
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
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        title_lbl = Label(self.root, text="FACE RECOGNITION SYSTEM",
                        font=("times new roman", 35, "bold"),
                        bg="skyblue", fg="darkgreen")
        title_lbl.place(x=0, y=0, width=1530, height=45)
        
        # ============================time=============================
        self.time_lbl = Label(title_lbl, font=("times new roman", 14, "bold"), bg="skyblue", fg="white")
        self.time_lbl.place(x=0, y=0, width=130, height=45) 
        self.update_time()


        # Images with error handling
        try:
            img_Top = Image.open(r"college images\face detector.webp")
            img_Top = img_Top.resize((650, 750), Image.Resampling.LANCZOS)
            self.photoimg_Top = ImageTk.PhotoImage(img_Top)
            f_lbl = Label(self.root, image=self.photoimg_Top)
            f_lbl.place(x=0, y=45, width=650, height=750)
        except:
            pass

        try:
            img_side = Image.open(r"college images\image 8.png")
            img_side = img_side.resize((950, 750), Image.Resampling.LANCZOS)
            self.photoimg_side = ImageTk.PhotoImage(img_side)
            f_lbl = Label(self.root, image=self.photoimg_side)
            f_lbl.place(x=650, y=45, width=950, height=750)
        except:
            pass

        # Buttons
        b1_1 = Button(self.root, text="START FACE RECOGNITION", cursor="hand2",
                    font=("times new roman", 15, "bold"), bg="darkgreen", fg="white",
                    command=self.start_recognition_thread)
        b1_1.place(x=970, y=705, width=300, height=27)

        # button with Database Check === 
        b1_2 = Button(self.root, text="🔍 CHECK DATABASE", cursor="hand2",
                    font=("times new roman", 15, "bold"), bg="blue", fg="white",
                    command=self.check_database) # Command changed
        b1_2.place(x=970, y=735, width=300, height=24)

        #=============================face recognition================================
        
        # Configuration
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.CASCADE_PATH = os.path.join(self.BASE_DIR, "haarcascade_frontalface_default.xml")
        self.CLASSIFIER_DIR = os.path.join(self.BASE_DIR, "classifier")
        self.CLASSIFIER_PATH = os.path.join(self.CLASSIFIER_DIR, "classifier.xml")
        # Alternative paths
        self.CLASSIFIER_PATH_ALT = os.path.join(self.BASE_DIR, "classifier.xml")

        # Database connection pool configuration
        self.db_pool = None
        self.init_database_pool()

        # Recognition state
        self.recognition_running = False
        self.recognition_lock = threading.Lock()
        self.stop_flag = False

        # Smoothing and caching
        self.face_tracking = {}  # Track multiple faces: {face_position: deque of predictions}
        self.student_cache = {}
        self.last_recognized = {}  # Prevent duplicate alerts

        print("✓ Face Recognition System Initialized Successfully")

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

    # === ADDED: Database diagnostic function from first script (and upgraded) ===
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
                conn.close() # Returns the connection to the pool
                print("✓ Diagnostic finished, connection returned to pool.")
    # ========================================================================

    def get_student_info(self, student_id):
        """Fetch student information with caching and error handling"""
        # Check cache first
        if student_id in self.student_cache:
            return self.student_cache[student_id]

        # Fetch from database
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
        # ============= STEP 1: VALIDATE FILES =============
        print("\n" + "="*60)
        print("STARTING FACE RECOGNITION SYSTEM")
        print("="*60)

        # Check Haar Cascade
        if not os.path.exists(self.CASCADE_PATH):
            # Try OpenCV's built-in path
            cascade_builtin = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
            if os.path.exists(cascade_builtin):
                self.CASCADE_PATH = cascade_builtin
                print(f"✓ Using built-in Haar Cascade: {cascade_builtin}")
            else:
                messagebox.showerror("Error",
                                    f"Haar Cascade not found!\n\n"
                                    f"Searched in:\n"
                                    f"1. {self.CASCADE_PATH}\n"
                                    f"2. {cascade_builtin}\n\n"
                                    f"Please ensure the file exists.")
                self.recognition_running = False
                return
        else:
            print(f"✓ Haar Cascade found: {self.CASCADE_PATH}")

        # Check Classifier (try multiple locations)
        classifier_loaded = False
        classifier_file = None
        for path in [self.CLASSIFIER_PATH, self.CLASSIFIER_PATH_ALT]:
            if os.path.exists(path):
                classifier_file = path
                file_size = os.path.getsize(path)
                print(f"✓ Classifier found: {path} (Size: {file_size} bytes)")
                if file_size < 100:
                    print(f"✗ WARNING: Classifier file is too small ({file_size} bytes)")
                    print("  This indicates the model may not be properly trained!")
                    messagebox.showwarning("Warning",
                                        f"Classifier file is suspiciously small ({file_size} bytes).\n"
                                        f"Please retrain your model with adequate training data.")
                classifier_loaded = True
                break

        if not classifier_loaded:
            messagebox.showerror("Error",
                                f"Classifier not found!\n\n"
                                f"Searched in:\n"
                                f"1. {self.CLASSIFIER_PATH}\n"
                                f"2. {self.CLASSIFIER_PATH_ALT}\n\n"
                                f"Please train your model first!")
            self.recognition_running = False
            return

        # ============= STEP 2: LOAD CASCADE =============
        faceCascade = cv2.CascadeClassifier(self.CASCADE_PATH)
        if faceCascade.empty():
            messagebox.showerror("Error",
                                "Failed to load Haar Cascade!\n"
                                "The cascade file may be corrupted.")
            self.recognition_running = False
            return
        print("✓ Haar Cascade loaded successfully")

        # ============= STEP 3: LOAD CLASSIFIER =============
        try:
            clf = cv2.face.LBPHFaceRecognizer_create(
                radius=2,
                neighbors=16,
                grid_x=8,
                grid_y=8
            )
            clf.read(classifier_file)
            print(f"✓ LBPH Classifier loaded successfully from: {classifier_file}")
            print(f"  Parameters: radius=2, neighbors=16, grid=8x8")

        except Exception as e:
            messagebox.showerror("Error",
                                f"Failed to load classifier!\n\n"
                                f"Error: {str(e)}\n\n"
                                f"Possible causes:\n"
                                f"1. Classifier file is corrupted\n"
                                f"2. Model not properly trained\n"
                                f"3. opencv-contrib-python not installed\n\n"
                                f"Solution: Retrain your model or reinstall:\n"
                                f"pip install opencv-contrib-python")
            self.recognition_running = False
            return

        # ============= STEP 4: TEST DATABASE CONNECTION =============
        if not self.db_pool:
            messagebox.showerror("Error",
                                "Database connection pool not initialized!\n\n"
                                "Please check:\n"
                                "1. MySQL server is running\n"
                                "2. Database 'face_recog' exists\n"
                                "3. Credentials are correct\n"
                                "4. Student table exists with data")
            self.recognition_running = False
            return

        test_conn = self.get_db_connection()
        if not test_conn:
            messagebox.showerror("Error",
                                "Cannot connect to database!\n"
                                "Face recognition will not work properly.")
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
                messagebox.showwarning("Warning",
                                    "No students found in database!\n"
                                    "Please add students before recognition.")
                self.recognition_running = False
                return

        except Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
            self.recognition_running = False
            return

        # ============= STEP 5: OPEN CAMERA =============
        print("\nOpening camera...")
        video_cap = cv2.VideoCapture(0)
        if not video_cap.isOpened():
            video_cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not video_cap.isOpened():
            messagebox.showerror("Error",
                                "Cannot access camera!\n\n"
                                "Please check:\n"
                                "1. Camera is connected\n"
                                "2. No other application is using it\n"
                                "3. Camera drivers are installed")
            self.recognition_running = False
            return

        # Set optimal camera properties
        video_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        video_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        video_cap.set(cv2.CAP_PROP_FPS, 30)
        video_cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce latency

        actual_width = video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        actual_height = video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(f"✓ Camera opened: {int(actual_width)}x{int(actual_height)}")

        # ============= STEP 6: RECOGNITION PARAMETERS =============
        SCALE_FACTOR = 1.05  # Smaller = more thorough but slower
        MIN_NEIGHBORS = 6    # Higher = fewer false positives
        MIN_SIZE = (60, 60)  # Minimum face size to detect
        # Confidence thresholds (CRITICAL FOR ACCURACY)
        CONFIDENCE_THRESHOLD = 50  # Accept predictions above this
        HIGH_CONFIDENCE = 70       # High confidence threshold
        # Smoothing parameters
        WINDOW_SIZE = 10           # Larger window = more stable
        CONSENSUS_RATIO = 0.5      # 50% must agree
        print(f"\nRecognition Parameters:")
        print(f"  Scale Factor: {SCALE_FACTOR}")
        print(f"  Min Neighbors: {MIN_NEIGHBORS}")
        print(f"  Min Face Size: {MIN_SIZE}")
        print(f"  Confidence Threshold: {CONFIDENCE_THRESHOLD}%")
        print(f"  Window Size: {WINDOW_SIZE} frames")
        print(f"  Consensus Required: {int(CONSENSUS_RATIO * 100)}%")

        # ============= STEP 7: MAIN RECOGNITION LOOP =============
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
            # Calculate FPS every 30 frames
            if frame_count % 30 == 0:
                fps = 30 / (time.time() - fps_start_time)
                fps_start_time = time.time()

            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            gray_enhanced = clahe.apply(gray)
            gray_denoised = cv2.fastNlMeansDenoising(gray_enhanced, None, 10, 7, 21)

            # Detect faces
            faces = faceCascade.detectMultiScale(
                gray_denoised,
                scaleFactor=SCALE_FACTOR,
                minNeighbors=MIN_NEIGHBORS,
                minSize=MIN_SIZE,
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            # Process each detected face
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

            # Display system info
            cv2.putText(frame, f"FPS: {int(fps)}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(frame, f"Faces: {len(faces)}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(frame, "Press ENTER to exit", (10, frame.shape[0] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # Show frame
            cv2.imshow("Face Recognition System - Ultra Accurate Mode", frame)

            # Check for exit
            key = cv2.waitKey(1) & 0xFF
            if key == 13:  # ENTER key
                print("\n⚠ User requested exit via ENTER key")
                self.stop_flag = True # Signal the loop to stop
        
        # ============= CLEANUP =============
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
            filename = "attendance.csv"
            # create file with header if missing
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                with open(filename, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["StudentID", "Name", "RollNo", "Department", "Time", "Date", "Status"])

            # read existing lines to check duplication
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
        # Schedule this method to run again after 1000ms (1 second)
        self.time_lbl.after(1000, self.update_time)    
    
if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()