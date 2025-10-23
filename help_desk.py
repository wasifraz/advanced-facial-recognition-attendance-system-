from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from time import strftime

class HelpDesk:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Help Desk")

        title_lbl=Label(self.root,text="HELP DESK",font=("times new roman",40,"bold"),bg="skyblue",fg="red")
        title_lbl.place(x=0,y=0,width=1530,height=60)
        
        # ============================time=============================
        self.time_lbl = Label(title_lbl, font=("times new roman", 15, "bold"), bg="skyblue", fg="white")
        self.time_lbl.place(x=0, y=0, width=130, height=45) 
        self.update_time()
        
        img=Image.open(r"college images\help desk img.png")
        img=img.resize((1530,720),Image.Resampling.LANCZOS)
        self.photoimg=ImageTk.PhotoImage(img)


        f_lbl=Label(self.root,image=self.photoimg)
        f_lbl.place(x=0,y=60,width=1530,height=700)          


    def update_time(self):
        """Fetches the current time and updates the time label."""
        string = strftime('%H:%M:%S %p')
        self.time_lbl.config(text=string)
        # Schedule this method to run again after 1000ms (1 second)
        self.time_lbl.after(1000, self.update_time)
        
        
        
if __name__ == "__main__":
    root=Tk()
    obj=HelpDesk(root)
    root.mainloop()