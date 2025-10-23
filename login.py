from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import threading
import pyttsx3

class Login_Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Window")
        self.root.geometry("1550x800+0+0")
        
        # Initialize TTS engine
        self.engine = pyttsx3.init()
        try:
            voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
        except Exception as e:
            print(f"Could not set TTS voice: {e}")

        # Background image
        try:
            original_bg_image = Image.open(r"college images/image3.jpg")
            resized_bg_image = original_bg_image.resize((1550, 800), Image.Resampling.LANCZOS)
            self.bg = ImageTk.PhotoImage(resized_bg_image)
            lbl_bg = Label(self.root, image=self.bg)
            lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.root.config(bg="gray")
        
        # Login frame
        frame = Frame(self.root, bg="black")
        frame.place(x=610, y=170, width=340, height=450)
        
        # User icon
        try:
            img1 = Image.open(r"college images/image4.jpg")
            img1 = img1.resize((100, 100), Image.Resampling.LANCZOS)
            self.photoimage1 = ImageTk.PhotoImage(img1)
            lblimg1 = Label(image=self.photoimage1, bg="black", borderwidth=0)
            lblimg1.place(x=730, y=175, width=100, height=100)
        except Exception as e:
            print(f"Error loading user icon: {e}")
        
        # Title
        get_str = Label(frame, text="Get Started", font=("times new roman", 20, "bold"), fg="red", bg="black")
        get_str.place(x=95, y=100)
        
        # Username
        username = Label(frame, text="Username", font=("times new roman", 15, "bold"), fg="white", bg="black")
        username.place(x=70, y=155)
        
        self.txtuser = Entry(frame, font=("times new roman", 15), bg="lightgray")
        self.txtuser.place(x=40, y=180, width=270)
        
        # Password
        password = Label(frame, text="Password", font=("times new roman", 15, "bold"), fg="white", bg="black")
        password.place(x=70, y=225)
        
        self.txtpass = Entry(frame, show="*", font=("times new roman", 15), bg="lightgray")
        self.txtpass.place(x=40, y=250, width=270)
        
        # Field icons
        try:
            img2 = Image.open(r"college images/image4.jpg")
            img2 = img2.resize((25, 25), Image.Resampling.LANCZOS)
            self.photoimage2 = ImageTk.PhotoImage(img2)
            lblimg1_user_icon = Label(image=self.photoimage2, bg="black", borderwidth=0)
            lblimg1_user_icon.place(x=650, y=323, width=25, height=25)
            
            img3 = Image.open(r"college images/image4.jpg")
            img3 = img3.resize((25, 25), Image.Resampling.LANCZOS)
            self.photoimage3 = ImageTk.PhotoImage(img3)
            lblimg2_pass_icon = Label(image=self.photoimage3, bg="black", borderwidth=0)
            lblimg2_pass_icon.place(x=650, y=395, width=25, height=25)
        except Exception as e:
            print(f"Error loading field icons: {e}")
        
        # Login button
        loginbtn = Button(frame, command=self.login, text="Login", font=("times new roman", 15, "bold"), 
                        fg="white", bg="red", activeforeground="white", activebackground="red", cursor="hand2")
        loginbtn.place(x=110, y=300, width=120, height=35)
        
        # Register button
        registerbtn = Button(frame, text="Register New Account", command=self.register_window, 
                        font=("times new roman", 10, "bold"), fg="red", bg="black", borderwidth=0, 
                        activeforeground="red", activebackground="black", cursor="hand2")
        registerbtn.place(x=75, y=350, width=200)
        
        # Forget password button
        forgetbtn = Button(frame, text="Forget Password", command=self.forget_password_window, 
                        font=("times new roman", 10, "bold"), fg="red", bg="black", borderwidth=0, 
                        activeforeground="red", activebackground="black", cursor="hand2")
        forgetbtn.place(x=95, y=370, width=160)
    
    def _speak_thread(self, text):
        """Internal function to run the speech engine."""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Speech Error: {e}")

    def speak(self, text):
        """Speaks the given text in a non-blocking background thread."""
        threading.Thread(target=self._speak_thread, args=(text,), daemon=True).start()
        
    def login(self):
        if self.txtuser.get() == "" or self.txtpass.get() == "":
            messagebox.showerror("Error", "All fields are required")
            return
            
        # Admin login
        if self.txtuser.get() == "admin" and self.txtpass.get() == "12345":
            self.speak("Welcome to Advanced Facial Recognition Attendance System")
            messagebox.showinfo("Success", "Welcome to Advanced Facial Recognition Attendance System")
            self.open_main_system()
            return
        
        # Database login
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Raza@Khan2002",
                database="face_recog"
            )
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT * FROM register WHERE email=%s AND password=%s", 
                            (self.txtuser.get(), self.txtpass.get()))
            row = my_cursor.fetchone()
            
            if row is None:
                messagebox.showerror("Error", "Invalid Username or Password")
            else:
                open_main = messagebox.askyesno("Access Control", "Access only Admin")
                if open_main:
                    self.speak("Welcome to Advanced Facial Recognition Attendance System")
                    self.open_main_system()
            
            conn.close()
        except Exception as es:
            messagebox.showerror("Error", f"Database connection error: {str(es)}")

    def open_main_system(self):
        """Open main.py Face_Recognition_System with proper window handling"""
        try:
            # Hide login window immediately
            self.root.withdraw()
            
            # Create new window for main system
            self.main_window = Toplevel(self.root)
            self.main_window.protocol("WM_DELETE_WINDOW", self.return_to_login)
            
            # Import and initialize main system
            import sys
            import os
            
            # Add current directory to path if not already there
            current_dir = os.path.dirname(os.path.abspath(__file__))
            if current_dir not in sys.path:
                sys.path.insert(0, current_dir)
            
            # Import Face_Recognition_System
            from main import Face_Recognition_System
            
            # Initialize main system
            self.app = Face_Recognition_System(self.main_window)
            
        except ImportError as e:
            error_msg = f"Could not import main.py.\n\nMake sure:\n1. main.py exists in the same folder\n2. main.py has 'Face_Recognition_System' class\n\nError: {str(e)}"
            messagebox.showerror("Import Error", error_msg)
            self.root.deiconify()
        except Exception as e:
            messagebox.showerror("Error", f"Error opening main system: {str(e)}")
            self.root.deiconify()
    
    def return_to_login(self):
        """Return to login page when main system exits"""
        try:
            # Destroy main window
            if hasattr(self, 'main_window') and self.main_window.winfo_exists():
                self.main_window.destroy()
        except:
            pass
        
        # Clear login fields for security
        self.txtuser.delete(0, END)
        self.txtpass.delete(0, END)
        
        # Show login window again
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def register_window(self):
        self.new_window = Toplevel(self.root)
        self.app = register(self.new_window)

    def reset_pass(self):
        if self.combo_security_Q.get() == "Select":
            messagebox.showerror("Error", "Please select a security question", parent=self.root2)
        elif self.text_security_A.get() == "":
            messagebox.showerror("Error", "Please enter the security answer", parent=self.root2)
        elif self.text_new_password.get() == "":
            messagebox.showerror("Error", "Please enter the new password", parent=self.root2)
        else:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Raza@Khan2002",
                    database="face_recog"
                )
                my_cursor = conn.cursor()
                query = "SELECT * FROM register WHERE email=%s AND security_Q=%s AND security_A=%s"
                value = (self.txtuser.get(), self.combo_security_Q.get(), self.text_security_A.get())
                my_cursor.execute(query, value)
                row = my_cursor.fetchone()
                
                if row is None:
                    messagebox.showerror("Error", "Invalid security question or answer", parent=self.root2)
                else:
                    query = "UPDATE register SET password=%s WHERE email=%s"
                    value = (self.text_new_password.get(), self.txtuser.get())
                    my_cursor.execute(query, value)
                    conn.commit()
                    messagebox.showinfo("Success", "Password reset successfully. Please login with your new password.", 
                                    parent=self.root2)
                    self.root2.destroy()
                
                conn.close()
            except Exception as es:
                messagebox.showerror("Error", f"Database connection error: {str(es)}", parent=self.root2)

    def forget_password_window(self):
        if self.txtuser.get() == "":
            messagebox.showerror("Error", "Please enter your email address to reset password")
        else:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Raza@Khan2002",
                    database="face_recog"
                )
                my_cursor = conn.cursor()
                query = "SELECT * FROM register WHERE email=%s"
                value = (self.txtuser.get(),)
                my_cursor.execute(query, value)
                row = my_cursor.fetchone()
                
                if row is None:
                    messagebox.showerror("Error", "This email is not registered")
                else:
                    conn.close()
                    self.root2 = Toplevel()
                    self.root2.title("Forget Password")
                    self.root2.geometry("350x400+650+200")
                    
                    l = Label(self.root2, text="Forget Password", font=("times new roman", 20, "bold"), 
                            fg="darkgreen", bg="white")
                    l.place(x=0, y=10, relwidth=1)
                    
                    security_Q = Label(self.root2, text="Security Question", 
                                    font=("times new roman", 15, "bold"), bg="white")
                    security_Q.place(x=50, y=80)
                    
                    self.combo_security_Q = ttk.Combobox(self.root2, font=("times new roman", 15), state="readonly")
                    self.combo_security_Q.place(x=50, y=110, width=250)
                    self.combo_security_Q["values"] = ("Select", "Your First Pet Name", "Your Birth Place", 
                                                    "Your Favorite Color")
                    self.combo_security_Q.current(0)
                    
                    security_A = Label(self.root2, text="Security Answer", 
                                    font=("times new roman", 15, "bold"), bg="white")
                    security_A.place(x=50, y=150)
                    
                    self.text_security_A = ttk.Entry(self.root2, font=("times new roman", 15))
                    self.text_security_A.place(x=50, y=180, width=250)
                    
                    new_password = Label(self.root2, text="New Password", 
                                    font=("times new roman", 15, "bold"), bg="white")
                    new_password.place(x=50, y=220)
                    
                    self.text_new_password = ttk.Entry(self.root2, font=("times new roman", 15), show="*")
                    self.text_new_password.place(x=50, y=250, width=250)
                    
                    btn = Button(self.root2, text="Reset", command=self.reset_pass, 
                            font=("times new roman", 15, "bold"), fg="white", bg="darkgreen", 
                            borderwidth=0, activeforeground="white", activebackground="darkgreen", cursor="hand2")
                    btn.place(x=110, y=300, width=120, height=35)
            except Exception as es:
                messagebox.showerror("Error", f"Database connection error: {str(es)}")


class register:
    def __init__(self, root):
        self.root = root
        self.root.title("Register")
        self.root.geometry("1600x900+0+0")
        
        # Variables
        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_contact = StringVar()
        self.var_email = StringVar()
        self.var_securityQ = StringVar()
        self.var_securityA = StringVar()
        self.var_pwd = StringVar()
        self.var_confirmpwd = StringVar()
        
        # Background image
        try:
            original_bg_image = Image.open(r"college images/image3.jpg")
            resized_bg_image = original_bg_image.resize((1600, 900), Image.Resampling.LANCZOS)
            self.bg = ImageTk.PhotoImage(resized_bg_image)
            lbl_bg = Label(self.root, image=self.bg)
            lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.root.config(bg="gray")
        
        # Left image
        try:
            self.bg1 = ImageTk.PhotoImage(file=r"college images/image4.jpg")
            left_lbl = Label(self.root, image=self.bg1)
            left_lbl.place(x=50, y=100, width=550, height=600)
        except Exception as e:
            print(f"Error loading left image: {e}")
        
        # Registration frame
        frame = Frame(self.root, bg="white")
        frame.place(x=600, y=100, width=800, height=600)
        
        register_lbl = Label(frame, text="REGISTER HERE", font=("times new roman", 20, "bold"), 
                        fg="darkgreen", bg="white")
        register_lbl.place(x=20, y=20)
        
        # First Name
        fname = Label(frame, text="First Name", font=("times new roman", 15, "bold"), bg="white")
        fname.place(x=50, y=100)
        self.fname_entry = ttk.Entry(frame, textvariable=self.var_fname, font=("times new roman", 15))
        self.fname_entry.place(x=50, y=130, width=250)
        
        # Last Name
        lname = Label(frame, text="Last Name", font=("times new roman", 15, "bold"), bg="white")
        lname.place(x=400, y=100)
        self.text_lname = ttk.Entry(frame, textvariable=self.var_lname, font=("times new roman", 15))
        self.text_lname.place(x=400, y=130, width=250)
        
        # Contact
        contact = Label(frame, text="Contact No.", font=("times new roman", 15, "bold"), bg="white")
        contact.place(x=50, y=170)
        self.text_contact = ttk.Entry(frame, textvariable=self.var_contact, font=("times new roman", 15))
        self.text_contact.place(x=50, y=200, width=250)
        
        # Email
        email = Label(frame, text="Email", font=("times new roman", 15, "bold"), bg="white")
        email.place(x=400, y=170)
        self.text_email = ttk.Entry(frame, textvariable=self.var_email, font=("times new roman", 15))
        self.text_email.place(x=400, y=200, width=250)
        
        # Security Question
        security_Q = Label(frame, text="Security Question", font=("times new roman", 15, "bold"), bg="white")
        security_Q.place(x=50, y=240)
        self.combo_security_Q = ttk.Combobox(frame, textvariable=self.var_securityQ, 
                                            font=("times new roman", 15), state="readonly")
        self.combo_security_Q.place(x=50, y=270, width=250)
        self.combo_security_Q["values"] = ("Select", "Your First Pet Name", "Your Birth Place", 
                                        "Your Favorite Color")
        self.combo_security_Q.current(0)
        
        # Security Answer
        security_A = Label(frame, text="Security Answer", font=("times new roman", 15, "bold"), bg="white")
        security_A.place(x=400, y=240)
        self.text_security_A = ttk.Entry(frame, textvariable=self.var_securityA, font=("times new roman", 15))
        self.text_security_A.place(x=400, y=270, width=250)
        
        # Password
        pwd = Label(frame, text="Password", font=("times new roman", 15, "bold"), bg="white")
        pwd.place(x=50, y=310)
        self.text_pwd = ttk.Entry(frame, textvariable=self.var_pwd, font=("times new roman", 15), show="*")
        self.text_pwd.place(x=50, y=340, width=250)
        
        # Confirm Password
        confirm_pwd = Label(frame, text="Confirm Password", font=("times new roman", 15, "bold"), bg="white")
        confirm_pwd.place(x=400, y=310)
        self.text_confirm_pwd = ttk.Entry(frame, textvariable=self.var_confirmpwd, 
                                        font=("times new roman", 15), show="*")
        self.text_confirm_pwd.place(x=400, y=340, width=250)
        
        # Terms checkbox
        self.var_check = IntVar()
        self.checkbtn = Checkbutton(frame, variable=self.var_check, text="I Agree The Terms & Conditions", 
                                font=("times new roman", 12, "bold"), bg="white", onvalue=1, offvalue=0, 
                                activebackground="white")
        self.checkbtn.place(x=50, y=380)
        
        # Buttons
        try:
            img = Image.open(r"college images/image3.jpg")
            img = img.resize((200, 50), Image.Resampling.LANCZOS)
            self.photoimg = ImageTk.PhotoImage(img)
            b1 = Button(frame, image=self.photoimg, command=self.register_data, text="Register Now", 
                    font=("times new roman", 12, "bold"), compound="center", borderwidth=0, 
                    cursor="hand2", bg="white", fg="blue")
            b1.place(x=60, y=450, width=200)
            
            img1 = Image.open(r"college images/image3.jpg")
            img1 = img1.resize((200, 50), Image.Resampling.LANCZOS)
            self.photoimg1 = ImageTk.PhotoImage(img1)
            b2 = Button(frame, image=self.photoimg1, command=self.return_login, text="Login Now", 
                    font=("times new roman", 12, "bold"), compound="center", borderwidth=0, 
                    cursor="hand2", bg="white", fg="blue")
            b2.place(x=300, y=450, width=200)
        except Exception as e:
            print(f"Error loading button images: {e}")

    def register_data(self):
        if self.var_fname.get() == "" or self.var_email.get() == "" or self.var_securityQ.get() == "Select":
            messagebox.showerror("Error", "All Fields are Required", parent=self.root)
        elif self.var_pwd.get() != self.var_confirmpwd.get():
            messagebox.showerror("Error", "Password & Confirm Password must be same", parent=self.root)
        elif self.var_check.get() == 0:
            messagebox.showerror("Error", "Please Agree our Terms & Conditions", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Raza@Khan2002",
                    database="face_recog"
                )
                my_cursor = conn.cursor()
                query = "SELECT * FROM register WHERE email=%s"
                value = (self.var_email.get(),)
                my_cursor.execute(query, value)
                row = my_cursor.fetchone()
                
                if row is not None:
                    messagebox.showerror("Error", "User already exists, please try another email", 
                                    parent=self.root)
                else:
                    my_cursor.execute("INSERT INTO register VALUES(%s,%s,%s,%s,%s,%s,%s)", (
                        self.var_fname.get(),
                        self.var_lname.get(),
                        self.var_contact.get(),
                        self.var_email.get(),
                        self.var_securityQ.get(),
                        self.var_securityA.get(),
                        self.var_pwd.get()
                    ))
                    conn.commit()
                    messagebox.showinfo("Success", "Registered Successfully", parent=self.root)
                    self.root.destroy()
                
                conn.close()
            except Exception as es:
                messagebox.showerror("Error", f"Error connecting to database: {str(es)}", parent=self.root)

    def return_login(self):
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    app = Login_Window(root)
    root.mainloop()