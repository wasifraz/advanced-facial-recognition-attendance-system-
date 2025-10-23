from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import cv2
import os
import numpy as np
from time import strftime


class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        title_lbl = Label(self.root, text="TRAIN PHOTO SAMPLE", 
                        font=("times new roman", 35, "bold"), 
                        bg="skyblue", fg="red")
        title_lbl.place(x=0, y=0, width=1530, height=45)
        # ============================time=============================
        self.time_lbl = Label(title_lbl, font=("times new roman", 14, "bold"), bg="skyblue", fg="white")
        self.time_lbl.place(x=0, y=0, width=130, height=45) 
        self.update_time()

        # Progress bar
        self.progress = ttk.Progressbar(self.root, length=1500, mode='determinate')
        self.progress.place(x=15, y=350, width=1500, height=20)
        
        # top img
        
        img=Image.open(r"college images\traindata.jpg")
        img=img.resize((1530,350),Image.Resampling.LANCZOS)
        self.photoimg=ImageTk.PhotoImage(img)

        f_lbl = Label(self.root, image=self.photoimg)
        f_lbl.place(x=0, y=45, width=1530, height=300)
        
        b1 = Button(self.root, text="TRAIN DATA", cursor="hand2", 
                command=self.Train_Classifier_Fixed,
                font=("times new roman", 24, "bold"), 
                bg="green", fg="white")
        b1.place(x=0, y=380, width=1530, height=60)
        
        #bottom
        img1=Image.open(r"college images\traindata2.jpg")
        img1=img1.resize((1530,350),Image.Resampling.LANCZOS)
        self.photoimg1=ImageTk.PhotoImage(img1)
        f_lbl = Label(self.root, image=self.photoimg1)
        f_lbl.place(x=0, y=440, width=1530, height=345)
        
        # Status
        self.status_lbl = Label(self.root, text="Ready To Train Your Data", 
                            font=("times new roman", 12, "bold"), 
                            bg="white", fg="green")
        self.status_lbl.place(x=0, y=445, width=1530, height=25)

    def update_status(self, message):
        self.status_lbl.config(text=message)
        self.root.update()

    def Train_Classifier_Fixed(self):
        """Fixed version that handles OpenCV compatibility issues"""
        
        self.update_status("Checking data directory...")
        
        # Check data directory
        data_dir = "data"
        if not os.path.exists(data_dir):
            messagebox.showerror("Error", "Data directory not found!\n\nSteps:\n1. Use Student module\n2. Take photo samples\n3. Return here to train")
            return

        # Get image files
        file_list = [f for f in os.listdir(data_dir) if f.endswith(('.jpg', '.jpeg', '.png')) and 'user.' in f]
        
        if len(file_list) == 0:
            messagebox.showerror("Error", "No training images found!\n\nLooking for files like: user.45.1.jpg\n\nPlease take photo samples first.")
            return

        print("="*60)
        print(f"FIXED TRAINING STARTED")
        print("="*60)
        print(f"Found {len(file_list)} training images")
        
        faces = []
        ids = []
        
        # Setup progress
        self.progress['maximum'] = len(file_list)
        self.progress['value'] = 0
        
        valid_images = 0
        
        for idx, filename in enumerate(file_list):
            try:
                # Update progress
                self.progress['value'] = idx + 1
                self.update_status(f"Processing {idx+1}/{len(file_list)}: {filename}")
                
                image_path = os.path.join(data_dir, filename)
                
                # Parse filename: user.ID.number.jpg
                parts = filename.split('.')
                if len(parts) < 3 or parts[0] != 'user':
                    print(f"Skipping {filename} - wrong format")
                    continue
                
                try:
                    student_id = int(parts[1])
                except ValueError:
                    print(f"Skipping {filename} - invalid ID")
                    continue

                # Load and preprocess image
                img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                
                if img is None:
                    print(f"Error: Could not read {filename}")
                    continue

                # CRITICAL FIX: Resize to consistent size
                img = cv2.resize(img, (100, 100))
                
                # Simple preprocessing (avoid complex operations that cause corruption)
                img = cv2.equalizeHist(img)
                
                # Ensure proper data type
                img = np.array(img, dtype=np.uint8)
                
                faces.append(img)
                ids.append(student_id)
                valid_images += 1
                
                print(f"✓ Processed: {filename} -> ID: {student_id}")
                
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue

        if len(faces) == 0:
            messagebox.showerror("Error", "No valid faces processed!\n\nCheck:\n1. Images exist in data folder\n2. Filenames: user.ID.number.jpg\n3. Images are readable")
            return

        self.update_status(f"Training model with {len(faces)} faces...")
        print(f"\nTraining with {valid_images} valid images...")

        # Convert to numpy arrays
        faces = np.array(faces)
        ids = np.array(ids, dtype=np.int32)

        print(f"Face array shape: {faces.shape}")
        print(f"IDs array shape: {ids.shape}")
        print(f"Unique IDs: {np.unique(ids)}")

        try:
            # CRITICAL FIX: Use basic LBPH parameters to avoid corruption
            clf = cv2.face.LBPHFaceRecognizer_create(
                radius=1,       # Basic radius
                neighbors=8,    # Basic neighbors  
                grid_x=8,       # Standard
                grid_y=8        # Standard
            )
            
            print("✓ LBPH Recognizer created")
            
            # Train the model
            clf.train(faces, ids)
            print("✓ Training completed")
            
            # Create classifier directory
            classifier_dir = "classifier"
            if not os.path.exists(classifier_dir):
                os.makedirs(classifier_dir)
                print("✓ Created classifier directory")
            
            # CRITICAL FIX: Use absolute path and ensure directory is writable
            model_path = os.path.abspath(os.path.join(classifier_dir, "classifier.xml"))
            
            # Delete any existing corrupted file first
            if os.path.exists(model_path):
                os.remove(model_path)
                print("✓ Removed old classifier file")
            
            # Save the model
            clf.write(model_path)
            
            # CRITICAL VERIFICATION: Check if file was created properly
            if os.path.exists(model_path):
                file_size = os.path.getsize(model_path)
                print(f"✓ Model saved: {model_path}")
                print(f"✓ File size: {file_size} bytes")
                
                if file_size < 500:
                    raise Exception(f"Model file too small ({file_size} bytes) - likely corrupted")
                
                # TEST: Try to load the saved model to verify it's not corrupted
                test_clf = cv2.face.LBPHFaceRecognizer_create()
                test_clf.read(model_path)
                print("✓ Model verification successful - file is readable")
                
                # Success!
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
                
                messagebox.showinfo("Training Complete", success_msg)
                self.update_status("Training completed successfully!")
                
                print("="*60)
                print("TRAINING COMPLETED SUCCESSFULLY")
                print("="*60)
                
            else:
                raise Exception("Model file was not created")
                
        except Exception as e:
            error_msg = f"Training failed: {str(e)}\n\nSolutions:\n1. Restart Python\n2. Check opencv-contrib-python version\n3. Ensure images are valid\n4. Try taking new photos"
            messagebox.showerror("Training Failed", error_msg)
            print(f"❌ Training error: {e}")
        
        # Reset progress
        self.progress['value'] = 0

    def update_time(self):
        """Fetches the current time and updates the time label."""
        string = strftime('%H:%M:%S %p')
        self.time_lbl.config(text=string)
        # Schedule this method to run again after 1000ms (1 second)
        self.time_lbl.after(1000, self.update_time)

if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()