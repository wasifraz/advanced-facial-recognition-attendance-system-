from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np

class Train:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")


        title_lbl=Label(self.root,text="TRAIN DATA SET",font=("times new roman",35,"bold"),bg="white",fg="blue")
        title_lbl.place(x=0,y=0,width=1530,height=45)

        #TOP IMAGE
        img_Top=Image.open(r"college images\traindata.jpg")
        img_Top=img_Top.resize((1530,325),Image.Resampling.LANCZOS)
        self.photoimg_Top=ImageTk.PhotoImage(img_Top)
        
        f_lbl=Label(self.root,image=self.photoimg_Top)
        f_lbl.place(x=0,y=55,width=1530,height=325)

        # Button
        b1=Button(self.root,text="TRAIN DATA",cursor="hand2",command=self.Train_Classifier,font=("times new roman",30,"bold"),bg="blue",fg="white")
        b1.place(x=0,y=380,width=1530,height=60)

        #BOTTOM IMAGE
        img_Bottom=Image.open(r"college images\traindata2.jpg")
        img_Bottom=img_Bottom.resize((1530,325),Image.Resampling.LANCZOS)
        self.photoimg_Bottom=ImageTk.PhotoImage(img_Bottom)
        
        f_lbl=Label(self.root,image=self.photoimg_Bottom)
        f_lbl.place(x=0,y=440,width=1530,height=325)


    def Train_Classifier(self):
        data_dir=("data")
        path=[os.path.join(data_dir,file) for file in os.listdir(data_dir)]

        faces=[]
        ids=[]

        for image in path:
            img=Image.open(image).convert('L') #Grayscale img
            image_np=np.array(img,'uint8')
            id=int(os.path.split(image)[1].split('.')[1])

            faces.append(image_np)
            ids.append(id)
            cv2.imshow("Training",image_np)
            cv2.waitKey(1)==13
        ids=np.array(ids)

        # Training the classifier and save
        clf=cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces,ids)
        clf.write("classifier.xml")
        cv2.destroyAllWindows()
        messagebox.showinfo("Result","Training datasets completed!!")
        



if __name__ == "__main__":
    root=Tk()
    obj=Train(root)
    root.mainloop()