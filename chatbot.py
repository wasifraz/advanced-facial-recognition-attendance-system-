import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from groq import Groq
import threading
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


class UltimateGroqChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Chatbot - Powered by Groq")
        self.root.geometry("900x700")
        
        # Apply modern dark theme
        self.style = ttk.Style(theme="vapor")
        
        # API Setup
        self.API_KEY = os.getenv("GROQ_API_KEY", "YOUR_API_KEY_HERE")
        if self.API_KEY == "YOUR_API_KEY_HERE":
            messagebox.showwarning("API Key Missing", 
                                 "Please set your GROQ_API_KEY environment variable.")
        self.MODEL = "llama-3.3-70b-versatile"

        try:
            self.client = Groq(api_key=self.API_KEY)
        except Exception as e:
            messagebox.showerror("Error", f"Groq Initialization Failed:\n{str(e)}")

        self.is_streaming = False
        self.theme_dark = True
        self.typing_animation_id = None
        self.message_count = 0
        
        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        # ==================== HEADER SECTION ====================
        header_frame = ttk.Frame(self.root, bootstyle="secondary")
        header_frame.pack(fill=X, side=TOP)
        
        header_content = ttk.Frame(header_frame, bootstyle="secondary")
        header_content.pack(fill=X, padx=20, pady=15)
        
        title_container = ttk.Frame(header_content, bootstyle="secondary")
        title_container.pack(side=LEFT, fill=Y)
        
        title_label = ttk.Label(
            title_container,
            text="🤖 Ultimate AI Chatbot",
            font=("Segoe UI", 24, "bold"),
            bootstyle="inverse-secondary"
        )
        title_label.pack(anchor=W)
        
        subtitle_label = ttk.Label(
            title_container,
            text="Powered by Groq Llama 3.3 70B • Real-time Streaming",
            font=("Segoe UI", 10),
            bootstyle="inverse-secondary"
        )
        subtitle_label.pack(anchor=W, pady=(2, 0))
        
        controls_frame = ttk.Frame(header_content, bootstyle="secondary")
        controls_frame.pack(side=RIGHT, fill=Y)
        
        # Theme toggle button
        self.theme_btn = ttk.Button(
            controls_frame,
            text="☀️ Light",
            command=self.toggle_theme,
            bootstyle="outline-light",
            width=10
        )
        self.theme_btn.pack(side=LEFT, padx=5)
        
        # Clear chat button
        clear_btn = ttk.Button(
            controls_frame,
            text="🗑️ Clear",
            command=self.clear_chat,
            bootstyle="outline-danger",
            width=10
        )
        clear_btn.pack(side=LEFT, padx=5)
        
        # Settings button
        settings_btn = ttk.Button(
            controls_frame,
            text="⚙️",
            command=self.show_settings,
            bootstyle="outline-info",
            width=5
        )
        settings_btn.pack(side=LEFT, padx=5)
        
        # Separator
        ttk.Separator(self.root, bootstyle="secondary").pack(fill=X, pady=0)
        
        # ==================== CHAT AREA ====================
        chat_container = ttk.Frame(self.root) 
        chat_container.pack(fill=BOTH, expand=YES, padx=15, pady=15)
        
        canvas_frame = ttk.Frame(chat_container)
        canvas_frame.pack(fill=BOTH, expand=YES)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(canvas_frame, bootstyle="info-round")
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Get initial theme colors
        self.update_tk_widget_colors()
        
        # Canvas
        self.chat_canvas = tk.Canvas(
            canvas_frame,
            bg=self.default_bg,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.chat_canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.config(command=self.chat_canvas.yview)
        
        # Frame inside canvas for messages
        self.scrolled_frame = ttk.Frame(self.chat_canvas)
        self.canvas_window = self.chat_canvas.create_window(
            (0, 0), 
            window=self.scrolled_frame, 
            anchor="nw"
        )
        
        # Bind canvas to update scroll region
        self.scrolled_frame.bind("<Configure>", self.on_frame_configure)
        self.chat_canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Bind mouse wheel
        self.chat_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        
        # Welcome message
        self.add_bot_message(
            "Hello! I'm your AI assistant powered by Groq's Llama 3.3 70B model. How can I help you today? 😊", 
            show_time=False
        )
        
        # ==================== INPUT AREA ====================
        input_container = ttk.Frame(self.root)
        input_container.pack(fill=X, side=BOTTOM, padx=15, pady=15)
        
        # Input frame with border effect
        input_frame = ttk.Frame(input_container, bootstyle="info")
        input_frame.pack(fill=X)
        
        # Text container
        text_container = ttk.Frame(input_frame)
        text_container.pack(fill=BOTH, expand=YES, padx=2, pady=2)
        
        self.user_input = tk.Text(
            text_container,
            font=("Segoe UI", 11),
            bg=self.input_bg,
            fg=self.default_fg,
            insertbackground=self.accent_color,
            height=3,
            relief=tk.FLAT,
            wrap=tk.WORD,
            padx=12,
            pady=10
        )
        self.user_input.pack(fill=BOTH, expand=YES)
        self.user_input.bind("<Return>", self.enter_pressed)
        self.user_input.bind("<Shift-Return>", lambda e: None)
        self.user_input.bind("<KeyRelease>", self.update_char_count)
        
        # Placeholder text
        self.placeholder_text = "Type your message here... (Shift+Enter for new line)"
        self.user_input.insert("1.0", self.placeholder_text)
        self.user_input.config(fg=self.placeholder_color)
        self.user_input.bind("<FocusIn>", self.on_input_focus_in)
        self.user_input.bind("<FocusOut>", self.on_input_focus_out)
        
        # Bottom bar with character count and send button
        bottom_bar = ttk.Frame(input_container)
        bottom_bar.pack(fill=X, pady=(8, 0))
        
        # Character count
        self.char_count_label = ttk.Label(
            bottom_bar,
            text="0 characters",
            font=("Segoe UI", 9),
            bootstyle="secondary"
        )
        self.char_count_label.pack(side=LEFT)
        
        # Send button
        self.send_btn = ttk.Button(
            bottom_bar,
            text="📤 Send Message",
            command=self.send_message,
            bootstyle="info",
            width=18
        )
        self.send_btn.pack(side=RIGHT)
        
        # Tooltip
        tooltip = ttk.Label(
            bottom_bar,
            text="💡 Tip: Press Enter to send, Shift+Enter for new line",
            font=("Segoe UI", 8),
            bootstyle="secondary"
        )
        tooltip.pack(side=RIGHT, padx=10)

    # ==================== UI HELPER FUNCTIONS ====================
    
    def update_tk_widget_colors(self):
        """
        Fetches current theme colors from ttkbootstrap and applies them
        to standard tk widgets (Canvas, Text).
        """
        # Get colors from the current theme
        colors = self.style.colors
        
        self.default_bg = colors.bg
        
        # FIXED: Use try-except instead of .get() method
        try:
            self.input_bg = colors.inputbg
        except AttributeError:
            self.input_bg = colors.bg
            
        self.default_fg = colors.fg
        self.accent_color = colors.primary
        self.placeholder_color = colors.secondary

        # Update existing widgets if they exist
        if hasattr(self, 'chat_canvas'):
            self.chat_canvas.config(bg=self.default_bg)
        
        if hasattr(self, 'user_input'):
            self.user_input.config(
                bg=self.input_bg,
                fg=self.default_fg,
                insertbackground=self.accent_color
            )
            
            # Re-apply placeholder/text color
            try:
                current_text = self.user_input.get("1.0", "end-1c")
                if current_text == self.placeholder_text:
                    self.user_input.config(fg=self.placeholder_color)
                else:
                    self.user_input.config(fg=self.default_fg)
            except tk.TclError:
                pass
                
    def on_frame_configure(self, event=None):
        """Update scroll region when frame size changes"""
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        self.scroll_to_bottom()
    
    def on_canvas_configure(self, event):
        """Update canvas window width when canvas is resized"""
        self.chat_canvas.itemconfig(self.canvas_window, width=event.width)
    
    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.chat_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def scroll_to_bottom(self):
        """Scroll to bottom of chat"""
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)
    
    def on_input_focus_in(self, event):
        """Remove placeholder on focus"""
        if self.user_input.get("1.0", "end-1c") == self.placeholder_text:
            self.user_input.delete("1.0", tk.END)
            self.user_input.config(fg=self.default_fg)
    
    def on_input_focus_out(self, event):
        """Add placeholder if empty"""
        if not self.user_input.get("1.0", "end-1c").strip():
            self.user_input.insert("1.0", self.placeholder_text)
            self.user_input.config(fg=self.placeholder_color)
    
    def update_char_count(self, event=None):
        """Update character count display"""
        text = self.user_input.get("1.0", "end-1c")
        if text == self.placeholder_text:
            count = 0
        else:
            count = len(text)
        self.char_count_label.config(text=f"{count} characters")
    
    def enter_pressed(self, event):
        """Handle Enter key press"""
        if not event.state & 0x1:  # Check if Shift is not pressed
            self.send_message()
            return "break"
    
    def toggle_theme(self):
        """Toggle between dark and light theme"""
        if self.theme_dark:
            new_theme = "flatly"  # Light theme
            self.theme_btn.config(text="🌙 Dark", bootstyle="outline-dark")
            self.theme_dark = False
        else:
            new_theme = "vapor"   # Dark theme
            self.theme_btn.config(text="☀️ Light", bootstyle="outline-light")
            self.theme_dark = True
            
        # Apply the new theme
        self.style.theme_use(new_theme)
        
        # Update all tk widgets with new colors
        self.update_tk_widget_colors()
    
    def clear_chat(self):
        """Clear all messages"""
        response = messagebox.askyesno(
            "Clear Chat", 
            "Are you sure you want to clear all messages?"
        )
        if response:
            # Destroy all message widgets
            for widget in self.scrolled_frame.winfo_children():
                widget.destroy()
            self.message_count = 0
            # Add welcome message again
            self.add_bot_message("Chat cleared! How can I help you?", show_time=False)
    
    def show_settings(self):
        """Show settings dialog"""
        settings_window = ttk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x350")
        
        ttk.Label(
            settings_window,
            text="⚙️ Settings",
            font=("Segoe UI", 18, "bold"),
            bootstyle="info"
        ).pack(pady=20)
        
        # Settings info frame
        info_frame = ttk.Frame(settings_window, padding=20)
        info_frame.pack(fill=BOTH, expand=YES)
        
        # Model info
        model_frame = ttk.Labelframe(info_frame, text="Model Information", padding=10)
        model_frame.pack(fill=X, pady=5)
        
        ttk.Label(
            model_frame,
            text=f"Model: {self.MODEL}",
            font=("Segoe UI", 10)
        ).pack(anchor=W, pady=2)
        
        ttk.Label(
            model_frame,
            text="Provider: Groq",
            font=("Segoe UI", 10)
        ).pack(anchor=W, pady=2)
        
        # Stats info
        stats_frame = ttk.Labelframe(info_frame, text="Statistics", padding=10)
        stats_frame.pack(fill=X, pady=5)
        
        ttk.Label(
            stats_frame,
            text=f"Total Messages: {self.message_count}",
            font=("Segoe UI", 10)
        ).pack(anchor=W, pady=2)
        
        ttk.Label(
            stats_frame,
            text=f"Theme: {'Dark (Vapor)' if self.theme_dark else 'Light (Flatly)'}",
            font=("Segoe UI", 10)
        ).pack(anchor=W, pady=2)
        
        # Close button
        ttk.Button(
            settings_window,
            text="Close",
            command=settings_window.destroy,
            bootstyle="secondary",
            width=15
        ).pack(pady=15)

    def add_user_message(self, message):
        """Add user message bubble"""
        self.message_count += 1
        
        # Message frame (right-aligned)
        msg_container = ttk.Frame(self.scrolled_frame)
        msg_container.pack(fill=X, pady=8, padx=10)
        
        # Inner frame for message
        inner_frame = ttk.Frame(msg_container)
        inner_frame.pack(side=RIGHT)
        
        # Time stamp
        time_label = ttk.Label(
            inner_frame,
            text=datetime.now().strftime("%I:%M %p"),
            font=("Segoe UI", 8),
            bootstyle="secondary"
        )
        time_label.pack(anchor=E, padx=5)
        
        # Message bubble
        message_frame = ttk.Frame(inner_frame, bootstyle="info")
        message_frame.pack(side=RIGHT, padx=5)
        
        message_label = ttk.Label(
            message_frame,
            text=message,
            font=("Segoe UI", 11),
            wraplength=500,
            bootstyle="inverse-info",
            padding=12,
            justify=LEFT
        )
        message_label.pack()
        
        # User icon
        icon_label = ttk.Label(
            inner_frame,
            text="👤",
            font=("Segoe UI", 16)
        )
        icon_label.pack(side=RIGHT, padx=5)
        
        # Auto scroll
        self.root.update_idletasks()
        self.scroll_to_bottom()

    def add_bot_message(self, message, show_time=True):
        """Add bot message bubble"""
        self.message_count += 1
        
        # Message frame (left-aligned)
        msg_container = ttk.Frame(self.scrolled_frame)
        msg_container.pack(fill=X, pady=8, padx=10)
        
        # Inner frame for message
        inner_frame = ttk.Frame(msg_container)
        inner_frame.pack(side=LEFT)
        
        # Bot icon
        icon_label = ttk.Label(
            inner_frame,
            text="🤖",
            font=("Segoe UI", 16)
        )
        icon_label.pack(side=LEFT, padx=5)
        
        # Message bubble
        message_frame = ttk.Frame(inner_frame, bootstyle="success")
        message_frame.pack(side=LEFT, padx=5)
        
        message_label = ttk.Label(
            message_frame,
            text=message,
            font=("Segoe UI", 11),
            wraplength=500,
            bootstyle="inverse-success",
            padding=12,
            justify=LEFT
        )
        message_label.pack()
        
        # Time stamp
        if show_time:
            time_label = ttk.Label(
                inner_frame,
                text=datetime.now().strftime("%I:%M %p"),
                font=("Segoe UI", 8),
                bootstyle="secondary"
            )
            time_label.pack(side=LEFT, padx=5, anchor=W)
        
        # Auto scroll
        self.root.update_idletasks()
        self.scroll_to_bottom()

    def show_typing_indicator(self):
        """Show typing animation"""
        typing_container = ttk.Frame(self.scrolled_frame)
        typing_container.pack(fill=X, pady=8, padx=10)
        typing_container.pack_configure(anchor=W)
        
        inner_frame = ttk.Frame(typing_container)
        inner_frame.pack(side=LEFT)
        
        # Bot icon
        icon_label = ttk.Label(
            inner_frame,
            text="🤖",
            font=("Segoe UI", 16)
        )
        icon_label.pack(side=LEFT, padx=5)
        
        # Typing indicator
        self.typing_frame = ttk.Frame(inner_frame, bootstyle="warning")
        self.typing_frame.pack(side=LEFT, padx=5)
        
        self.typing_label = ttk.Label(
            self.typing_frame,
            text="Thinking",
            font=("Segoe UI", 11),
            bootstyle="inverse-warning",
            padding=12
        )
        self.typing_label.pack()
        
        # Start animation
        self.animate_typing()
        
        # Auto scroll
        self.root.update_idletasks()
        self.scroll_to_bottom()
        
        return typing_container

    def animate_typing(self, dots=0):
        """Animate typing dots"""
        if hasattr(self, 'typing_label') and self.typing_label.winfo_exists():
            dot_text = "." * (dots % 4)
            self.typing_label.config(text=f"Thinking{dot_text}")
            self.typing_animation_id = self.root.after(
                300, 
                lambda: self.animate_typing(dots + 1)
            )

    def remove_typing_indicator(self, container):
        """Remove typing indicator"""
        if self.typing_animation_id:
            self.root.after_cancel(self.typing_animation_id)
            self.typing_animation_id = None
        if container and container.winfo_exists():
            container.destroy()

    # ==================== MESSAGE HANDLING ====================
    def send_message(self):
        """Handle send message"""
        user_message = self.user_input.get("1.0", tk.END).strip()
        
        # Check if empty or placeholder
        if not user_message or user_message == self.placeholder_text or self.is_streaming:
            return
        
        # Add user message
        self.add_user_message(user_message)
        
        # Clear input
        self.user_input.delete("1.0", tk.END)
        self.update_char_count()
        
        # Disable send button
        self.send_btn.config(state="disabled", text="⏳ Sending...")
        self.is_streaming = True
        
        # Start streaming in thread
        threading.Thread(
            target=self.stream_groq_response, 
            args=(user_message,), 
            daemon=True
        ).start()

    def stream_groq_response(self, user_message):
        """Stream response from Groq API"""
        typing_container = None
        
        try:
            # Show typing indicator
            self.root.after(0, lambda: self.show_typing_indicator())
            typing_container = list(self.scrolled_frame.winfo_children())[-1]
            
            # Call Groq API
            stream = self.client.chat.completions.create(
                model=self.MODEL,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a friendly and knowledgeable AI assistant. Keep responses concise and helpful."
                    },
                    {"role": "user", "content": user_message}
                ],
                stream=True,
                max_tokens=1024
            )

            # Collect response
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    text_chunk = chunk.choices[0].delta.content
                    full_response += text_chunk
            
            # Remove typing indicator
            if typing_container:
                self.root.after(0, lambda: self.remove_typing_indicator(typing_container))
            
            # Add bot response
            self.root.after(0, lambda: self.add_bot_message(full_response))

        except Exception as e:
            # Remove typing indicator
            if typing_container:
                self.root.after(0, lambda: self.remove_typing_indicator(typing_container))
            
            error_msg = f"⚠️ Error: {str(e)}"
            self.root.after(0, lambda: self.add_bot_message(error_msg))
        
        finally:
            # Re-enable send button
            self.root.after(
                0, 
                lambda: self.send_btn.config(state="normal", text="📤 Send Message")
            )
            self.is_streaming = False


# Run standalone
if __name__ == "__main__":
    root = ttk.Window(themename="vapor")
    app = UltimateGroqChatbot(root)
    root.mainloop()