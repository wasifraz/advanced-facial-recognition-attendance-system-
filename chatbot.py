# chatbot.py

import tkinter as tk
from tkinter import scrolledtext, messagebox
from groq import Groq
import threading
import os
from dotenv import load_dotenv

load_dotenv()

class UltimateGroqChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate AI Chatbot - Powered by Groq")
        self.root.geometry("600x800")
        self.root.resizable(False, False)

        # ✅ Use Environment Variable for API Key (secure)
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

        # UI Setup
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Label(self.root, text="🤖 Ultimate AI Chatbot",
                        font=("Segoe UI", 22, "bold"), bg="#111b27", fg="#00d4ff", pady=18)
        header.pack(fill=tk.X)

        subtitle = tk.Label(self.root, text="Powered by Groq Llama 3.3 70B",
                            font=("Segoe UI", 10), bg="#111b27", fg="#88A", pady=0)
        subtitle.pack(fill=tk.X)

        # Chat area
        chat_frame = tk.Frame(self.root, bg="#181f2a")
        chat_frame.pack(fill=tk.BOTH, expand=True)
        self.chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD,
                                                    bg="#1a2130", fg="#fff",
                                                    state=tk.DISABLED,
                                                    font=("Segoe UI", 11),
                                                    padx=15, pady=15)
        self.chat_display.pack(fill=tk.BOTH, expand=True)

        # Color tags
        self.chat_display.tag_config("user", foreground="#00d4ff", font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_config("bot", foreground="#00ba7c", font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_config("msg_user", foreground="#fff", lmargin1=30, lmargin2=30)
        self.chat_display.tag_config("msg_bot", foreground="#e6ffe9", lmargin1=30, lmargin2=30)
        self.chat_display.tag_config("typing", foreground="#ffaa00", font=("Segoe UI", 10, "italic"))

        # Input area
        input_frame = tk.Frame(self.root, bg="#141c24", height=70)
        input_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.user_input = tk.Text(input_frame, font=("Segoe UI", 12),
                                bg="#2d2d2d", fg="#fff", height=2, relief=tk.FLAT)
        self.user_input.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=10, pady=13)
        self.user_input.bind("<Return>", self.enter_pressed)
        self.user_input.bind("<Shift-Return>", lambda e: None)

        send_btn = tk.Button(input_frame, text="Send", command=self.send_message,
                            font=("Segoe UI", 12, "bold"), bg="#00d4ff", fg="#05141b",
                            activebackground="#00a8cc", activeforeground="#fff", width=10, bd=0)
        send_btn.pack(side=tk.RIGHT, padx=10, pady=13)

        self.display_bot_message("Hello! I'm your AI assistant powered by Groq's Llama 3.3 70B model. How can I help you today?")

    # === UI message functions ===
    def enter_pressed(self, event):
        if not event.state & 0x1:
            self.send_message()
            return "break"

    def display_user_message(self, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, "You\n", "user")
        self.chat_display.insert(tk.END, f"{message}\n\n", "msg_user")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def display_bot_message(self, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, "AI Assistant\n", "bot")
        self.chat_display.insert(tk.END, f"{message}\n\n", "msg_bot")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    # === Streaming response ===
    def send_message(self):
        user_message = self.user_input.get("1.0", tk.END).strip()
        if not user_message or self.is_streaming:
            return
        self.display_user_message(user_message)
        self.user_input.delete("1.0", tk.END)
        self.is_streaming = True
        threading.Thread(target=self.stream_groq_response, args=(user_message,), daemon=True).start()

    def stream_groq_response(self, user_message):
        try:
            self.root.after(0, lambda: self.display_bot_message("Thinking..."))
            stream = self.client.chat.completions.create(
                model=self.MODEL,
                messages=[
                    {"role": "system", "content": "You are a friendly and knowledgeable AI assistant."},
                    {"role": "user", "content": user_message}
                ],
                stream=True
            )

            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    text_chunk = chunk.choices[0].delta.content
                    full_response += text_chunk
                    self.root.after(0, lambda t=text_chunk: self.append_bot_stream(t))
            self.root.after(0, self.finish_bot_stream)

        except Exception as e:
            self.root.after(0, lambda: self.display_bot_message(f"⚠️ Error: {str(e)}"))
        finally:
            self.is_streaming = False

    def append_bot_stream(self, text):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, text, "msg_bot")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def finish_bot_stream(self):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, "\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

# Run standalone
if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateGroqChatbot(root)
    root.mainloop()
