from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import threading
import pyttsx3
import sys
import os

# --- We need to import the main class to open it ---
try:
    from main import Face_Recognition_System
except ImportError:
    messagebox.showerror("Import Error", "Could not find main.py. Make sure it's in the same folder.")
    Face_Recognition_System = None


class Login_Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition System - Login")
        
        # --- OPTIMIZED: Hide window initially for faster perceived load ---
        self.root.withdraw()
        
        # --- OPTIMIZED: Set window properties first ---
        self.root.state('zoomed')
        self.root.minsize(1400, 800)
        
        # Apply modern theme
        self.style = ttk.Style(theme="vapor")
        
        # --- NEW: Variable for password toggle ---
        self.show_password_var = IntVar(value=0)

        # --- OPTIMIZED: Initialize TTS engine in background thread ---
        self.engine = None
        threading.Thread(target=self._init_tts_engine, daemon=True).start()
        

        # Build UI first (fast operations)
        self._build_ui()
        
        # --- OPTIMIZED: Show window immediately after UI is built ---
        self.root.deiconify()
        self.root.update_idletasks()
        
        # --- OPTIMIZED: Load icon after window is visible ---
        self.root.after(100, self._load_icon)

    def _init_tts_engine(self):
        """Initialize TTS engine in background thread"""
        try:
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
        except Exception as e:
            print(f"Could not set TTS voice: {e}")

    def _load_icon(self):
        """Load icon after window is displayed"""
        try:
            if os.path.exists("face_recog icon.ico"):
                self.root.iconbitmap("face_recog icon.ico")
        except Exception as e:
            print(f"Could not load icon: {e}")

    def _build_ui(self):
        """Build the UI (fast operations only)"""
        
        # ==================== MAIN CONTAINER ====================
        main_container = ttk.Frame(self.root, bootstyle="dark")
        main_container.pack(fill=BOTH, expand=YES)

        # ==================== LEFT PANEL - BRANDING ====================
        left_panel = ttk.Frame(main_container, bootstyle="primary", width=700)
        left_panel.pack(side=LEFT, fill=BOTH, expand=YES)
        left_panel.pack_propagate(False)

        # Branding content
        brand_container = ttk.Frame(left_panel, bootstyle="primary")
        brand_container.place(relx=0.5, rely=0.5, anchor=CENTER)

        ttk.Label(
            brand_container,
            text="🔐",
            font=("Segoe UI Emoji", 80),
            bootstyle="inverse-primary"
        ).pack(pady=(0, 20))

        ttk.Label(
            brand_container,
            text="Face Recognition System",
            font=("Helvetica", 36, "bold"),
            bootstyle="inverse-primary"
        ).pack(pady=(0, 10))

        ttk.Label(
            brand_container,
            text="Advanced Facial Recognition Attendance System",
            font=("Helvetica", 14),
            bootstyle="inverse-primary"
        ).pack(pady=(0, 20))

        features_frame = ttk.Frame(brand_container, bootstyle="primary")
        features_frame.pack(pady=30)

        features = [
            "✓ Real-time Face Detection",
            "✓ Automated Attendance Marking",
            "✓ Secure Authentication",
            "✓ Multi-user Support"
        ]

        for feature in features:
            ttk.Label(
                features_frame,
                text=feature,
                font=("Helvetica", 12),
                bootstyle="inverse-primary"
            ).pack(anchor=W, pady=5)

        # ==================== RIGHT PANEL - LOGIN FORM ====================
        right_panel = ttk.Frame(main_container, bootstyle="dark")
        right_panel.pack(side=RIGHT, fill=BOTH, expand=YES)

        login_card = ttk.Frame(right_panel, bootstyle="dark")
        login_card.place(relx=0.5, rely=0.5, anchor=CENTER, width=450)

        header_frame = ttk.Frame(login_card, bootstyle="dark")
        header_frame.pack(fill=X, pady=(0, 30))

        ttk.Label(
            header_frame,
            text="Welcome Back! 👋",
            font=("Helvetica", 28, "bold"),
            bootstyle="light"
        ).pack(anchor=W)

        ttk.Label(
            header_frame,
            text="Please login to continue",
            font=("Helvetica", 12),
            bootstyle="secondary"
        ).pack(anchor=W, pady=(5, 0))

        # Username Section
        username_frame = ttk.Frame(login_card, bootstyle="dark")
        username_frame.pack(fill=X, pady=(0, 20))

        ttk.Label(
            username_frame,
            text="Username or Email",
            font=("Helvetica", 11, "bold"),
            bootstyle="light"
        ).pack(anchor=W, pady=(0, 8))

        username_container = ttk.Frame(username_frame, bootstyle="info")
        username_container.pack(fill=X)

        user_icon_frame = ttk.Frame(username_container, bootstyle="info")
        user_icon_frame.pack(side=LEFT, padx=(10, 5))

        ttk.Label(
            user_icon_frame,
            text="👤",
            font=("Segoe UI Emoji", 16),
            bootstyle="inverse-info"
        ).pack(pady=8)

        self.txtuser = ttk.Entry(
            username_container,
            font=("Helvetica", 12),
            bootstyle="info"
        )
        self.txtuser.pack(side=LEFT, fill=X, expand=YES, padx=(5, 10), pady=10)
        self.txtuser.focus_set()

        # Password Section
        password_frame = ttk.Frame(login_card, bootstyle="dark")
        password_frame.pack(fill=X, pady=(0, 25))

        ttk.Label(
            password_frame,
            text="Password",
            font=("Helvetica", 11, "bold"),
            bootstyle="light"
        ).pack(anchor=W, pady=(0, 8))

        password_container = ttk.Frame(password_frame, bootstyle="info")
        password_container.pack(fill=X)

        pass_icon_frame = ttk.Frame(password_container, bootstyle="info")
        pass_icon_frame.pack(side=LEFT, padx=(10, 5))

        ttk.Label(
            pass_icon_frame,
            text="🔒",
            font=("Segoe UI Emoji", 16),
            bootstyle="inverse-info"
        ).pack(pady=8)

        self.txtpass = ttk.Entry(
            password_container,
            font=("Helvetica", 12),
            show="●",
            bootstyle="info"
        )
        self.txtpass.pack(side=LEFT, fill=X, expand=YES, padx=(5, 5), pady=10)
        self.txtpass.bind("<Return>", lambda e: self.start_login_thread())

        # Password Toggle Button
        self.pass_toggle_btn = ttk.Checkbutton(
            password_container,
            text="👁",
            variable=self.show_password_var,
            command=self.toggle_password,
            bootstyle="info-toolbutton",
            style="Icon.TCheckbutton"
        )
        self.pass_toggle_btn.pack(side=RIGHT, padx=(0, 10), pady=10)
        
        self.style.configure("Icon.TCheckbutton", font=("Segoe UI Emoji", 16))
        self.style.map("Icon.TCheckbutton", 
                       background=[('active', '#03719c'), ('!active', '#03719c')],
                       foreground=[('!active', '#ffffff')])

        # Forgot Password Link
        forgot_frame = ttk.Frame(login_card, bootstyle="dark")
        forgot_frame.pack(fill=X, pady=(0, 25))

        ttk.Button(
            forgot_frame,
            text="Forgot Password?",
            command=self.forget_password_window,
            bootstyle="link",
            cursor="hand2"
        ).pack(side=RIGHT)

        # Login Button
        self.login_btn = ttk.Button(
            login_card,
            text="🚀 Login to Dashboard",
            command=self.start_login_thread,
            bootstyle="success",
            width=30
        )
        self.login_btn.pack(fill=X, pady=(0, 20), ipady=10)

        # Divider
        divider_frame = ttk.Frame(login_card, bootstyle="dark")
        divider_frame.pack(fill=X, pady=20)

        ttk.Separator(divider_frame, bootstyle="secondary").pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))
        ttk.Label(divider_frame, text="OR", bootstyle="secondary", font=("Helvetica", 10)).pack(side=LEFT)
        ttk.Separator(divider_frame, bootstyle="secondary").pack(side=LEFT, fill=X, expand=YES, padx=(10, 0))

        # Register Section
        register_frame = ttk.Frame(login_card, bootstyle="dark")
        register_frame.pack(fill=X, pady=(20, 0))

        ttk.Label(
            register_frame,
            text="Don't have an account?",
            font=("Helvetica", 11),
            bootstyle="secondary"
        ).pack(side=LEFT)

        ttk.Button(
            register_frame,
            text="Register Now",
            command=self.register_window,
            bootstyle="link",
            cursor="hand2"
        ).pack(side=LEFT, padx=(5, 0))

        # Footer
        footer_frame = ttk.Frame(login_card, bootstyle="dark")
        footer_frame.pack(fill=X, pady=(300, 0))

        ttk.Label(
            footer_frame,
            text="🔒 Secure Login • Protected by Advanced Encryption",
            font=("Helvetica", 10),
            bootstyle="secondary"
        ).pack()

    def toggle_password(self):
        """Toggles the password entry visibility."""
        if self.show_password_var.get() == 1:
            self.txtpass.config(show="")
            self.pass_toggle_btn.config(text="🙈")
        else:
            self.txtpass.config(show="●")
            self.pass_toggle_btn.config(text="👁")

    def show_message(self, type, title, message):
        """Shows a messagebox safely from any thread."""
        if type == "error":
            self.root.after(0, lambda: messagebox.showerror(title, message, parent=self.root))
        elif type == "info":
            self.root.after(0, lambda: messagebox.showinfo(title, message, parent=self.root))
        elif type == "askyesno":
            return messagebox.askyesno(title, message, parent=self.root)

    def _speak_thread(self, text):
        """Internal function to run the speech engine."""
        if not self.engine:
            return
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Speech Error: {e}")

    def speak(self, text):
        """Speaks the given text in a non-blocking background thread."""
        threading.Thread(target=self._speak_thread, args=(text,), daemon=True).start()
        
    def start_login_thread(self):
        """Starts the login process in a new thread to keep the UI responsive."""
        self.login_btn.config(state=DISABLED, text="🚀 Verifying...")
        self.root.update_idletasks()
        login_thread = threading.Thread(target=self.login_logic, daemon=True)
        login_thread.start()

    def login_logic(self):
        """The actual login logic that runs in a thread."""
        try:
            user = self.txtuser.get()
            pwd = self.txtpass.get()

            if user == "" or pwd == "":
                self.show_message("error", "Error", "All fields are required")
                return
                
            if user == "admin" and pwd == "12345":
                self.speak("Welcome to Advanced Facial Recognition Attendance System")
                self.show_message("info", "Success", "Welcome to Advanced Facial Recognition Attendance System")
                self.root.after(0, self.open_main_system)
                return
            
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Raza@Khan2002",
                    database="face_recog"
                )
                my_cursor = conn.cursor()
                my_cursor.execute("SELECT * FROM register WHERE email=%s AND password=%s", 
                                (user, pwd))
                row = my_cursor.fetchone()
                
                if row is None:
                    self.show_message("error", "Error", "Invalid Username or Password")
                else:
                    open_main = self.show_message("askyesno", "Access Control", "Access only Admin")
                    
                    if open_main:
                        self.speak("Welcome to Advanced Facial Recognition Attendance System")
                        self.root.after(0, self.open_main_system)
                
                conn.close()
            except Exception as es:
                self.show_message("error", "Error", f"Database connection error: {str(es)}")
        
        finally:
            self.root.after(0, lambda: self.login_btn.config(state=NORMAL, text="🚀 Login to Dashboard"))

    def open_main_system(self):
        """Open main.py Face_Recognition_System with proper window handling"""
        if not Face_Recognition_System:
            self.show_message("error", "Error", "Main application class not loaded. Cannot open.")
            return

        try:
            self.root.withdraw()
            self.main_window = Toplevel(self.root)
            self.main_window.protocol("WM_DELETE_WINDOW", self.return_to_login)
            self.app = Face_Recognition_System(self.main_window)
            
        except Exception as e:
            self.show_message("error", "Error", f"Error opening main system: {str(e)}")
            self.root.after(0, self.root.deiconify)
    
    def return_to_login(self):
        """Return to login page when main system exits"""
        try:
            if hasattr(self, 'main_window') and self.main_window.winfo_exists():
                self.main_window.destroy()
        except Exception as e:
            print(f"Error destroying main window: {e}")
        
        self.txtuser.delete(0, END)
        self.txtpass.delete(0, END)
        
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
                    self.root2 = Toplevel(self.root)
                    self.root2.title("Reset Password")
                    self.root2.geometry("500x550+400+150")
                    
                    popup_style = ttk.Style(theme="vapor")
                    
                    container = ttk.Frame(self.root2, bootstyle="dark", padding=30)
                    container.pack(fill=BOTH, expand=YES)
                    
                    ttk.Label(
                        container,
                        text="🔐 Reset Password",
                        font=("Helvetica", 24, "bold"),
                        bootstyle="light"
                    ).pack(pady=(0, 10))
                    
                    ttk.Label(
                        container,
                        text="Verify your identity to reset password",
                        font=("Helvetica", 11),
                        bootstyle="secondary"
                    ).pack(pady=(0, 30))
                    
                    ttk.Label(
                        container,
                        text="Security Question",
                        font=("Helvetica", 11, "bold"),
                        bootstyle="light"
                    ).pack(anchor=W, pady=(0, 8))
                    
                    self.combo_security_Q = ttk.Combobox(
                        container,
                        font=("Helvetica", 11),
                        state="readonly",
                        bootstyle="info"
                    )
                    self.combo_security_Q["values"] = ("Select", "Your First Pet Name", "Your Birth Place", 
                                                    "Your Favorite Color")
                    self.combo_security_Q.current(0)
                    self.combo_security_Q.pack(fill=X, pady=(0, 20))
                    
                    ttk.Label(
                        container,
                        text="Security Answer",
                        font=("Helvetica", 11, "bold"),
                        bootstyle="light"
                    ).pack(anchor=W, pady=(0, 8))
                    
                    self.text_security_A = ttk.Entry(
                        container,
                        font=("Helvetica", 11),
                        bootstyle="info"
                    )
                    self.text_security_A.pack(fill=X, pady=(0, 20))
                    
                    ttk.Label(
                        container,
                        text="New Password",
                        font=("Helvetica", 11, "bold"),
                        bootstyle="light"
                    ).pack(anchor=W, pady=(0, 8))
                    
                    self.text_new_password = ttk.Entry(
                        container,
                        font=("Helvetica", 11),
                        show="●",
                        bootstyle="info"
                    )
                    self.text_new_password.pack(fill=X, pady=(0, 30))
                    
                    btn_frame = ttk.Frame(container, bootstyle="dark")
                    btn_frame.pack(fill=X, pady=(10, 0))
                    
                    ttk.Button(
                        btn_frame,
                        text="✓ Reset Password",
                        command=self.reset_pass,
                        bootstyle="success",
                        width=20
                    ).pack(side=LEFT, expand=YES, fill=X, padx=(0, 5), ipady=8)
                    
                    ttk.Button(
                        btn_frame,
                        text="✗ Cancel",
                        command=self.root2.destroy,
                        bootstyle="secondary-outline",
                        width=20
                    ).pack(side=LEFT, expand=YES, fill=X, padx=(5, 0), ipady=8)
                    
            except Exception as es:
                messagebox.showerror("Error", f"Database connection error: {str(es)}")


class register:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition System - Registration")
        self.root.geometry("1000x750+200+50")
        
        self.style = ttk.Style(theme="vapor")
        
        # Variables
        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_contact = StringVar()
        self.var_email = StringVar()
        self.var_securityQ = StringVar()
        self.var_securityA = StringVar()
        self.var_pwd = StringVar()
        self.var_confirmpwd = StringVar()
        self.var_check = IntVar()
        
        self.show_pwd_var = IntVar(value=0)
        self.show_confirmpwd_var = IntVar(value=0)

        main_container = ttk.Frame(self.root, bootstyle="dark")
        main_container.pack(fill=BOTH, expand=YES)
        
        header_frame = ttk.Frame(main_container, bootstyle="primary")
        header_frame.pack(fill=X, pady=(0, 0))
        
        header_content = ttk.Frame(header_frame, bootstyle="primary")
        header_content.pack(fill=X, padx=40, pady=25)
        
        ttk.Label(
            header_content,
            text="📝 Create New Account",
            font=("Helvetica", 28, "bold"),
            bootstyle="inverse-primary"
        ).pack(anchor=W)
        
        ttk.Label(
            header_content,
            text="Join the Advanced Face Recognition System",
            font=("Helvetica", 12),
            bootstyle="inverse-primary"
        ).pack(anchor=W, pady=(5, 0))
        
        form_container = ScrolledFrame(main_container, bootstyle="dark", autohide=True)
        form_container.pack(fill=BOTH, expand=YES, padx=40, pady=30)
        
        scrollable_frame = form_container.container
        scrollable_frame.columnconfigure((0, 2), weight=1, minsize=100)
        scrollable_frame.columnconfigure((1, 3), weight=2)

        ttk.Label(scrollable_frame, text="First Name", font=("Helvetica", 11, "bold"), bootstyle="light").grid(row=0, column=0, sticky=W, padx=10, pady=(10, 5))
        ttk.Entry(scrollable_frame, textvariable=self.var_fname, font=("Helvetica", 11), bootstyle="info").grid(row=1, column=0, columnspan=2, sticky=EW, padx=10, pady=(0, 15))
        
        ttk.Label(scrollable_frame, text="Last Name", font=("Helvetica", 11, "bold"), bootstyle="light").grid(row=0, column=2, sticky=W, padx=10, pady=(10, 5))
        ttk.Entry(scrollable_frame, textvariable=self.var_lname, font=("Helvetica", 11), bootstyle="info").grid(row=1, column=2, columnspan=2, sticky=EW, padx=10, pady=(0, 15))
        
        ttk.Label(scrollable_frame, text="Contact Number", font=("Helvetica", 11, "bold"), bootstyle="light").grid(row=2, column=0, sticky=W, padx=10, pady=(10, 5))
        ttk.Entry(scrollable_frame, textvariable=self.var_contact, font=("Helvetica", 11), bootstyle="info").grid(row=3, column=0, columnspan=2, sticky=EW, padx=10, pady=(0, 15))
        
        ttk.Label(scrollable_frame, text="Email Address", font=("Helvetica", 11, "bold"), bootstyle="light").grid(row=2, column=2, sticky=W, padx=10, pady=(10, 5))
        ttk.Entry(scrollable_frame, textvariable=self.var_email, font=("Helvetica", 11), bootstyle="info").grid(row=3, column=2, columnspan=2, sticky=EW, padx=10, pady=(0, 15))
        
        ttk.Label(scrollable_frame, text="Security Question", font=("Helvetica", 11, "bold"), bootstyle="light").grid(row=4, column=0, sticky=W, padx=10, pady=(10, 5))
        security_q_combo = ttk.Combobox(scrollable_frame, textvariable=self.var_securityQ, values=["Select", "Your First Pet Name", "Your Birth Place", "Your Favorite Color"], state="readonly", font=("Helvetica", 11), bootstyle="info")
        security_q_combo.current(0)
        security_q_combo.grid(row=5, column=0, columnspan=2, sticky=EW, padx=10, pady=(0, 15))
        
        ttk.Label(scrollable_frame, text="Security Answer", font=("Helvetica", 11, "bold"), bootstyle="light").grid(row=4, column=2, sticky=W, padx=10, pady=(10, 5))
        ttk.Entry(scrollable_frame, textvariable=self.var_securityA, font=("Helvetica", 11), bootstyle="info").grid(row=5, column=2, columnspan=2, sticky=EW, padx=10, pady=(0, 15))
        
        ttk.Label(scrollable_frame, text="Password", font=("Helvetica", 11, "bold"), bootstyle="light").grid(row=6, column=0, sticky=W, padx=10, pady=(10, 5))
        
        pass_frame = ttk.Frame(scrollable_frame, bootstyle="info")
        pass_frame.grid(row=7, column=0, columnspan=2, sticky=EW, padx=10, pady=(0, 15))
        self.txt_pwd = ttk.Entry(pass_frame, textvariable=self.var_pwd, font=("Helvetica", 11), show="●", bootstyle="info")
        self.txt_pwd.pack(side=LEFT, fill=X, expand=YES, padx=(10, 5), pady=8)
        self.pwd_toggle_btn = ttk.Checkbutton(pass_frame, text="👁", variable=self.show_pwd_var, command=self.toggle_reg_password, bootstyle="info-toolbutton", style="Icon.TCheckbutton")
        self.pwd_toggle_btn.pack(side=RIGHT, padx=(0, 10), pady=8)
        
        ttk.Label(scrollable_frame, text="Confirm Password", font=("Helvetica", 11, "bold"), bootstyle="light").grid(row=6, column=2, sticky=W, padx=10, pady=(10, 5))
        
        confirm_pass_frame = ttk.Frame(scrollable_frame, bootstyle="info")
        confirm_pass_frame.grid(row=7, column=2, columnspan=2, sticky=EW, padx=10, pady=(0, 15))
        self.txt_confirmpwd = ttk.Entry(confirm_pass_frame, textvariable=self.var_confirmpwd, font=("Helvetica", 11), show="●", bootstyle="info")
        self.txt_confirmpwd.pack(side=LEFT, fill=X, expand=YES, padx=(10, 5), pady=8)
        self.confirmpwd_toggle_btn = ttk.Checkbutton(confirm_pass_frame, text="👁", variable=self.show_confirmpwd_var, command=self.toggle_reg_password, bootstyle="info-toolbutton", style="Icon.TCheckbutton")
        self.confirmpwd_toggle_btn.pack(side=RIGHT, padx=(0, 10), pady=8)
        
        terms_frame = ttk.Frame(scrollable_frame, bootstyle="dark")
        terms_frame.grid(row=8, column=0, columnspan=4, pady=(20, 15), padx=10, sticky=W)
        
        
        ttk.Checkbutton(
            terms_frame,
            text="I agree to the Terms & Conditions and Privacy Policy",
            variable=self.var_check,
            bootstyle="success-round-toggle"
        ).pack(anchor=W)
        
        # --- UI/UX FIX: Row 6 (Buttons) ---
        btn_frame = ttk.Frame(scrollable_frame, bootstyle="dark")
        btn_frame.grid(row=9, column=0, columnspan=4, pady=(20, 10), padx=10, sticky=EW)
        
        ttk.Button(
            btn_frame,
            text="✓ Create Account",
            command=self.register_data,
            bootstyle="success",
            width=25
        ).pack(side=LEFT, expand=YES, fill=X, padx=(0, 5), ipady=10)
        
        ttk.Button(
            btn_frame,
            text="← Back to Login",
            command=self.return_login,
            bootstyle="secondary-outline",
            width=25
        ).pack(side=LEFT, expand=YES, fill=X, padx=(5, 0), ipady=10)
        
        # --- UI/UX FIX: Row 7 (Footer) ---
        footer_frame = ttk.Frame(scrollable_frame, bootstyle="dark")
        footer_frame.grid(row=10, column=0, columnspan=4, pady=(20, 10), padx=10)
        
        ttk.Label(
            footer_frame,
            text="Already have an account?",
            font=("Helvetica", 10),
            bootstyle="secondary"
        ).pack(side=LEFT)
        
        ttk.Button(
            footer_frame,
            text="Login Now",
            command=self.return_login, # --- FIX: Corrected typo ---
            bootstyle="link"
        ).pack(side=LEFT, padx=(5, 0))

    # --- NEW: Password toggle for register page ---
    def toggle_reg_password(self):
        if self.show_pwd_var.get() == 1:
            self.txt_pwd.config(show="")
            self.pwd_toggle_btn.config(text="🙈")
        else:
            self.txt_pwd.config(show="●")
            self.pwd_toggle_btn.config(text="👁")
            
        if self.show_confirmpwd_var.get() == 1:
            self.txt_confirmpwd.config(show="")
            self.confirmpwd_toggle_btn.config(text="🙈")
        else:
            self.txt_confirmpwd.config(show="●")
            self.confirmpwd_toggle_btn.config(text="👁")

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
    root = ttk.Window(themename="vapor")
    app = Login_Window(root)
    root.mainloop()