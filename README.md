# NEAMAT_KOUR
Process Management System Call Wrapper (Windows)

This project demonstrates how process management system calls work in a Windows environment using Python. It wraps important process-related operations through a simplified interface so that users can interact easily without directly calling system-level APIs.

The system allows users to:

Create a new process

Monitor and control running processes

Terminate active processes

Retrieve and display process details

This project is mainly for learning and understanding how the operating system handles tasks and processes.

Features

✔ Process creation using Windows system calls
✔ View running process list with Process ID (PID)
✔ Terminate a selected process by PID
✔ User-friendly menu/GUI/CLI through frontend
✔ Backend functions with proper exception handling

 Implementation Details

This project is implemented in Python using modules like:

os

subprocess

psutil (if used for process info)

It consists of:

Backend file (backend.py)
Contains wrapper functions for process creation, listing, and termination.

Frontend file (frontend.py)
Provides user interaction (menu-based or GUI) and calls backend functions.

Workflow

User selects a process action on frontend

Frontend sends request to backend wrapper functions

Backend executes system call and returns results
Future Enhancements

🔹 Show CPU & memory usage per process
🔹 Advanced GUI dashboard
🔹 Logging and analytics for process history
🔹 Multi-process management features

Future Enhancements

🔹 Show CPU & memory usage per process
🔹 Advanced GUI dashboard
🔹 Logging and analytics for process history
🔹 Multi-process management features
