from tkinter import*
from tkinter import ttk 
from PIL import Image,ImageTk
from tkinter import messagebox #imported for messagebox
import mysql.connector #imported for database                            

class Student:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")


        #Variables
        self.var_dep=StringVar()
        self.var_course=StringVar()
        self.var_year=StringVar()
        self.var_sem=StringVar()
        self.var_std_id=StringVar()
        self.var_std_name=StringVar()
        self.var_div=StringVar()
        self.var_roll=StringVar()
        self.var_group=StringVar()
        self.var_gender=StringVar()
        self.var_dob=StringVar()
        self.var_email=StringVar()
        self.var_phone=StringVar()
        self.var_address=StringVar()
        self.var_proctor=StringVar()
        self.var_photo_sample=StringVar()



# first image
        img=Image.open("college image\\image1.jpg")
        img=img.resize((530,130),Image.Resampling.LANCZOS)
        self.photoimg=ImageTk.PhotoImage(img)


        f_lbl=Label(self.root,image=self.photoimg)
        f_lbl.place(x=0,y=0,width=500,height=130)
        
        
        # second image     
        img1=Image.open("college image\\image2.png")
        img1=img1.resize((540,130),Image.Resampling.LANCZOS)
        self.photoimg1=ImageTk.PhotoImage(img1)


        f_lbl=Label(self.root,image=self.photoimg1)
        f_lbl.place(x=500,y=0,width=500,height=130)

        # third image
        img2=Image.open("college image\\image3.jpg")
        img2=img2.resize((600,130),Image.Resampling.LANCZOS)
        self.photoimg2=ImageTk.PhotoImage(img2)

        f_lbl=Label(self.root,image=self.photoimg2)
        f_lbl.place(x=1000,y=0,width=550,height=130)
        
        # bg image
        img3=Image.open("college image\\background.jpg")
        img3=img3.resize((1530,710),Image.Resampling.LANCZOS)
        self.photoimg3=ImageTk.PhotoImage(img3)
        
        bg_img=Label(self.root,image=self.photoimg3)
        bg_img.place(x=0,y=130,width=1530,height=710)

        title_lbl=Label(bg_img,text="STUDENT MANAGEMENT SYSTEM",font=("times new roman",35,"bold"),bg="white",fg="green")
        title_lbl.place(x=0,y=0,width=1530,height=45)


        main_frame=Frame(bg_img,bd=2,bg="white")
        main_frame.place(x=20,y=55,width=1480,height=600)

        #left label frame
        Left_Frame=LabelFrame(main_frame,bd=2,bg='white',relief='ridge',text="Student Information",font=('times new roman',12,"bold"))
        Left_Frame.place(x=10,y=10,width=730,height=580)

        img_Left=Image.open("college image\\background.jpg")
        img_Left=img_Left.resize((1530,710),Image.Resampling.LANCZOS)
        self.photoimg_Left=ImageTk.PhotoImage(img_Left)

        bg_img=Label(Left_Frame,image=self.photoimg_Left)
        bg_img.place(x=5,y=0,width=720,height=130)

        #Current Course Details
        Current_Course_Frame=LabelFrame(Left_Frame,bd=2,bg='white',relief='ridge',text="Current Course",font=('times new roman',12,"bold"))
        Current_Course_Frame.place(x=5,y=135,width=720,height=115)

        #department
        dept_label=Label(Current_Course_Frame,text="Department",bg="white",font=("times new roman",12,"bold"))
        dept_label.grid(row=0,column=0,padx=10)

        dept_combo=ttk.Combobox(Current_Course_Frame,textvariable=self.var_dep,font=("times new roman",13,"bold"),width=20,state="readonly")
        dept_combo["values"]=("Select Department","ECE","CSE","EE","CIVIL","MECH","ENTC")
        dept_combo.current(0)
        dept_combo.grid(row=0,column=1,padx=2,pady=10,sticky=W)
        
        #group
        group_label=Label(Current_Course_Frame,text="Group",bg="white",font=("times new roman",13,"bold"))
        group_label.grid(row=0,column=2,padx=10,sticky=W)

        group_combo=ttk.Combobox(Current_Course_Frame,textvariable=self.var_group,font=("times new roman",13,"bold"),width=20,state="readonly")
        group_combo["values"]=("Select Group","1","2")
        group_combo.current(0)
        group_combo.grid(row=0,column=3,padx=2,pady=10,sticky=W)

        #Year
        Year_label=Label(Current_Course_Frame,text="Year",bg="white",font=("times new roman",13,"bold"))
        Year_label.grid(row=1,column=0,padx=10,sticky=W)

        Year_combo=ttk.Combobox(Current_Course_Frame,textvariable=self.var_year,font=("times new roman",13,"bold"),width=20,state="readonly")
        Year_combo["values"]=("Select Year","First Year","Second Year","Third Year","Fourth Year")
        Year_combo.current(0)
        Year_combo.grid(row=1,column=1,padx=2,pady=10,sticky=W)
        
        #semester
        Sem_label=Label(Current_Course_Frame,text="Semester",bg="white",font=("times new roman",13,"bold"))
        Sem_label.grid(row=1,column=2,padx=10,sticky=W)

        Sem_combo=ttk.Combobox(Current_Course_Frame,textvariable=self.var_sem,font=("times new roman",13,"bold"),width=20,state="readonly")
        Sem_combo["values"]=("Select Semester","1st","2nd","3rd","4th","5th","6th","7th","8th")
        Sem_combo.current(0)
        Sem_combo.grid(row=1,column=3,padx=2,pady=10,sticky=W)

        #class student information
        Class_Info_Frame=LabelFrame(Left_Frame,bd=2,bg="white",relief='ridge',text="Class Student Information",font=('times new roman',12,"bold"))
        Class_Info_Frame.place(x=5,y=250,width=720,height=300)

        #StudentId
        StudentID_label=Label(Class_Info_Frame,text="Registration Number:",bg="white",font=("times new roman",13,"bold"))
        StudentID_label.grid(row=0,column=0,padx=10,pady=5,sticky=W)

        StudentID_entry=ttk.Entry(Class_Info_Frame,textvariable=self.var_std_id,font=('times new roman',12,"bold"),width=21)
        StudentID_entry.grid(row=0,column=1,padx=10,pady=5,sticky=W)

        #StudentName
        StudentName_label=Label(Class_Info_Frame,text="Student Name:",bg="white",font=("times new roman",13,"bold"))
        StudentName_label.grid(row=0,column=2,padx=10,pady=5,sticky=W)

        StudentName_entry=ttk.Entry(Class_Info_Frame,textvariable=self.var_std_name,font=('times new roman',12,"bold"),width=20)
        StudentName_entry.grid(row=0,column=3,padx=10,pady=5,sticky=W)

        #Class Division
        ClassDiv_label=Label(Class_Info_Frame,text="Class Division:",bg="white",font=("times new roman",12,"bold"))
        ClassDiv_label.grid(row=1,column=0,padx=10,sticky=W)

        ClassDiv_combo=ttk.Combobox(Class_Info_Frame,textvariable=self.var_div,font=("times new roman",13,"bold"),width=17,state="readonly")
        ClassDiv_combo["values"]=("Select Division","A","B","C","D")
        ClassDiv_combo.current(0)
        ClassDiv_combo.grid(row=1,column=1,padx=10,pady=5,sticky=W)

        #Roll Number
        RegdNo_label=Label(Class_Info_Frame,text="Roll Number:",bg="white",font=("times new roman",13,"bold"))
        RegdNo_label.grid(row=1,column=2,padx=10,pady=5,sticky=W)

        RegdNo_entry=ttk.Entry(Class_Info_Frame,textvariable=self.var_roll,font=('times new roman',12,"bold"),width=20)
        RegdNo_entry.grid(row=1,column=3,padx=10,pady=5,sticky=W)

        #Gender
        Gender_label=Label(Class_Info_Frame,text="Gender",bg="white",font=("times new roman",12,"bold"))
        Gender_label.grid(row=2,column=0,padx=10,sticky=W)

        Gender_combo=ttk.Combobox(Class_Info_Frame,textvariable=self.var_gender,font=("times new roman",13,"bold"),width=17,state="readonly")
        Gender_combo["values"]=("Select Gender","Male","Female")
        Gender_combo.current(0)
        Gender_combo.grid(row=2,column=1,padx=10,pady=5,sticky=W)

        #DOB
        DOB_label=Label(Class_Info_Frame,text="DOB:",bg="white",font=("times new roman",13,"bold"))
        DOB_label.grid(row=2,column=2,padx=10,pady=5,sticky=W)

        DOB_entry=ttk.Entry(Class_Info_Frame,textvariable=self.var_dob,font=('times new roman',12,"bold"),width=20)
        DOB_entry.grid(row=2,column=3,padx=10,pady=5,sticky=W)

        #Email
        Email_label=Label(Class_Info_Frame,text="Email ID:",bg="white",font=("times new roman",13,"bold"))
        Email_label.grid(row=3,column=0,padx=10,pady=5,sticky=W)

        Email_entry=ttk.Entry(Class_Info_Frame,textvariable=self.var_email,font=('times new roman',12,"bold"),width=21)
        Email_entry.grid(row=3,column=1,padx=10,pady=5,sticky=W)
        
        #PhoneNo
        PhoneNo_label=Label(Class_Info_Frame,text="PhoneNo:",bg="white",font=("times new roman",13,"bold"))
        PhoneNo_label.grid(row=3,column=2,padx=10,pady=5,sticky=W)

        PhoneNo_entry=ttk.Entry(Class_Info_Frame,textvariable=self.var_phone,font=('times new roman',12,"bold"),width=20)
        PhoneNo_entry.grid(row=3,column=3,padx=10,pady=5,sticky=W)

        #Address
        Address_label=Label(Class_Info_Frame,text="Address:",bg="white",font=("times new roman",13,"bold"))
        Address_label.grid(row=4,column=0,padx=10,pady=5,sticky=W)

        Address_entry=ttk.Entry(Class_Info_Frame,textvariable=self.var_address,font=('times new roman',12,"bold"),width=21)
        Address_entry.grid(row=4,column=1,padx=10,pady=5,sticky=W)

        #Proctor
        Proctor_label=Label(Class_Info_Frame,text="ProctorName:",bg="white",font=("times new roman",13,"bold"))
        Proctor_label.grid(row=4,column=2,padx=10,pady=5,sticky=W)

        Proctor_entry=ttk.Entry(Class_Info_Frame,textvariable=self.var_proctor,font=('times new roman',12,"bold"),width=20)
        Proctor_entry.grid(row=4,column=3,padx=10,pady=5,sticky=W)

        #Radio Button
        self.var_radio1=StringVar()

        Radiobtn1=ttk.Radiobutton(Class_Info_Frame,variable=self.var_radio1,text="Take Photo Sample",value="Yes")
        Radiobtn1.grid(row=5,column=0,padx=10,pady=5,sticky=W)
        
        Radiobtn2=ttk.Radiobutton(Class_Info_Frame,variable=self.var_radio1,text="No Photo Sample",value="No")
        Radiobtn2.grid(row=5,column=1,padx=10,pady=5,sticky=W)

        #button frame
        btn_frame=Frame(Class_Info_Frame,bd=2,relief='ridge',bg='white')
        btn_frame.place(x=0,y=200,width=715,height=35)
        
        save_btn=Button(btn_frame,text="Save",width=17,command=self.add_data,font=('times new roman',13,"bold"),bg="blue",fg="white")
        save_btn.grid(row=0,column=0)

        update_btn=Button(btn_frame,text="Update",width=17,font=('times new roman',13,"bold"),bg="blue",fg="white")
        update_btn.grid(row=0,column=1)

        delete_btn=Button(btn_frame,text="Delete",width=17,font=('times new roman',13,"bold"),bg="blue",fg="white")
        delete_btn.grid(row=0,column=2)

        reset_btn=Button(btn_frame,text="Reset",width=17,font=('times new roman',13,"bold"),bg="blue",fg="white")
        reset_btn.grid(row=0,column=3)

        #button frame1
        btn_frame1=Frame(Class_Info_Frame,bd=2,relief='ridge',bg='white')
        btn_frame1.place(x=0,y=235,width=715,height=35)
        take_photo_btn=Button(btn_frame1,text="Take Photo Sample",width=35,font=('times new roman',13,"bold"),bg="blue",fg="white")
        take_photo_btn.grid(row=0,column=0)

        update_photo_btn=Button(btn_frame1,text="Update Photo Sample",width=35,font=('times new roman',13,"bold"),bg="blue",fg="white")
        update_photo_btn.grid(row=0,column=1)
        

        #right label frame
        Right_Frame=LabelFrame(main_frame,bd=2,bg='white',relief='ridge',text="Student Details",font=('times new roman',12,"bold"))
        Right_Frame.place(x=750,y=10,width=720,height=580)

        img5_Right=Image.open("college image\\background.jpg")
        img5_Right=img5_Right.resize((1530,710),Image.Resampling.LANCZOS)
        self.photoimg5_Right=ImageTk.PhotoImage(img5_Right)

        bg_img=Label(Right_Frame,image=self.photoimg5_Right)
        bg_img.place(x=5,y=0,width=710,height=130)

        #=================Search System=================
        Search_Frame=LabelFrame(Right_Frame,bd=2,bg='white',relief='ridge',text="Search System",font=('times new roman',12,"bold"))
        Search_Frame.place(x=5,y=135,width=710,height=70)

        search_label=Label(Search_Frame,text="Search By:",bg="red",font=("times new roman",13,"bold"),fg="white")
        search_label.grid(row=0,column=0,padx=10,sticky=W)
        search_combo=ttk.Combobox(Search_Frame,font=("times new roman",13,"bold"),width=15,state="readonly")
        search_combo["values"]=("Select","Roll_No","Phone_No")
        search_combo.current(0)
        search_combo.grid(row=0,column=1,padx=2,pady=5,sticky=W)
        
        search_entry=ttk.Entry(Search_Frame,width=15,font=("times new roman",13,"bold"))
        search_entry.grid(row=0,column=2,padx=10,pady=5,sticky=W)   
        search_btn=Button(Search_Frame,text="Search",width=12,font=('times new roman',13,"bold"),bg="blue",fg="white")
        search_btn.grid(row=0,column=3,padx=4)  
        showAll_btn=Button(Search_Frame,text="Show All",width=12,font=('times new roman',13,"bold"),bg="blue",fg="white")
        showAll_btn.grid(row=0,column=4,padx=4)
        #=================Table Frame=================
        Table_Frame=Frame(Right_Frame,bd=2,bg='white',relief='ridge')
        Table_Frame.place(x=5,y=210,width=710,height=350)
        scroll_x=ttk.Scrollbar(Table_Frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(Table_Frame,orient=VERTICAL)     

        self.student_table=ttk.Treeview(Table_Frame,column=("dep","course","year","sem","id","name","div","regd","group","gender","dob","email","phone","address","proctor","photo"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        # self.student_table.column("dep",width=100)
        # self.student_table.column("course",width=100)
        # self.student_table.column("year",width=100)
        # self.student_table.column("sem",width=100)
        # self.student_table.column("id",width=100)
        # self.student_table.column("name",width=100)
        # self.student_table.column("div",width=100)
        # self.student_table.column("regd",width=100)
        # self.student_table.column("group",width=100)

        self.student_table.heading("dep",text="Department")
        self.student_table.heading("course",text="Course")
        self.student_table.heading("year",text="Year")
        self.student_table.heading("sem",text="Semester")
        self.student_table.heading("id",text="StudentID")
        self.student_table.heading("name",text="Name")  
        self.student_table.heading("div",text="Division")
        self.student_table.heading("regd",text="RegdNo")
        self.student_table.heading("group",text="Group")
        self.student_table.heading("gender",text="Gender")
        self.student_table.heading("dob",text="DOB")
        self.student_table.heading("email",text="Email")
        self.student_table.heading("phone",text="PhoneNo")
        self.student_table.heading("address",text="Address")
        self.student_table.heading("proctor",text="Proctor")
        self.student_table.heading("photo",text="PhotoSampleStatus")
        self.student_table["show"]="headings"

        self.student_table.pack(fill=BOTH,expand=1)
        
        #Funtion Declaration

    def add_data(self):
      if self.var_dep.get()=="Select Department" or self.var_std_name.get()=="" or self.var_std_id.get()=="":
        messagebox.showerror("Error","All Fields are required",parent=self.root)
      else:
          try:
              conn=mysql.connector.connect(host="localhost",username="root",password="Reverse@Osmosis1132",database="face_recog")
              my_cursor=conn.cursor()
              my_cursor.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
                
                                                                              self.var_dep.get(),
                                                                              self.var_course.get(),
                                                                              self.var_year.get(),
                                                                              self.var_sem.get(),
                                                                              self.var_std_id.get(),  
                                                                              self.var_std_name.get(),
                                                                              self.var_div.get(),
                                                                              self.var_roll.get(),
                                                                              self.var_group.get(),
                                                                              self.var_gender.get(),
                                                                              self.var_dob.get(),
                                                                              self.var_email.get(),
                                                                              self.var_phone.get(), 
                                                                              self.var_address.get(),
                                                                              self.var_proctor.get(),
                                                                              self.var_radio1.get()

                                                                                  ))
              conn.commit()
              conn.close()
              messagebox.showinfo("Successful","Student details successfully added",parent=self.root)
          except Exception as es:
              messagebox.showerror("Error",f"Due to :{str(es)}",parenrt=self.root)

if __name__ =="__main__":
    root=Tk()
    obj=Student(root)
    root.mainloop()
    
