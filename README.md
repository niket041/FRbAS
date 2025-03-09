Overview
The Face Recognition-based Attendance System (FRbAS) is an AI-powered solution designed to automate attendance marking using face recognition technology. Built with Python, OpenCV, and face_recognition library, this project efficiently identifies individuals and records their attendance with timestamped entries.

Features
Automated Attendance Marking: Uses facial recognition to identify and log attendance.

Real-time Detection: Captures and processes faces directly via webcam.

Excel Sheet Generation: Automatically generates and updates an Excel file with attendance records.

Timeout Mechanism: Prevents multiple entries for the same individual within a short period.

Error Handling: Ensures smooth execution by addressing common issues like webcam closure errors and file conflicts.

Technologies Used
Python

OpenCV

face_recognition

Pandas

Excel Automation

Installation
Clone the repository:

git clone https://github.com/niket041/FRbAS
cd FRbAS
Install dependencies:

pip install opencv-python face_recognition pandas
Run the program:

python attendance.py
How to Use
Ensure your webcam is connected and functional.

Run attendance.py to launch the system.

The system will detect faces and mark attendance automatically.

Attendance will be recorded in an Excel file named with the current date.

Troubleshooting
Webcam Issues: Ensure no other applications are accessing the webcam.

Excel File Errors: Check for file permissions or naming conflicts.

Recognition Errors: Ensure proper lighting and camera angle for optimal accuracy.

Future Enhancements
Integration with a database for better data management.

Improved UI for enhanced user experience.

Multi-camera support for large classrooms or office environments.

License
This project is licensed under the MIT License. Feel free to modify and expand the project as needed.

Contact
For further queries or contributions, contact Niket Sah.
