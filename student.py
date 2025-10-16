from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2


class Student:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        # ================Variables===================
        self.var_dep=StringVar()
        self.var_group=StringVar()
        self.var_year=StringVar()
        self.var_sem=StringVar()
        self.var_std_id=StringVar()
        self.var_std_name=StringVar()
        self.var_course=StringVar()
        self.var_roll=StringVar()
        self.var_gender=StringVar()
        self.var_dob=StringVar()
        self.var_email=StringVar()
        self.var_phone=StringVar()
        self.var_address=StringVar()
        self.var_proctor=StringVar()
        self.var_photo_sample=StringVar()

        # first image
        img=Image.open(r"college images\image1.jpg")
        img=img.resize((530,130),Image.Resampling.LANCZOS)
        self.photoimg=ImageTk.PhotoImage(img)


        f_lbl=Label(self.root,image=self.photoimg)
        f_lbl.place(x=0,y=0,width=500,height=130)   


        # secong image
        img1=Image.open(r"college images\image2.png")
        img1=img1.resize((540,130),Image.Resampling.LANCZOS)
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

        title_lbl=Label(bg_img,text="STUDENT MANAGEMENT SYSTEM",font=("times new roman",35,"bold"),bg="white",fg="green")
        title_lbl.place(x=0,y=0,width=1530,height=45)


        main_frame=Frame(bg_img,bd=2,bg="white")
        main_frame.place(x=20,y=50,width=1480,height=600)

        #left label frame
        Left_frame=LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Student Details",font=("times new roman",12,"bold"))
        Left_frame.place(x=10,y=10,width=730,height=580)

        img_Left=Image.open(r"college images\background.jpg")
        img_Left=img_Left.resize((720,130),Image.Resampling.LANCZOS)
        self.photoimg_Left=ImageTk.PhotoImage(img_Left)
        
        bg_img=Label(Left_frame,image=self.photoimg_Left)
        bg_img.place(x=5,y=0,width=720,height=130)

        # Current Course Details
        Current_Course_Frame=LabelFrame(Left_frame,bd=2,bg="white",relief=RIDGE,text="Current Course",font=("times new roman",12,"bold"))
        Current_Course_Frame.place(x=5,y=135,width=720,height=150)

        #Department
        dept_label=Label(Current_Course_Frame,text="Department",font=("times new roman",13,"bold"),bg="white")
        dept_label.grid(row=0,column=0,padx=10,sticky=W)

        dept_combo=ttk.Combobox(Current_Course_Frame,textvariable=self.var_dep,font=("times new roman",13,"bold"),width=20,state="readonly")
        dept_combo["values"]=("Select Department","CSE","ECE","ENTC","MECH","EE","CIVIL","BScITM","MCA","MBA","BArch")
        dept_combo.current(0)
        dept_combo.grid(row=0,column=1,padx=2,pady=10,sticky=W)

        #Group
        group_label=Label(Current_Course_Frame,text="Group",font=("times new roman",13,"bold"),bg="white")
        group_label.grid(row=0,column=2,padx=10,sticky=W)

        group_combo=ttk.Combobox(Current_Course_Frame,textvariable=self.var_group,font=("times new roman",13,"bold"),width=20,state="readonly")
        group_combo["values"]=("Select Group","1","2","3","4")
        group_combo.current(0)
        group_combo.grid(row=0,column=3,padx=2,pady=10,sticky=W)

        #Year
        Year_label=Label(Current_Course_Frame,text="Year",bg="white",font=("times new roman",13,"bold"))
        Year_label.grid(row=1,column=0,padx=10,sticky=W)

        Year_combo=ttk.Combobox(Current_Course_Frame,textvariable=self.var_year,font=("times new roman",13,"bold"),width=20,state="readonly")
        Year_combo["values"]=("Select Year","First Year","Second Year","Third Year","Fourth Year","Fifth Year")
        Year_combo.current(0)
        Year_combo.grid(row=1,column=1,padx=2,pady=10,sticky=W)

        #Semester
        Sem_label=Label(Current_Course_Frame,text="Semester",bg="white",font=("times new roman",13,"bold"))
        Sem_label.grid(row=1,column=2,padx=10,sticky=W)

        Sem_combo=ttk.Combobox(Current_Course_Frame,textvariable=self.var_sem,font=("times new roman",13,"bold"),width=20,state="readonly")
        Sem_combo["values"]=("Select Semester","1st","2nd","3rd","4th","5th","6th","7th","8th","9th","10th")
        Sem_combo.current(0)
        Sem_combo.grid(row=1,column=3,padx=2,pady=10,sticky=W)

        #class student information
        Class_Info_Frame=LabelFrame(Left_frame,bd=2,bg="white",relief=RIDGE,text="Class Student Information",font=("times new roman",12,"bold"))
        Class_Info_Frame.place(x=5,y=250,width=720,height=300)

        #StudentId
        StudentID_label=Label(Class_Info_Frame,text="Registration Number:",bg="white",font=("times new roman",13,"bold"))
        StudentID_label.grid(row=0,column=0,padx=10,pady=5,sticky=W)

        StudentID_entry=ttk.Entry(Class_Info_Frame,textvariable=self.var_std_id,font=("times new roman",12,"bold"),width=20)
        StudentID_entry.grid(row=0,column=1,padx=10,pady=5,sticky=W)

        #StudentName
        StudentName_label=Label(Class_Info_Frame,text="Student Name:",bg="white",font=("times new roman",13,"bold"))
        StudentName_label.grid(row=0,column=2,padx=10,pady=5,sticky=W)

        StudentName_entry=ttk.Entry(Class_Info_Frame,textvariable=self.var_std_name,font=("times new roman",12,"bold"),width=20)
        StudentName_entry.grid(row=0,column=3,padx=10,pady=5,sticky=W)

        #Course
        Course_label=Label(Class_Info_Frame,text="Course:",bg="white",font=("times new roman",13,"bold"))
        Course_label.grid(row=1,column=0,padx=10,pady=5,sticky=W)

        Course_combo=ttk.Combobox(Class_Info_Frame,textvariable=self.var_course,font=("times new roman",13,"bold"),width=17,state="readonly")
        Course_combo["values"]=("Select Course","BTech","MBA","MCA","BScITM","BArch")
        Course_combo.current(0)
        Course_combo.grid(row=1,column=1,padx=10,pady=5,sticky=W)

        #Roll Number
        RegdNo_label=Label(Class_Info_Frame,text="Roll Number:",bg="white",font=("times new roman",13,"bold"))
        RegdNo_label.grid(row=1,column=2,padx=10,pady=5,sticky=W)

        RegdNo_entry=ttk.Entry(Class_Info_Frame,textvariable=self.var_roll,font=("times new roman",12,"bold"),width=20)
        RegdNo_entry.grid(row=1,column=3,padx=10,pady=5,sticky=W)

        #Gender
        Gender_label=Label(Class_Info_Frame,text="Gender",bg="white",font=("times new roman",12,"bold"))
        Gender_label.grid(row=2,column=0,padx=10,pady=5,sticky=W)

        Gender_combo=ttk.Combobox(Class_Info_Frame,textvariable=self.var_gender,font=("times new roman",13,"bold"),width=17,state="readonly")
        Gender_combo["values"]=("Select Gender","Male","Female")
        Gender_combo.current(0)
        Gender_combo.grid(row=2,column=1,padx=10,pady=5,sticky=W)

        #DOB
        DOB_label=Label(Class_Info_Frame,text="DOB:",bg="white",font=("times new roman",13,"bold"))
        DOB_label.grid(row=2,column=2,padx=10,pady=5,sticky=W)

        DOB_entry=ttk.Entry(Class_Info_Frame,textvariable=self.var_dob,font=("times new roman",12,"bold"),width=20)
        DOB_entry.grid(row=2,column=3,padx=10,pady=5,sticky=W)

        #Email
        Email_label=Label(Class_Info_Frame,text="Email ID:",bg="white",font=("times new roman",13,"bold"))
        Email_label.grid(row=3,column=0,padx=10,pady=5,sticky=W)

        Email_entry=ttk.Entry(Class_Info_Frame,textvariable=self.var_email,font=("times new roman",12,"bold"),width=21)
        Email_entry.grid(row=3,column=1,padx=12,pady=5,sticky=W)
        
        #PhoneNo
        PhoneNo_label=Label(Class_Info_Frame,text="PhoneNo:",bg="white",font=("times new roman",13,"bold"))
        PhoneNo_label.grid(row=3,column=2,padx=10,pady=5,sticky=W)

        PhoneNo_entry=ttk.Entry(Class_Info_Frame,textvariable=self.var_phone,font=("times new roman",12,"bold"),width=20)
        PhoneNo_entry.grid(row=3,column=3,padx=10,pady=5,sticky=W)

        #Address
        Address_label=Label(Class_Info_Frame,text="Address:",bg="white",font=("times new roman",13,"bold"))
        Address_label.grid(row=4,column=0,padx=10,pady=5,sticky=W)

        Address_entry=ttk.Entry(Class_Info_Frame,textvariable=self.var_address,font=("times new roman",12,"bold"),width=21)
        Address_entry.grid(row=4,column=1,padx=12,pady=5,sticky=W)

        #Proctor
        Proctor_label=Label(Class_Info_Frame,text="ProctorName:",bg="white",font=("times new roman",13,"bold"))
        Proctor_label.grid(row=4,column=2,padx=10,pady=5,sticky=W)

        Proctor_entry=ttk.Entry(Class_Info_Frame,textvariable=self.var_proctor,font=("times new roman",12,"bold"),width=20)
        Proctor_entry.grid(row=4,column=3,padx=10,pady=5,sticky=W)

        #Radio Button
        self.var_radio1=StringVar()
        Radiobtn1=ttk.Radiobutton(Class_Info_Frame,variable=self.var_radio1,text="Take Photo Sample",value="Yes")
        Radiobtn1.grid(row=5,column=0,padx=10,pady=5,sticky=W)

        Radiobtn2=ttk.Radiobutton(Class_Info_Frame,variable=self.var_radio1,text="No Photo Sample",value="No")
        Radiobtn2.grid(row=5,column=1,padx=10,pady=5,sticky=W)

        #button frame
        btn_frame=Frame(Class_Info_Frame,bd=2,relief=RIDGE,bg='white')
        btn_frame.place(x=0,y=200,width=715,height=35)
        
        save_btn=Button(btn_frame,text="Save",command=self.add_data,width=17,font=("times new roman",13,"bold"),bg="blue",fg="white")
        save_btn.grid(row=0,column=0)

        update_btn=Button(btn_frame,text="Update",command=self.update_data,width=17,font=("times new roman",13,"bold"),bg="blue",fg="white")
        update_btn.grid(row=0,column=1)

        delete_btn=Button(btn_frame,text="Delete",command=self.delete_data,width=17,font=("times new roman",13,"bold"),bg="blue",fg="white")
        delete_btn.grid(row=0,column=2)

        reset_btn=Button(btn_frame,text="Reset",command=self.reset_data,width=17,font=("times new roman",13,"bold"),bg="blue",fg="white")
        reset_btn.grid(row=0,column=3)

        #button frame1
        btn_frame1=Frame(Class_Info_Frame,bd=2,relief=RIDGE,bg="white")
        btn_frame1.place(x=0,y=235,width=715,height=35)
        take_photo_btn=Button(btn_frame1,command=self.generate_dataset,text="Take Photo Sample",width=35,font=("times new roman",13,"bold"),bg="blue",fg="white")
        take_photo_btn.grid(row=0,column=0)

        update_photo_btn=Button(btn_frame1,text="Update Photo Sample",width=35,font=("times new roman",13,"bold"),bg="blue",fg="white")
        update_photo_btn.grid(row=0,column=1)


        #right label frame
        Right_frame=LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Student Details",font=("times new roman",12,"bold"))
        Right_frame.place(x=750,y=10,width=720,height=580)

        img_Right=Image.open(r"college images\background.jpg")
        img_Right=img_Right.resize((720,130),Image.Resampling.LANCZOS)
        self.photoimg_Right=ImageTk.PhotoImage(img_Right)

        bg_img=Label(Right_frame,image=self.photoimg_Right)
        bg_img.place(x=5,y=0,width=720,height=130)


        #=================Search System=================
        Search_Frame=LabelFrame(Right_frame,bd=2,bg='white',relief=RIDGE,text="Search System",font=("times new roman",12,"bold"))
        Search_Frame.place(x=5,y=135,width=710,height=70)

        Search_bar=Label(Search_Frame,text="Search By:",bg="red",font=("times new roman",13,"bold"),fg="white")
        Search_bar.grid(row=0,column=0,padx=10,pady=5,sticky=W)

        Search_combo=ttk.Combobox(Search_Frame,font=("times new roman",13,"bold"),width=15,state="readonly")
        Search_combo["values"]=("Select","Roll_No","Phone_No")
        Search_combo.current(0)
        Search_combo.grid(row=0,column=1,padx=2,pady=5,sticky=W)

        search_entry=ttk.Entry(Search_Frame,width=15,font=("times new roman",13,"bold"))
        search_entry.grid(row=0,column=2,padx=10,pady=5,sticky=W)

        search_btn=Button(Search_Frame,text="Search",width=12,font=('times new roman',13,"bold"),bg="blue",fg="white")
        search_btn.grid(row=0,column=3,padx=4)  

        showAll_btn=Button(Search_Frame,text="Show All",width=12,font=('times new roman',13,"bold"),bg="blue",fg="white")
        showAll_btn.grid(row=0,column=4,padx=4)

        #=================Table Frame=================
        Table_Frame=Frame(Right_frame,bd=2,bg="white",relief=RIDGE)
        Table_Frame.place(x=5,y=210,width=710,height=350)

        scroll_x=ttk.Scrollbar(Table_Frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(Table_Frame,orient=VERTICAL)

        self.student_table=ttk.Treeview(Table_Frame,column=("dep","group","year","sem","id","name","course","roll_no","gender","dob","email","phone_no","address","proctor","photo"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("dep",text="Department")
        self.student_table.heading("group",text="Group")
        self.student_table.heading("year",text="Year")
        self.student_table.heading("sem",text="Semester")
        self.student_table.heading("id",text="StudentID")
        self.student_table.heading("name",text="Name")
        self.student_table.heading("course",text="Course")  
        self.student_table.heading("roll_no",text="RollNo")
        self.student_table.heading("gender",text="Gender")
        self.student_table.heading("dob",text="DOB")
        self.student_table.heading("email",text="Email")
        self.student_table.heading("phone_no",text="PhoneNo")
        self.student_table.heading("address",text="Address")
        self.student_table.heading("proctor",text="Proctor")
        self.student_table.heading("photo",text="PhotoSampleStatus")
        self.student_table["show"]="headings"

        self.student_table.pack(fill=BOTH,expand=1)
        self.student_table.bind("<ButtonRelease>",self.get_cursor)
        self.fetch_data()
    
    # ====================Function Declaration=====================
    def add_data(self):
        if self.var_dep.get()=="Select Department" or self.var_std_name.get()=="" or self.var_std_id.get()=="":
            messagebox.showerror("Error","All Fields are required",parent=self.root)
        else:
            try:
                conn=mysql.connector.connect(host="localhost",username="root",password="Raza@Khan2002",database="face_recog")
                my_cursor=conn.cursor()
                my_cursor.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",( 
                                                                                                            self.var_dep.get(),
                                                                                                            self.var_group.get(),
                                                                                                            self.var_year.get(),
                                                                                                            self.var_sem.get(),
                                                                                                            self.var_std_id.get(),
                                                                                                            self.var_std_name.get(),
                                                                                                            self.var_course.get(),
                                                                                                            self.var_roll.get(),
                                                                                                            self.var_gender.get(),
                                                                                                            self.var_dob.get(),
                                                                                                            self.var_email.get(),
                                                                                                            self.var_phone.get(), 
                                                                                                            self.var_address.get(),
                                                                                                            self.var_proctor.get(),
                                                                                                            self.var_radio1.get()))

                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Successful","Student details successfully added",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due To :{str(es)}",parent=self.root)

    # ================= fetch data ==================
    def fetch_data(self):
        conn=mysql.connector.connect(host="localhost",username="root",password="Raza@Khan2002",database="face_recog")
        my_cursor=conn.cursor()
        my_cursor.execute("select * from student")
        data=my_cursor.fetchall()

        if len(data)!=0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("",END,values=i)
            conn.commit()
        conn.close()

    # ================ get cursor ================
    def get_cursor(self,event=""):
        cursor_focus=self.student_table.focus()
        content=self.student_table.item(cursor_focus)
        data=content["values"]

        self.var_dep.set(data[0]),
        self.var_group.set(data[1]),
        self.var_year.set(data[2]),
        self.var_sem.set(data[3]),
        self.var_std_id.set(data[4]),
        self.var_std_name.set(data[5]),
        self.var_course.set(data[6]),
        self.var_roll.set(data[7]),
        self.var_gender.set(data[8]),
        self.var_dob.set(data[9]),
        self.var_email.set(data[10]),
        self.var_phone.set(data[11]),
        self.var_address.set(data[12]),
        self.var_proctor.set(data[13]),
        self.var_radio1.set(data[14])

    # ============ Update Function ===========
    def update_data(self):
        if self.var_dep.get()=="Select Department" or self.var_std_name.get()=="" or self.var_std_id.get()=="":
            messagebox.showerror("Error","All Fields are required",parent=self.root)
        else:
            try:
                Update=messagebox.askyesno("Update","Do you want to update this student details?",parent=self.root)
                if Update>0:
                    conn=mysql.connector.connect(host="localhost",username="root",password="Raza@Khan2002",database="face_recog")
                    my_cursor=conn.cursor()
                    my_cursor.execute("Update student set Department=%s,GroupNo=%s,YearNo=%s,Semester=%s,StudentName=%s,Course=%s,RollNo=%s,Gender=%s,DOB=%s,Email=%s,PhoneNo=%s,Home_Address=%s,Proctor=%s,PhotoSampleStatus=%s where StudentID=%s",(

                                                                                                                                                                                                                self.var_dep.get(),
                                                                                                                                                                                                                self.var_group.get(),
                                                                                                                                                                                                                self.var_year.get(),
                                                                                                                                                                                                                self.var_sem.get(),
                                                                                                                                                                                                                self.var_std_name.get(),
                                                                                                                                                                                                                self.var_course.get(),
                                                                                                                                                                                                                self.var_roll.get(),
                                                                                                                                                                                                                self.var_gender.get(),
                                                                                                                                                                                                                self.var_dob.get(),
                                                                                                                                                                                                                self.var_email.get(),
                                                                                                                                                                                                                self.var_phone.get(),
                                                                                                                                                                                                                self.var_address.get(),
                                                                                                                                                                                                                self.var_proctor.get(),
                                                                                                                                                                                                                self.var_radio1.get(),
                                                                                                                                                                                                                self.var_std_id.get(),
                                                                                                                                                                                                            ))
                else:
                    if not Update:
                        return
                messagebox.showinfo("Success","Student details successfully updated",parent=self.root)
                conn.commit()
                self.fetch_data()
                conn.close()
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)

    # =============== Delete Function =================
    def delete_data(self):
        if self.var_std_id.get()=="":
            messagebox.showerror("Error","Student ID is required",parent=self.root)
        else:
            try:
                Delete=messagebox.askyesno("Student Delete Page","Do you want to delete the student details?",parent=self.root)
                if Delete>0:
                    conn=mysql.connector.connect(host="localhost",username="root",password="Raza@Khan2002",database="face_recog")
                    my_cursor=conn.cursor()
                    sql="Delete from student where StudentID=%s"
                    val=(self.var_std_id.get(),)
                    my_cursor.execute(sql,val)
                else:
                    if not Delete:
                        return
                
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Delete","Successfully deleted student details",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)
    
    # ============== Reset Function ====================
    def reset_data(self):
        self.var_dep.set("Select Department")
        self.var_group.set("Select Group")
        self.var_year.set("Select Year")
        self.var_sem.set("Select Semester")
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_course.set("Select Course")
        self.var_roll.set("")
        self.var_gender.set("Male")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_phone.set("") 
        self.var_address.set("")
        self.var_proctor.set("")
        self.var_radio1.set("")

    # =============== Photo Sample Function ===================
    def generate_dataset(self):
        if self.var_dep.get()=="Select Department" or self.var_std_name.get()=="" or self.var_std_id.get()=="":
            messagebox.showerror("Error","All Fields are required",parent=self.root)
        else:
            try:
                conn=mysql.connector.connect(host="localhost",username="root",password="Raza@Khan2002",database="face_recog")
                my_cursor=conn.cursor()
                my_cursor.execute("Select * from student")
                myresult=my_cursor.fetchall()
                id=0
                for x in myresult:
                    id+=1
                my_cursor.execute("Update student set Department=%s,GroupNo=%s,YearNo=%s,Semester=%s,StudentName=%s,Course=%s,RollNo=%s,Gender=%s,DOB=%s,Email=%s,PhoneNo=%s,Home_Address=%s,Proctor=%s,PhotoSampleStatus=%s where StudentID=%s",(

                                                                                                                                                                                                                self.var_dep.get(),
                                                                                                                                                                                                                self.var_group.get(),
                                                                                                                                                                                                                self.var_year.get(),
                                                                                                                                                                                                                self.var_sem.get(),
                                                                                                                                                                                                                self.var_std_name.get(),
                                                                                                                                                                                                                self.var_course.get(),
                                                                                                                                                                                                                self.var_roll.get(),
                                                                                                                                                                                                                self.var_gender.get(),
                                                                                                                                                                                                                self.var_dob.get(),
                                                                                                                                                                                                                self.var_email.get(),
                                                                                                                                                                                                                self.var_phone.get(),
                                                                                                                                                                                                                self.var_address.get(),
                                                                                                                                                                                                                self.var_proctor.get(),
                                                                                                                                                                                                                self.var_radio1.get(),
                                                                                                                                                                                                                self.var_std_id.get()==id+1
                                                                                                                                                                                                            ))
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()

                # ============ load predefined data on face frontals from opencv===========

                face_classifier=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

                def face_cropped(img):
                    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    faces=face_classifier.detectMultiScale(gray,1.3,5)

                    for(x,y,w,h) in faces:
                        face_cropped=img[y:y+h,x:x+w]
                        return face_cropped
                
                cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
                img_id=0
                while True:
                    ret,my_frame=cap.read()
                    if face_cropped(my_frame) is not None:
                        img_id+=1
                        face=cv2.resize(face_cropped(my_frame),(450,450))
                        face=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
                        file_name_path="data/user."+str(id)+"."+str(img_id)+".jpg"
                        cv2.imwrite(file_name_path,face)
                        cv2.putText(face,str(img_id),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)
                        cv2.imshow("Your Face",face)

                    if cv2.waitKey(1)==13 or int(img_id)==100:
                        break
                cap.release()
                cv2.destroyAllWindows()

                messagebox.showinfo("Result","Generating data sets!!")
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)
                    

if __name__ == "__main__":
    root=Tk()
    obj=Student(root)
    root.mainloop()