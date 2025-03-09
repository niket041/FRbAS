import os
import cv2
import face_recognition
import numpy as np
import pandas as pd
from datetime import datetime

# Define the student names and their corresponding image files
student_names = ['Rachit Dewangan', 'Aditi Sahu']
student_images = ['rachit.jpeg', 'aditi.jpeg']

# Path to save the attendance records
attendance_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"attendance_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx")

# Function to load and encode the images of students
def encode_images(image_files):
    encoded_list = []
    
    # Get the path to the image directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_path = os.path.join(script_dir, 'students_images')
    
    for image_file in image_files:
        # Check if the image file is in JPEG format
        if not image_file.lower().endswith(('.jpeg', '.jpg')):
            print(f"Error: {image_file} is not in JPEG format. Skipping.")
            continue
        
        image_path = os.path.join(images_path, image_file)
        print(f"Loading image from: {image_path}")
        
        # Check if the image file exists
        if not os.path.exists(image_path):
            print(f"Error: Image {image_file} not found at {image_path}. Please check the file path.")
            continue
        
        # Load image using OpenCV
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)  # Force color image read
        
        # Ensure the image was loaded successfully
        if img is None:
            print(f"Error: Failed to load image {image_file}.")
            continue
        
        # Convert to RGB explicitly
        if img.shape[2] == 4:  # Image with alpha channel (RGBA)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        elif img.shape[2] == 3:  # Standard RGB image
            if img.dtype != np.uint8:
                img_rgb = (img / 256).astype('uint8')
            else:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        else:
            print(f"Unknown image format for {image_file}. Skipping.")
            continue
        
        # Try to encode the image
        try:
            encodings = face_recognition.face_encodings(img_rgb)
            if len(encodings) > 0:
                encoded_list.append(encodings[0])
                print(f"Successfully encoded {image_file}")
            else:
                print(f"Error: No face found in {image_file}.")
        except Exception as e:
            print(f"Error encoding face for {image_file}: {e}")
    
    return encoded_list

# Encode known student images (only JPEG images are accepted)
encoded_known_faces = encode_images(student_images)

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialize a DataFrame to track attendance
attendance_df = pd.DataFrame(columns=["Name", "Time"])

# Function to mark attendance
def mark_attendance(name):
    global attendance_df
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    attendance_df = pd.concat([attendance_df, pd.DataFrame({"Name": [name], "Time": [current_time]})], ignore_index=True)
    print(f"Attendance marked for {name} at {current_time}")
    # Save the DataFrame to Excel
    attendance_df.to_excel(attendance_file_path, index=False)

# Set of names already processed to avoid multiple markings in short time
processed_names = set()

while True:
    success, frame = cap.read()
    if not success:
        print("Error: Failed to capture frame from webcam.")
        break

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    small_frame_rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect faces and encode them in the current frame
    faces_current_frame = face_recognition.face_locations(small_frame_rgb)
    encodes_current_frame = face_recognition.face_encodings(small_frame_rgb, faces_current_frame)

    # Compare the current face encodings with the known student encodings
    for encode_face, face_loc in zip(encodes_current_frame, faces_current_frame):
        matches = face_recognition.compare_faces(encoded_known_faces, encode_face)
        face_distance = face_recognition.face_distance(encoded_known_faces, encode_face)

        # Get the best match index
        match_index = np.argmin(face_distance)

        if matches[match_index]:
            name = student_names[match_index].upper()

            # Check if this name has already been processed
            if name not in processed_names:
                # Mark attendance
                mark_attendance(name)
                # Add name to the processed set
                processed_names.add(name)

            # Display the name on the webcam feed
            y1, x2, y2, x1 = face_loc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Display the webcam feed
    cv2.imshow('Webcam', frame)

    # Exit with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release webcam and close windows
cap.release()
cv2.destroyAllWindows()
