import cx_Freeze
import sys
import os
import cv2
import ttkbootstrap

base = None
if sys.platform == "win32":
    base = "Win32GUI"

cv2_data_path = os.path.join(os.path.dirname(cv2.__file__), 'data')
ttk_themes_path = os.path.join(os.path.dirname(ttkbootstrap.__file__), 'themes')

executables = [
    cx_Freeze.Executable(
        "Face_Recognition_Software.py",
        base=base,
        icon="face_recog icon.ico"
    )
]

build_exe_options = {
    "packages": [
        "tkinter",
        "ttkbootstrap",
        "PIL",
        "cv2",
        "mysql.connector",
        "numpy",
        "groq",
        "dotenv",
        "os",
        "sys"
    ],
    "include_files": [
        'face_recog icon.ico',
        'college images',
        'data',
        'database',
        'attendance_report',
        '.env',  
        (cv2_data_path, os.path.join('lib', 'cv2', 'data')),
        (ttk_themes_path, os.path.join('lib', 'ttkbootstrap', 'themes'))
    ],
    "includes": [
        "Face_Recognition_Software",
        "main",
        "student",
        "train",
        "face_recognition",
        "attendance",
        "chatbot",
        "help_desk"
    ],
    "excludes": [
        "unittest",
        "pydoc",
        "sqlite3",
        "http",
        "cv2.gapi"
    ]
}

cx_Freeze.setup(
    name="Facial Recognition Software",
    version="2.0",
    description="Face Recognition Automatic Attendance System | Developed By Raza",
    author="Raza",
    options={"build_exe": build_exe_options},
    executables=executables
)
