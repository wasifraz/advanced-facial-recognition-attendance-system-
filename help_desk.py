import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
from tkinter import messagebox
from time import strftime
import webbrowser


class HelpDesk:
    def __init__(self, root):
        self.root = root
        self.root.title("Help Desk - Face Recognition System")
        self.root.state("zoomed")
        
        # Professional fonts - reduced sizes for better fit
        self.fonts = {
            'header': ("Segoe UI", 28, "bold"),
            'subheader': ("Segoe UI", 12, "bold"),
            'body': ("Segoe UI", 10),
            'small': ("Segoe UI", 9)
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the complete UI structure"""
        
        # =================== HEADER SECTION ===================
        header_frame = tb.Frame(self.root, bootstyle="dark")
        header_frame.pack(fill=X)
        
        # Title
        tb.Label(
            header_frame,
            text="🆘 HELP DESK",
            font=self.fonts['header'],
            bootstyle="inverse-dark",
            foreground="#3b82f6"
        ).pack(side=LEFT, padx=30, pady=15)
        
        # Live time display
        self.time_lbl = tb.Label(
            header_frame,
            font=("Segoe UI", 14, "bold"),
            bootstyle="inverse-dark",
            foreground="#10b981"
        )
        self.time_lbl.pack(side=RIGHT, padx=30, pady=20)
        self.update_time()
        
        # =================== BACKGROUND ===================
        self.setup_background()
        
        # =================== MAIN CONTENT CONTAINER ===================
        main_container = tb.Frame(self.root)
        main_container.place(relx=0.5, rely=0.53, anchor=CENTER, relwidth=0.92, relheight=0.82)
        
        # Scrollable canvas for content
        canvas = tb.Canvas(main_container, highlightthickness=0, bg='#f8fafc')
        scrollbar = tb.Scrollbar(main_container, orient=VERTICAL, command=canvas.yview, bootstyle="info-round")
        scrollable_frame = tb.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor=NW)
        
        # Make scrollable frame fill canvas width
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind('<Configure>', configure_scroll_region)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # =================== CONTENT SECTIONS ===================
        self.create_welcome_section(scrollable_frame)
        self.create_quick_actions_section(scrollable_frame)
        self.create_faq_section(scrollable_frame)
        self.create_contact_section(scrollable_frame)
        self.create_footer(scrollable_frame)
        
    def setup_background(self):
        """Setup background with blur effect"""
        try:
            img = Image.open(r"college images\background.jpg")
            # Resize and apply blur for modern look
            img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
            img = img.filter(ImageFilter.GaussianBlur(radius=5))
            # Darken for better contrast
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.4)
            
            self.bg_img = ImageTk.PhotoImage(img)
            bg_lbl = tb.Label(self.root, image=self.bg_img)
            bg_lbl.place(x=0, y=80, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Background image error: {e}")
            # Fallback gradient-like background
            bg_frame = tb.Frame(self.root, bootstyle="secondary")
            bg_frame.place(x=0, y=80, relwidth=1, relheight=1)
    
    def create_welcome_section(self, parent):
        """Welcome message section"""
        section = tb.Frame(parent, bootstyle="light", padding=20)
        section.pack(fill=X, padx=20, pady=(10, 15))
        
        tb.Label(
            section,
            text="Welcome to the Help Center",
            font=("Segoe UI", 20, "bold"),
            bootstyle="primary"
        ).pack(anchor=W, pady=(0, 8))
        
        tb.Label(
            section,
            text="Find answers, get support, and learn how to use the Face Recognition Attendance System.",
            font=self.fonts['body'],
            bootstyle="secondary",
            wraplength=1000,
            justify=LEFT
        ).pack(anchor=W)
    
    def create_quick_actions_section(self, parent):
        """Quick action cards"""
        section = tb.Labelframe(
            parent,
            text="🚀 Quick Actions",
            bootstyle="info",
            padding=15
        )
        section.pack(fill=X, padx=20, pady=15)
        
        # Create container frame for cards
        cards_container = tb.Frame(section)
        cards_container.pack(fill=X, expand=True)
        
        # Grid configuration
        for i in range(4):
            cards_container.columnconfigure(i, weight=1, minsize=180)
        
        actions = [
            {
                'icon': '📧',
                'title': 'Email Support',
                'desc': 'frsystem@gmail.com',
                'action': lambda: webbrowser.open("mailto:frsystem@gmail.com"),
                'style': 'primary'
            },
            {
                'icon': '📞',
                'title': 'Call Us',
                'desc': '+91 7735064601',
                'action': lambda: self.show_info("Call Support", "Support: +91 7735064601\nAvailable: Mon-Fri, 9AM-6PM IST"),
                'style': 'success'
            },
            {
                'icon': '📖',
                'title': 'Documentation',
                'desc': 'User guides',
                'action': lambda: webbrowser.open("https://docs.frsystem.ai"),
                'style': 'info'
            },
            {
                'icon': '💬',
                'title': 'Live Chat',
                'desc': 'Chat support',
                'action': lambda: self.show_info("Live Chat", "Live chat coming soon!\nUse email or phone support."),
                'style': 'warning'
            }
        ]
        
        for idx, action in enumerate(actions):
            self.create_action_card(cards_container, idx, action)
    
    def create_action_card(self, parent, index, data):
        """Create individual action card"""
        card = tb.Frame(parent, bootstyle=f"{data['style']}", padding=15)
        card.grid(row=0, column=index, padx=8, pady=8, sticky="nsew")
        
        # Icon
        tb.Label(
            card,
            text=data['icon'],
            font=("Segoe UI", 28),
            bootstyle=f"inverse-{data['style']}"
        ).pack(pady=(5, 8))
        
        # Title
        tb.Label(
            card,
            text=data['title'],
            font=self.fonts['subheader'],
            bootstyle=f"inverse-{data['style']}"
        ).pack(pady=(0, 5))
        
        # Description
        tb.Label(
            card,
            text=data['desc'],
            font=self.fonts['small'],
            bootstyle=f"inverse-{data['style']}",
            wraplength=150
        ).pack(pady=(0, 10))
        
        # Action button
        tb.Button(
            card,
            text="Access",
            bootstyle=f"{data['style']}-outline",
            command=data['action'],
            width=10
        ).pack(pady=(0, 5))
    
    def create_faq_section(self, parent):
        """FAQ accordion section"""
        section = tb.Labelframe(
            parent,
            text="❓ Frequently Asked Questions",
            bootstyle="secondary",
            padding=15
        )
        section.pack(fill=X, padx=20, pady=15)
        
        faqs = [
            {
                'q': 'How do I register a new student?',
                'a': "1. Navigate to 'Student Details' from the main menu\n2. Click 'Add New Student' button\n3. Fill in required information\n4. Capture student photos\n5. Click 'Save' to register"
            },
            {
                'q': 'How to train the face recognition model?',
                'a': "1. After adding photos, go to 'Train Data'\n2. Click 'Train Classifier' button\n3. Wait for training to complete\n4. System is ready to recognize faces"
            },
            {
                'q': 'Why is my face not being recognized?',
                'a': "Common solutions:\n• Ensure adequate lighting\n• Position face directly to camera\n• Retrain model with recent photos\n• Remove obstructions (glasses, masks)\n• Check camera resolution"
            },
            {
                'q': 'How can I view attendance reports?',
                'a': "1. Go to 'Attendance' section\n2. Select date range\n3. Choose department filter\n4. Click 'Generate Report'\n5. Export to Excel or CSV"
            },
            {
                'q': 'What if the application crashes?',
                'a': "1. Check system requirements\n2. Update camera drivers\n3. Restart application\n4. Check error logs\n5. Contact support with error details"
            }
        ]
        
        for idx, faq in enumerate(faqs):
            self.create_faq_item(section, faq, idx)
    
    def create_faq_item(self, parent, faq, index):
        """Create collapsible FAQ item"""
        # Main container for this FAQ
        faq_container = tb.Frame(parent, padding=(0, 5))
        faq_container.pack(fill=X)
        
        # Variable to track expansion state
        is_expanded = tb.BooleanVar(value=False)
        
        # Question button (clickable header)
        q_frame = tb.Frame(faq_container, bootstyle="info", padding=12)
        q_frame.pack(fill=X)
        
        # Arrow indicator
        arrow_label = tb.Label(
            q_frame, 
            text="▶", 
            font=("Segoe UI", 10, "bold"), 
            bootstyle="inverse-info",
            width=2
        )
        arrow_label.pack(side=LEFT, padx=(0, 10))
        
        # Question text
        q_label = tb.Label(
            q_frame,
            text=faq['q'],
            font=self.fonts['subheader'],
            bootstyle="inverse-info",
            anchor=W
        )
        q_label.pack(side=LEFT, fill=X, expand=True)
        
        # Answer frame (initially hidden)
        a_frame = tb.Frame(faq_container, bootstyle="light", padding=(15, 10))
        
        a_label = tb.Label(
            a_frame,
            text=faq['a'],
            font=self.fonts['body'],
            bootstyle="secondary",
            wraplength=900,
            justify=LEFT,
            anchor=W
        )
        a_label.pack(anchor=W, fill=X)
        
        # Toggle function
        def toggle_faq(event=None):
            if is_expanded.get():
                a_frame.pack_forget()
                arrow_label.config(text="▶")
                is_expanded.set(False)
            else:
                a_frame.pack(fill=X, after=q_frame)
                arrow_label.config(text="▼")
                is_expanded.set(True)
        
        # Bind click events to all elements
        for widget in [q_frame, arrow_label, q_label]:
            widget.bind("<Button-1>", toggle_faq)
            widget.bind("<Enter>", lambda e, f=q_frame: f.configure(relief="raised"))
            widget.bind("<Leave>", lambda e, f=q_frame: f.configure(relief="flat"))
    
    def create_contact_section(self, parent):
        """Contact information section"""
        section = tb.Labelframe(
            parent,
            text="📞 Contact Technical Support",
            bootstyle="danger",
            padding=20
        )
        section.pack(fill=X, padx=20, pady=15)
        
        # Contact info container
        contact_frame = tb.Frame(section)
        contact_frame.pack(fill=X, pady=(0, 15))
        
        # Configure grid
        for i in range(3):
            contact_frame.columnconfigure(i, weight=1, minsize=200)
        
        contacts = [
            ('📧 Email', 'support@frsystem.com', 'primary'),
            ('📞 Phone', '+91 7735064601', 'success'),
            ('🌐 Website', 'www.frsystem.ai', 'info')
        ]
        
        for idx, (label, value, style) in enumerate(contacts):
            frame = tb.Frame(contact_frame, bootstyle=style, padding=15)
            frame.grid(row=0, column=idx, padx=10, pady=5, sticky="nsew")
            
            tb.Label(
                frame,
                text=label,
                font=self.fonts['subheader'],
                bootstyle=f"inverse-{style}"
            ).pack(pady=(0, 5))
            
            tb.Label(
                frame,
                text=value,
                font=self.fonts['body'],
                bootstyle=f"inverse-{style}"
            ).pack()
        
        # Emergency support button
        btn_frame = tb.Frame(section)
        btn_frame.pack(fill=X)
        
        tb.Button(
            btn_frame,
            text="🚨 Report Critical Issue",
            bootstyle="danger",
            command=lambda: webbrowser.open("mailto:support@frsystem.com?subject=URGENT: Critical Issue"),
            width=25
        ).pack(pady=5)
    
    def create_footer(self, parent):
        """Footer section"""
        footer = tb.Frame(parent, bootstyle="dark", padding=15)
        footer.pack(fill=X, padx=20, pady=(15, 10))
        
        tb.Label(
            footer,
            text="© 2025 Face Recognition System | Version 2.0 | Need help? Visit our support portal",
            font=self.fonts['small'],
            bootstyle="inverse-dark"
        ).pack()
    
    def update_time(self):
        """Update time display every second"""
        time_str = strftime('%I:%M:%S %p')
        self.time_lbl.config(text=f"🕐 {time_str}")
        self.time_lbl.after(1000, self.update_time)
    
    def show_info(self, title, message):
        """Show information dialog"""
        messagebox.showinfo(title, message)


if __name__ == "__main__":
    root = tb.Window(themename="vapor")
    app = HelpDesk(root)
    root.mainloop()