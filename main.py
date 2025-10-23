from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from student import Student
from train import Train
from face_recognition import Face_Recognition
import os
from time import strftime
from datetime import datetime
from tkinter import messagebox
from attendance import Attendance
from chatbot import UltimateGroqChatbot
from help_desk import HelpDesk
from tkinter import messagebox


class Face_Recognition_System:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        
        

        # first image
        img=Image.open(r"college images\image1.jpg")
        img=img.resize((500,130),Image.Resampling.LANCZOS)
        self.photoimg=ImageTk.PhotoImage(img)


        f_lbl=Label(self.root,image=self.photoimg)
        f_lbl.place(x=0,y=0,width=500,height=130)   


        # secong image
        img1=Image.open(r"college images\image2.png")
        img1=img1.resize((500,130),Image.Resampling.LANCZOS)
        self.photoimg1=ImageTk.PhotoImage(img1)


        f_lbl=Label(self.root,image=self.photoimg1)
        f_lbl.place(x=500,y=0,width=500,height=130)

        # third image
        img2=Image.open(r"college images\image3.jpg")
        img2=img2.resize((600,130),Image.Resampling.LANCZOS)
        self.photoimg2=ImageTk.PhotoImage(img2)

        f_lbl=Label(self.root,image=self.photoimg2)
        f_lbl.place(x=1000,y=0,width=550,height=130)

        # bg image
        img3=Image.open(r"college images\background.jpg")
        img3=img3.resize((1530,710),Image.Resampling.LANCZOS)
        self.photoimg3=ImageTk.PhotoImage(img3)

        bg_img=Label(self.root,image=self.photoimg3)
        bg_img.place(x=0,y=130,width=1530,height=710)

        title_lbl=Label(bg_img,text="FACE RECOGNITION ATTENDANCE SYSTEM SOFTWARE",font=("times new roman",30,"bold"),bg="skyblue",fg="red")
        title_lbl.place(x=0,y=0,width=1530,height=45)
        
        # ============================time=============================
        self.time_lbl = Label(title_lbl, font=("times new roman", 14, "bold"), bg="skyblue", fg="white")
        self.time_lbl.place(x=0, y=0, width=130, height=45) 
        self.update_time()

        # student button
        img4=Image.open(r"college images\students.png")
        img4=img4.resize((220,220),Image.Resampling.LANCZOS)
        self.photoimg4=ImageTk.PhotoImage(img4)

        b1=Button(bg_img,image=self.photoimg4,command=self.student_details,cursor="hand2")
        b1.place(x=200,y=100,width=220,height=220)

        b1=Button(bg_img,text="Student Details",command=self.student_details,cursor="hand2",font=("times new roman",15,"bold"),bg="lightblue",fg="navy")
        b1.place(x=200,y=300,width=220,height=40)

        #face recognition button
        img5=Image.open(r"college images\face_dectected.png")
        img5=img5.resize((220,220),Image.Resampling.LANCZOS)
        self.photoimg5=ImageTk.PhotoImage(img5)

        b1=Button(bg_img,image=self.photoimg5,command=self.face_data,cursor="hand2")
        b1.place(x=500,y=100,width=220,height=220)

        b1=Button(bg_img,text="Face Detector",cursor="hand2",command=self.face_data,font=("times new roman",15,"bold"),bg="lightblue",fg="navy")
        b1.place(x=500,y=300,width=220,height=40)

        # attendance button
        img6=Image.open(r"college images\generated-image.png")
        img6=img6.resize((220,220),Image.Resampling.LANCZOS)
        self.photoimg6=ImageTk.PhotoImage(img6)

        b1=Button(bg_img,image=self.photoimg6,cursor="hand2",command=self.attendance)
        b1.place(x=800,y=100,width=220,height=220)

        b1=Button(bg_img,text="Attendance",cursor="hand2",command=self.attendance,font=("times new roman",15,"bold"),bg="lightblue",fg="navy")
        b1.place(x=800,y=300,width=220,height=40)

        #Chatbot button
        img7=Image.open(r"college images\image2.png")
        img7=img7.resize((220,220),Image.Resampling.LANCZOS)
        self.photoimg7=ImageTk.PhotoImage(img7)

        b1=Button(bg_img,image=self.photoimg7,cursor="hand2",command=self.chatbot)
        b1.place(x=1100,y=100,width=220,height=220)

        b1=Button(bg_img,text="Chatbot",cursor="hand2",command=self.chatbot,font=("times new roman",15,"bold"),bg="lightblue",fg="navy")
        b1.place(x=1100,y=300,width=220,height=40)

        # train button
        img8=Image.open(r"college images\traindata.png")
        img8=img8.resize((220,220),Image.Resampling.LANCZOS)
        self.photoimg8=ImageTk.PhotoImage(img8)

        b1=Button(bg_img,image=self.photoimg8,cursor="hand2",command=self.train_data)
        b1.place(x=200,y=380,width=220,height=220)

        b1=Button(bg_img,text="Train Data",cursor="hand2",command=self.train_data,font=("times new roman",15,"bold"),bg="lightblue",fg="navy")
        b1.place(x=200,y=580,width=220,height=40)

        # photo button
        img9=Image.open(r"college images\photos.jpg")
        img9=img9.resize((220,220),Image.Resampling.LANCZOS)
        self.photoimg9=ImageTk.PhotoImage(img9)

        b1=Button(bg_img,image=self.photoimg9,cursor="hand2",command=self.open_img)
        b1.place(x=500,y=380,width=220,height=220)

        b1=Button(bg_img,text="Photos",cursor="hand2",command=self.open_img,font=("times new roman",15,"bold"),bg="lightblue",fg="navy")
        b1.place(x=500,y=580,width=220,height=40)

        # Help desk button
        img10=Image.open(r"college images\help desk.png")
        img10=img10.resize((220,220),Image.Resampling.LANCZOS)
        self.photoimg10=ImageTk.PhotoImage(img10)

        b1=Button(bg_img,image=self.photoimg10,cursor="hand2",command=self.help_desk)   
        b1.place(x=800,y=380,width=220,height=220)

        b1=Button(bg_img,text="Help Desk",cursor="hand2",command=self.help_desk,font=("times new roman",15,"bold"),bg="lightblue",fg="navy")
        b1.place(x=800,y=580,width=220,height=40)

        # exit button
        img11=Image.open(r"college images\exit.png")
        img11=img11.resize((220,220),Image.Resampling.LANCZOS)
        self.photoimg11=ImageTk.PhotoImage(img11)

        b1=Button(bg_img,image=self.photoimg11,cursor="hand2",command=self.exit)
        b1.place(x=1100,y=380,width=220,height=220)

        b1=Button(bg_img,text="Exit",cursor="hand2",command=self.exit,font=("times new roman",15,"bold"),bg="lightblue",fg="navy")
        b1.place(x=1100,y=580,width=220,height=40)

    def open_img(self):
        os.startfile("data")
        
    def exit(self):
        self.exit=messagebox.askyesno("Face Recognition","Are you sure to exit this project",parent=self.root)
        if self.exit>0:
            self.root.destroy()
        else:
            return
            
# ============================Function buttons=============================
    
    def student_details(self):
        self.new_window=Toplevel(self.root)
        self.app=Student(self.new_window)

    def train_data(self):
        self.new_window=Toplevel(self.root)
        self.app=Train(self.new_window)
        
        
    def face_data(self):
        self.new_window=Toplevel(self.root)
        self.app=Face_Recognition(self.new_window)
        
    def attendance(self):
        self.new_window=Toplevel(self.root)
        self.app=Attendance(self.new_window)
        
    def help_desk(self):
        self.new_window=Toplevel(self.root)
        self.app=HelpDesk(self.new_window)
    
    def chatbot(self):
        self.new_window=Toplevel(self.root)
        self.app=UltimateGroqChatbot(self.new_window)
        
    def update_time(self):
        """Fetches the current time and updates the time label."""
        string = strftime('%H:%M:%S %p')
        self.time_lbl.config(text=string)
        # Schedule this method to run again after 1000ms (1 second)
        self.time_lbl.after(1000, self.update_time)
        
        
if __name__ == "__main__":
    root=Tk()
    obj=Face_Recognition_System(root)
    root.mainloop()
    