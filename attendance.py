from tkinter import*
from tkinter import ttk, filedialog
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
from datetime import datetime
from time import strftime
import csv


class Attendance:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Attendance Management System")

        # ================ Instance variables ===================
        self.mydata = []
        
        # ==========================variables======================== 
        self.var_atten_id=StringVar()
        self.var_atten_roll=StringVar()
        self.var_atten_name=StringVar()
        self.var_atten_dep=StringVar()
        self.var_atten_time=StringVar()
        self.var_atten_date=StringVar()
        self.var_atten_attendance=StringVar()
        
        try:
            img=Image.open(r"college images\image1.jpg")
            img=img.resize((800,200),Image.Resampling.LANCZOS)
            self.photoimg=ImageTk.PhotoImage(img)
            f_lbl=Label(self.root,image=self.photoimg)
            f_lbl.place(x=0,y=0,width=800,height=200)

            img1=Image.open(r"college images\image2.png")
            img1=img1.resize((800,200),Image.Resampling.LANCZOS)
            self.photoimg1=ImageTk.PhotoImage(img1)
            f_lbl1=Label(self.root,image=self.photoimg1)
            f_lbl1.place(x=800,y=0,width=800,height=200)
        except Exception:
            pass
        
        # bg image
        try:
            img3=Image.open(r"college images\background.jpg")
            img3=img3.resize((1530,710),Image.Resampling.LANCZOS)
            self.photoimg3=ImageTk.PhotoImage(img3)
            bg_img=Label(self.root,image=self.photoimg3)
            bg_img.place(x=0,y=200,width=1530,height=710)
        except Exception:
            bg_img=Frame(self.root, bg="lightgray")
            bg_img.place(x=0,y=200,width=1530,height=710)
        
        title_lbl=Label(bg_img,text="ATTENDANCE MANAGEMENT SYSTEM",font=("times new roman",35,"bold"),bg="skyblue",fg="red")
        title_lbl.place(x=0,y=0,width=1530,height=45)
        
        # ============================time=============================
        self.time_lbl = Label(title_lbl, font=("times new roman", 14, "bold"), bg="skyblue", fg="white")
        self.time_lbl.place(x=0, y=0, width=130, height=45) 
        self.update_time()

        
        main_frame=Frame(bg_img,bd=2,bg="white")
        main_frame.place(x=20,y=60,width=1480,height=580)
        
        # left label frame 
        Left_frame=LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Student Attendance Details",font=("times new roman",12,"bold"))
        Left_frame.place(x=10,y=10,width=730,height=560)
        
        try:
            img_left=Image.open(r"college images\image 6.png")
            img_left=img_left.resize((720,130),Image.Resampling.LANCZOS)
            self.photoimg_left=ImageTk.PhotoImage(img_left) 
            f_lbl=Label(Left_frame,image=self.photoimg_left)
            f_lbl.place(x=5,y=0,width=720,height=130)
        except Exception:
            pass
        
        left_inside_frame=Frame(Left_frame,bd=2,relief=RIDGE,bg="white")
        left_inside_frame.place(x=5,y=135,width=720,height=370)
        
        # label and entry
        # attendanceid 
        attendance_id=Label(left_inside_frame,text="Attendance ID:",font=("times new roman",13,"bold"),bg="white")
        attendance_id.grid(row=0,column=0,padx=10,pady=5,sticky=W)
        attendance_id_entry=ttk.Entry(left_inside_frame,width=20,textvariable=self.var_atten_id,font=("times new roman",13,"bold"))
        attendance_id_entry.grid(row=0,column=1,padx=10,pady=5,sticky=W)
        
        # name 
        name=Label(left_inside_frame,text="Name:",font=("times new roman",12,"bold"),bg="white")
        name.grid(row=0,column=2,padx=4,pady=8,sticky=W)
        name_entry=ttk.Entry(left_inside_frame,width=22,textvariable=self.var_atten_name,font=("times new roman",12,"bold"))
        name_entry.grid(row=0,column=3,pady=8,sticky=W)

        # roll 
        roll=Label(left_inside_frame,text="Regd No:",font=("times new roman",12,"bold"),bg="white")
        roll.grid(row=1,column=0)
        roll_entry=ttk.Entry(left_inside_frame,width=22,textvariable=self.var_atten_roll,font=("times new roman",12,"bold"))
        roll_entry.grid(row=1,column=1,pady=8)
        
        #department
        dep=Label(left_inside_frame,text="Department:",font=("times new roman",12,"bold"),bg="white")
        dep.grid(row=1,column=2)
        dep_entry=ttk.Entry(left_inside_frame,width=22,textvariable=self.var_atten_dep,font=("times new roman",12,"bold"))
        dep_entry.grid(row=1,column=3,pady=8)
        # date
        date=Label(left_inside_frame,text="Date:",font=("times new roman",12,"bold"),bg="white")
        date.grid(row=2,column=2)
        date_entry=ttk.Entry(left_inside_frame,width=22,textvariable=self.var_atten_date,font=("times new roman",12,"bold"))
        date_entry.grid(row=2,column=3,pady=8)
        # time
        time=Label(left_inside_frame,text="Time:",font=("times new roman",12,"bold"),bg="white")
        time.grid(row=2,column=0)
        time_entry=ttk.Entry(left_inside_frame,width=22,textvariable=self.var_atten_time,font=("times new roman",12,"bold"))
        time_entry.grid(row=2,column=1,pady=8)
        
        # attendance 
        attendance=Label(left_inside_frame,text="Attendance:",font=("times new roman",12,"bold"),bg="white")
        attendance.grid(row=3,column=0)
        
        self.atten_status=ttk.Combobox(left_inside_frame,width=20,textvariable=self.var_atten_attendance,font=("times new roman",12,"bold"),state="readonly")
        self.atten_status["values"]=("Status","Present","Absent")
        self.atten_status.current(0)
        self.atten_status.grid(row=3,column=1,pady=8)
        
        # button frame 
        btn_frame=Frame(left_inside_frame,bd=2,relief=RIDGE,bg="white")
        btn_frame.place(x=0,y=300,width=715,height=35)
        
        save_btn=Button(btn_frame,text="Import CSV",command=self.importCsv,width=17,font=("times new roman",13,"bold"),bg="blue",fg="white")
        save_btn.grid(row=0,column=0)
        
        update_btn=Button(btn_frame,text="Export CSV",command=self.exportCsv,width=17,font=("times new roman",13,"bold"),bg="blue",fg="white") 
        update_btn.grid(row=0,column=1)
        
        delete_btn=Button(btn_frame,text="Update",command=self.update_data,width=17,font=("times new roman",13,"bold"),bg="blue",fg="white")
        delete_btn.grid(row=0,column=2)
        
        reset_btn=Button(btn_frame,text="Reset",command=self.reset_data,width=17,font=("times new roman",13,"bold"),bg="blue",fg="white")
        reset_btn.grid(row=0,column=3)

        # right label frame 
        right_frame=LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Attendance Details",font=("times new roman",12,"bold"))
        right_frame.place(x=750,y=10,width=720,height=560)
        
        table_frame=Frame(right_frame,bd=2,relief=RIDGE,bg="white")
        table_frame.place(x=5,y=5,width=700,height=455)
        
        # ===============================scroll bar table=========================
        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)
        
        self.AttendanceReportTable=ttk.Treeview(table_frame,column=("id","roll","name","department","time","date","attendance"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)    
        
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        
        scroll_x.config(command=self.AttendanceReportTable.xview)
        scroll_y.config(command=self.AttendanceReportTable.yview)
        
        self.AttendanceReportTable.heading("id",text="Attendance ID")
        # === MODIFIED: Swapped the heading text for "roll" and "name" ===
        self.AttendanceReportTable.heading("roll",text="Name")
        self.AttendanceReportTable.heading("name",text="Regd No")
        # =============================================================
        self.AttendanceReportTable.heading("department",text="Department")
        self.AttendanceReportTable.heading("time",text="Time")
        self.AttendanceReportTable.heading("date",text="Date")
        self.AttendanceReportTable.heading("attendance",text="Attendance")
        
        self.AttendanceReportTable["show"]="headings"
        
        self.AttendanceReportTable.column("id",width=100)
        self.AttendanceReportTable.column("roll",width=100)
        self.AttendanceReportTable.column("name",width=100)
        self.AttendanceReportTable.column("department",width=100)
        self.AttendanceReportTable.column("time",width=100)
        self.AttendanceReportTable.column("date",width=100)
        self.AttendanceReportTable.column("attendance",width=100)
        
        self.AttendanceReportTable.pack(fill=BOTH,expand=1)
        self.AttendanceReportTable.bind("<ButtonRelease>",self.get_cursor)
        
        
    # ===============================================fetch data===========================
    def fetchData(self,rows):
        self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
        for i in rows:
            self.AttendanceReportTable.insert("",END,values=i)
            
    # ===============================================import csv===========================
    def importCsv(self):
        try:
            self.mydata.clear()
            fln=filedialog.askopenfilename(initialdir=os.getcwd(),title="Open CSV",filetypes=(("CSV File","*.csv"),("All File","*.*")),parent=self.root)
            if fln: 
                with open(fln, newline='') as myfile:
                    csvread=csv.reader(myfile,delimiter=",")
                    next(csvread, None)
                    for i in csvread:
                        self.mydata.append(i)
                self.fetchData(self.mydata)
        except Exception as es:
            messagebox.showerror("Error", f"Error reading CSV file: {str(es)}", parent=self.root)
            
    # export csv 
    def exportCsv(self):
        try:
            if len(self.mydata)<1:
                messagebox.showerror("No Data","No data found to export",parent=self.root)
                return False
            fln=filedialog.asksaveasfilename(initialdir=os.getcwd(),title="Open CSV",filetypes=(("CSV File","*.csv"),("All File","*.*")),parent=self.root)
            if fln:
                with open(fln,mode="w",newline="") as myfile:
                    exp_write=csv.writer(myfile,delimiter=",")
                    # Write header
                    exp_write.writerow(["Attendance ID","Roll No","Name","Department","Time","Date","Attendance"])
                    for i in self.mydata:
                        exp_write.writerow(i)
                messagebox.showinfo("Data Exported",f"Your data has been exported to {os.path.basename(fln)} successfully",parent=self.root)
        except Exception as es:
            messagebox.showerror("Error",f"Error exporting CSV file: {str(es)}",parent=self.root)
            
    def get_cursor(self,event=""):
        try:
            cursor_row=self.AttendanceReportTable.focus()
            content=self.AttendanceReportTable.item(cursor_row)
            row=content["values"]
            self.var_atten_id.set(row[0])
            self.var_atten_roll.set(row[1])
            self.var_atten_name.set(row[2])
            self.var_atten_dep.set(row[3])
            self.var_atten_time.set(row[4])
            self.var_atten_date.set(row[5])
            self.var_atten_attendance.set(row[6])
        except IndexError:
            pass # Handles case where an empty table is clicked
        
    def reset_data(self):
        self.var_atten_id.set("")
        self.var_atten_roll.set("")
        self.var_atten_name.set("")
        self.var_atten_dep.set("")
        self.var_atten_time.set("")
        self.var_atten_date.set("")
        self.var_atten_attendance.set("Status")
        
    def update_data(self):
        # Get data from entry fields
        id = self.var_atten_id.get()
        roll = self.var_atten_roll.get()
        name = self.var_atten_name.get()
        dep = self.var_atten_dep.get()
        time = self.var_atten_time.get()
        date = self.var_atten_date.get()
        attendance = self.var_atten_attendance.get()

        # Check if an item is selected
        selected_item = self.AttendanceReportTable.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a record from the table to update.", parent=self.root)
            return

        try:
            # Update the selected item in the Treeview (the UI)
            self.AttendanceReportTable.item(selected_item, values=(id, roll, name, dep, time, date, attendance))

            # Find the index of the row to update in the self.mydata list
            for index, row in enumerate(self.mydata):
                if row[0] == id:
                    self.mydata[index] = [id, roll, name, dep, time, date, attendance]
                    break
            
            messagebox.showinfo("Success", "Attendance record has been updated.", parent=self.root)
            
        except Exception as es:
            messagebox.showerror("Error", f"An error occurred during update: {str(es)}", parent=self.root)
        
        
        
    def update_time(self):
        """Fetches the current time and updates the time label."""
        string = strftime('%H:%M:%S %p')
        self.time_lbl.config(text=string)
        # Schedule this method to run again after 1000ms (1 second)
        self.time_lbl.after(1000, self.update_time)
        
        
if __name__ == "__main__":
    root=Tk()
    obj=Attendance(root)
    root.mainloop()