# Django-Face-Authentication-System-OpenCV-Dlib
A Django-based Face Recognition Authentication System using OpenCV and dlib. Register users with facial images, capture facial features, and authenticate during login. Features real-time face capture, landmark detection, and secure database storage. Built with Django, OpenCV, dlib.

#Key Features:

1.User Registration: Register users by providing a unique username and uploading a facial image.
Real-time Face Capture: Utilize OpenCV for live facial image capture during registration and login.

2.Facial Landmark Detection: Apply dlib's shape predictor for accurate facial landmark detection.
Face Alignment: Use imutils for face alignment to enhance feature extraction consistency.

3.Database Storage: Securely store facial encodings in a Django database for quick retrieval.
Dynamic UI: Responsive user interface for a seamless and intuitive experience.

4.Login Process:
-Users submit their username and password.
-Real-time facial features are captured using the device camera.
-Extracted features are compared with stored encodings for user authentication.
-Feedback provided on successful or failed logins.

#Technologies:

Django: Web framework for building the backend and managing user data.
OpenCV: Computer vision library for capturing and processing facial images.
dlib: Library for facial landmark detection and alignment.
imutils: Utility functions for image processing and face alignment.
Python: Programming language used for the backend logic

#Note: Before running the system, ensure that the required dependencies are installed, including dlib, OpenCV, and Django.Check" installed_packages2.txt ".
