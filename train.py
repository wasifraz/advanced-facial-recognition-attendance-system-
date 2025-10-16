from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import cv2
import os
import numpy as np

class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        # Title Label
        title_lbl = Label(self.root, text="TRAIN DATA SET", 
                        font=("times new roman", 35, "bold"), 
                        bg="white", fg="blue")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        # TOP IMAGE - with error handling
        try:
            img_Top = Image.open(r"college images\traindata.jpg")
            img_Top = img_Top.resize((1530, 325), Image.Resampling.LANCZOS)
            self.photoimg_Top = ImageTk.PhotoImage(img_Top)
            f_lbl = Label(self.root, image=self.photoimg_Top)
            f_lbl.place(x=0, y=55, width=1530, height=325)
        except Exception as e:
            print(f"Could not load top image: {e}")

        # Button
        b1 = Button(self.root, text="TRAIN DATA", cursor="hand2", 
                command=self.Train_Classifier,
                font=("times new roman", 30, "bold"), 
                bg="blue", fg="white")
        b1.place(x=0, y=380, width=1530, height=60)

        # BOTTOM IMAGE - with error handling
        try:
            img_Bottom = Image.open(r"college images\traindata2.jpg")
            img_Bottom = img_Bottom.resize((1530, 325), Image.Resampling.LANCZOS)
            self.photoimg_Bottom = ImageTk.PhotoImage(img_Bottom)
            f_lbl = Label(self.root, image=self.photoimg_Bottom)
            f_lbl.place(x=0, y=440, width=1530, height=325)
        except Exception as e:
            print(f"Could not load bottom image: {e}")

    def Train_Classifier(self):
        # Check if data directory exists
        data_dir = "data"
        if not os.path.exists(data_dir):
            messagebox.showerror("Error", "Data directory not found! Please create a 'data' folder with training images.")
            return

        # Get all image files from data directory
        file_list = os.listdir(data_dir)
        if len(file_list) == 0:
            messagebox.showerror("Error", "No training images found in 'data' folder!")
            return

        path = [os.path.join(data_dir, file) for file in file_list if file.endswith(('.jpg', '.jpeg', '.png'))]
        
        if len(path) == 0:
            messagebox.showerror("Error", "No valid image files found in 'data' folder!")
            return

        faces = []
        ids = []

        print(f"Processing {len(path)} images...")
        
        for image_path in path:
            try:
                # Open and convert image to grayscale
                img = Image.open(image_path).convert('L')
                image_np = np.array(img, 'uint8')
                
                # Extract ID from filename (format: name.ID.number.jpg)
                filename = os.path.split(image_path)[1]
                parts = filename.split('.')
                
                if len(parts) >= 2:
                    try:
                        id = int(parts[1])
                    except ValueError:
                        print(f"Skipping {filename} - invalid ID format")
                        continue
                else:
                    print(f"Skipping {filename} - incorrect filename format")
                    continue

                faces.append(image_np)
                ids.append(id)
                
                # Display training progress
                cv2.imshow("Training", image_np)
                cv2.waitKey(1)
                
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
                continue

        cv2.destroyAllWindows()

        if len(faces) == 0:
            messagebox.showerror("Error", "No faces could be processed! Check image filenames and format.")
            return

        # Convert ids to numpy array
        ids = np.array(ids)

        print(f"Training with {len(faces)} face samples...")

        try:
            # Create LBPH Face Recognizer
            clf = cv2.face.LBPHFaceRecognizer_create()
            
            # Train the classifier
            clf.train(faces, ids)
            
            # Create classifier directory if it doesn't exist
            if not os.path.exists("classifier"):
                os.makedirs("classifier")
            
            # Save the trained model
            clf.write("classifier/classifier.xml")
            
            messagebox.showinfo("Result", f"Training completed successfully!\n{len(faces)} images processed.\nModel saved to classifier/classifier.xml")
            print("Training completed successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Training failed: {str(e)}\n\nMake sure opencv-contrib-python is installed:\npip install opencv-contrib-python")
            print(f"Training error: {e}")

if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()
