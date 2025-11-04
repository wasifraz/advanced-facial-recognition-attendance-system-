import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import * # Still needed for messagebox
from PIL import Image, ImageTk
from tkinter import messagebox
import cv2
import os
import numpy as np
from time import strftime
import threading  # To prevent app from freezing during training

class Train:
    def __init__(self, root):
        self.root = root
        
        # --- UI/UX CHANGE: Set window to open maximized ---
        self.root.state('zoomed')
        self.root.minsize(1280, 720) # Set a minimum size
        self.root.title("Face Recognition System - Model Training")

        # --- UI/UX CHANGE: Modern Header ---
        header_frame = ttk.Frame(self.root, bootstyle="primary")
        header_frame.pack(fill=X, side=TOP)
        
        title_lbl = ttk.Label(
            header_frame, 
            text="TRAIN PHOTO SAMPLE", 
            font=("Segoe UI", 24, "bold"), 
            bootstyle="primary-inverse"
        )
        title_lbl.pack(side=LEFT, padx=20, pady=10)
        
        self.time_lbl = ttk.Label(
            header_frame, 
            font=("Segoe UI", 16, "bold"), 
            bootstyle="primary-inverse"
        )
        self.time_lbl.pack(side=RIGHT, padx=20, pady=10)
        self.update_time()

        # --- UI/UX CHANGE: Main content frame for better organization ---
        main_content_frame = ttk.Frame(self.root)
        main_content_frame.pack(fill=BOTH, expand=YES)

        # --- RESTORED: Top Image ---
        try:
            # Dynamically resize for full width, fixed height
            screen_width = self.root.winfo_screenwidth()
            top_img_height = 360 # Fixed height for the image
            
            img_top = Image.open(r"college images\traindata.jpg")
            img_top = img_top.resize((screen_width, top_img_height), Image.Resampling.LANCZOS)
            self.photoimg_top = ImageTk.PhotoImage(img_top)

            f_lbl_top = ttk.Label(main_content_frame, image=self.photoimg_top)
            f_lbl_top.pack(fill=X, pady=(0, 10)) # Added some padding
        except Exception as e:
            print(f"Error loading top training image: {e}")
            f_lbl_top = ttk.Label(main_content_frame, text="Top Training Image Not Found", bootstyle="danger")
            f_lbl_top.pack(fill=X, pady=(0, 10))

        # Frame for controls (button, progress, status) to center them
        controls_frame = ttk.Frame(main_content_frame)
        controls_frame.pack(fill=X, expand=False, padx=20)

        # --- UI/UX CHANGE: Styled Button ---
        self.train_btn = ttk.Button(
            controls_frame, 
            text="🚀 TRAIN DATA", 
            command=self.start_training_thread,  # Call thread starter
            bootstyle="success-lg-outline",
            padding=15
        )
        self.train_btn.pack(pady=15, fill=X)
        
        # --- UI/UX CHANGE: Grouped Feedback Area ---
        feedback_frame = ttk.Labelframe(controls_frame, text="Training Progress", bootstyle="info")
        feedback_frame.pack(fill=X, expand=False)
        
        self.status_lbl = ttk.Label(
            feedback_frame, 
            text="Ready To Train Your Data", 
            font=("Segoe UI", 15, "bold"), 
            bootstyle="info",
            anchor=CENTER
        )
        self.status_lbl.pack(fill=X, padx=10, pady=(10, 5))
        
        self.progress = ttk.Progressbar(
            feedback_frame, 
            length=1000, # length here is more of a suggestion with fill=X
            mode='determinate', 
            bootstyle="success-striped"
        )
        self.progress.pack(fill=X, padx=10, pady=(5, 10))

        # --- RESTORED: Bottom Image (packed to fill remaining space) ---
        try:
            # Dynamically resize for full width, and scale height proportionally
            # Let's calculate remaining height for the bottom image if possible
            # Or just set a fixed height for simplicity with .pack
            bottom_img_height = 370 # Fixed height for the bottom image
            
            img_bottom = Image.open(r"college images\traindata2.jpg")
            img_bottom = img_bottom.resize((screen_width, bottom_img_height), Image.Resampling.LANCZOS)
            self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)
            
            f_lbl_bottom = ttk.Label(main_content_frame, image=self.photoimg_bottom)
            f_lbl_bottom.pack(fill=BOTH, expand=YES, pady=(10, 0)) # Pack to fill remaining space
        except Exception as e:
            print(f"Error loading bottom training image: {e}")
            f_lbl_bottom = ttk.Label(main_content_frame, text="Bottom Training Image Not Found", bootstyle="danger")
            f_lbl_bottom.pack(fill=BOTH, expand=YES, pady=(10, 0))

    # ==================== UX Functions for Threading ====================

    def start_training_thread(self):
        """Prevents the UI from freezing during training."""
        self.train_btn.config(state=DISABLED, text="⏳ TRAINING... PLEASE WAIT")
        self.update_status("Starting training thread...")
        
        # Run the intensive training logic in a separate thread
        train_thread = threading.Thread(target=self.Train_Classifier_Fixed, daemon=True)
        train_thread.start()

    def update_status(self, message):
        """Thread-safe way to update the status label."""
        # Use .after() to schedule the UI update on the main thread
        self.root.after(0, lambda: self.status_lbl.config(text=message))

    def update_progress(self, value):
        """Thread-safe way to update the progress bar."""
        self.root.after(0, lambda: self.progress.config(value=value))

    def show_message(self, type, title, message):
        """Thread-safe way to show message boxes."""
        if type == "error":
            self.root.after(0, lambda: messagebox.showerror(title, message, parent=self.root))
        else:
            self.root.after(0, lambda: messagebox.showinfo(title, message, parent=self.root))

    def reset_ui_on_finish(self):
        """Thread-safe way to re-enable the button and reset progress."""
        self.root.after(0, lambda: self.train_btn.config(state=NORMAL, text="🚀 TRAIN DATA"))
        self.root.after(0, lambda: self.progress.config(value=0))

    # ==================== Core Training Logic (UNCHANGED) ====================
    # --- Logic is identical, but UI calls (e.g., update_status) are now thread-safe ---

    def Train_Classifier_Fixed(self):
        """Fixed version that handles OpenCV compatibility issues"""
        
        try:
            self.update_status("Checking data directory...")
            
            data_dir = "data"
            if not os.path.exists(data_dir):
                self.show_message("error", "Error", "Data directory not found!\n\nSteps:\n1. Use Student module\n2. Take photo samples\n3. Return here to train")
                return

            file_list = [f for f in os.listdir(data_dir) if f.endswith(('.jpg', '.jpeg', '.png')) and 'user.' in f]
            
            if len(file_list) == 0:
                self.show_message("error", "Error", "No training images found!\n\nLooking for files like: user.45.1.jpg\n\nPlease take photo samples first.")
                return

            print("="*60)
            print(f"FIXED TRAINING STARTED")
            print("="*60)
            print(f"Found {len(file_list)} training images")
            
            faces = []
            ids = []
            
            self.root.after(0, lambda: self.progress.config(maximum=len(file_list)))
            self.update_progress(0)
            
            valid_images = 0
            
            for idx, filename in enumerate(file_list):
                try:
                    self.update_progress(idx + 1)
                    self.update_status(f"Processing {idx+1}/{len(file_list)}: {filename}")
                    
                    image_path = os.path.join(data_dir, filename)
                    
                    parts = filename.split('.')
                    if len(parts) < 3 or parts[0] != 'user':
                        print(f"Skipping {filename} - wrong format")
                        continue
                    
                    try:
                        student_id = int(parts[1])
                    except ValueError:
                        print(f"Skipping {filename} - invalid ID")
                        continue

                    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                    
                    if img is None:
                        print(f"Error: Could not read {filename}")
                        continue

                    img = cv2.resize(img, (100, 100))
                    img = cv2.equalizeHist(img)
                    img = np.array(img, dtype=np.uint8)
                    
                    faces.append(img)
                    ids.append(student_id)
                    valid_images += 1
                    
                    print(f"✓ Processed: {filename} -> ID: {student_id}")
                    
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
                    continue

            if len(faces) == 0:
                self.show_message("error", "Error", "No valid faces processed!\n\nCheck:\n1. Images exist in data folder\n2. Filenames: user.ID.number.jpg\n3. Images are readable")
                return

            self.update_status(f"Training model with {len(faces)} faces...")
            print(f"\nTraining with {valid_images} valid images...")

            faces = np.array(faces)
            ids = np.array(ids, dtype=np.int32)

            print(f"Face array shape: {faces.shape}")
            print(f"IDs array shape: {ids.shape}")
            print(f"Unique IDs: {np.unique(ids)}")

            try:
                clf = cv2.face.LBPHFaceRecognizer_create(
                    radius=1,
                    neighbors=8,
                    grid_x=8,
                    grid_y=8
                )
                
                print("✓ LBPH Recognizer created")
                
                clf.train(faces, ids)
                print("✓ Training completed")
                
                classifier_dir = "classifier"
                if not os.path.exists(classifier_dir):
                    os.makedirs(classifier_dir)
                    print("✓ Created classifier directory")
                
                model_path = os.path.abspath(os.path.join(classifier_dir, "classifier.xml"))
                
                if os.path.exists(model_path):
                    os.remove(model_path)
                    print("✓ Removed old classifier file")
                
                clf.write(model_path)
                
                if os.path.exists(model_path):
                    file_size = os.path.getsize(model_path)
                    print(f"✓ Model saved: {model_path}")
                    print(f"✓ File size: {file_size} bytes")
                    
                    if file_size < 500:
                        raise Exception(f"Model file too small ({file_size} bytes) - likely corrupted")
                    
                    test_clf = cv2.face.LBPHFaceRecognizer_create()
                    test_clf.read(model_path)
                    print("✓ Model verification successful - file is readable")
                    
                    unique_students = len(np.unique(ids))
                    success_msg = (
                        f"Training Successful!\n\n"
                        f"✅ Images processed: {valid_images}\n"
                        f"✅ Students trained: {unique_students}\n" 
                        f"✅ Student IDs: {list(np.unique(ids))}\n"
                        f"✅ Model size: {file_size} bytes\n"
                        f"✅ Saved to: classifier/classifier.xml\n\n"
                        f"Ready for face recognition!"
                    )
                    
                    self.show_message("info", "Training Complete", success_msg)
                    self.update_status("Training completed successfully!")
                    
                    print("="*60)
                    print("TRAINING COMPLETED SUCCESSFULLY")
                    print("="*60)
                    
                else:
                    raise Exception("Model file was not created")
                    
            except Exception as e:
                error_msg = f"Training failed: {str(e)}\n\nSolutions:\n1. Restart Python\n2. Check opencv-contrib-python version\n3. Ensure images are valid\n4. Try taking new photos"
                self.show_message("error", "Training Failed", error_msg)
                print(f"❌ Training error: {e}")
            
        except Exception as e:
            # Catch any unexpected errors in the main function
            self.show_message("error", "Fatal Error", f"An unexpected error occurred: {e}")
        
        finally:
            self.reset_ui_on_finish()

    # ==================== Time Update Function (UNCHANGED) ====================
    def update_time(self):
        """Fetches the current time and updates the time label."""
        string = strftime('%H:%M:%S %p')
        self.time_lbl.config(text=string)
        self.time_lbl.after(1000, self.update_time)

if __name__ == "__main__":
    # --- UI/UX CHANGE: Use ttk.Window with a theme ---
    root = ttk.Window(themename="vapor") 
    obj = Train(root)
    root.mainloop()