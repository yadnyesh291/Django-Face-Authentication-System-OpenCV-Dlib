# libraries are imported which are essentail for face recognition system.
from django.shortcuts import render,redirect ,reverse
import cv2
import numpy as np
import os
import dlib
from imutils import face_utils
from imutils.face_utils import FaceAligner
from django.contrib import messages
from face_recognition.models import UserProfile
from .forms import UserProfileForm
from fr_utils import *
from scipy.spatial import distance
from imutils import face_utils
from django.conf import settings
import face_recognition
import pickle




# different function are created for the
def index(request):
    return render(request, 'face_recognition/index.html')
def home(request):
    return render(request, 'face_recognition/home.html')


#function is created naming it as register and requets method is there post

def register(request):
    if request.method == 'POST':
        # Get the form data
        form = UserProfileForm(request.POST, request.FILES)

        username = form['username'].value()
        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return render(request, 'face_recognition/register.html')
        
        form.save()
        messages.success(request, ('You are successfully registered'))
        

        # Detector function will get the frontal face 
        detector = dlib.get_frontal_face_detector()
        shape_predictor_path = os.path.join(settings.BASE_DIR, 'resources', 'shape_predictor_68_face_landmarks.dat')
        shape_predictor = dlib.shape_predictor(shape_predictor_path)
        face_aligner = FaceAligner(shape_predictor, desiredFaceWidth=200) 

        # Opens the video frame
        video_capture = cv2.VideoCapture(0) 
        # Username will be there before saving the image 
        name = request.POST.get('username')
        # Path where the image and encoding will be saved
        path = 'images'
        directory = os.path.join(path, name)

        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok='True')

        # Maximum number of images
        MAX_NUMBER_OF_IMAGES = 1
        count = 0

        # Save face encodings during registration
        encodings = []

        while count < MAX_NUMBER_OF_IMAGES:
            ret, frame = video_capture.read()

            frame = cv2.flip(frame, 1)
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = detector(frame_gray)

            if len(faces) == 1:
                face = faces[0]
                (x, y, w, h) = face_utils.rect_to_bb(face)
                face_img = frame_gray[y-50:y+h-100, x-50:x + w+100]
                face_aligned = face_aligner.align(frame, frame_gray, face)

                if count == 4:
                    # Save the encoding during the last iteration
                    landmarks = shape_predictor(face_img, face)
                    encoding = [landmarks.part(i).x for i in range(68)] + [landmarks.part(i).y for i in range(68)]
                    encodings.append(encoding)

                    cv2.imwrite(os.path.join(directory, f"{name}_{count}.jpg"), face_aligned)
                    count += 1
                    break

                landmarks = shape_predictor(face_img, face)
                encoding = [landmarks.part(i).x for i in range(68)] + [landmarks.part(i).y for i in range(68)]
                encodings.append(encoding)

                cv2.imwrite(os.path.join(directory, f"{name}_{count}.jpg"), face_aligned)

                count += 1

            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

         # Get the UserProfile for the given username
        user_profiles = UserProfile.objects.filter(username=name)

        # Check if a UserProfile with the given username exists
        if user_profiles.exists():
            # Take the first result ( usernames are unique)
            user_profile = user_profiles.first()

            # Save the encodings to the database
            user_profile.face_encoding = pickle.dumps(encodings)
            user_profile.save()
        else:
            # Handle the case where no UserProfile with the given username exists
            user_profile = None  # Adjust this based on requirements

        video_capture.release()
        cv2.destroyAllWindows()
        return redirect('login')

    return render(request, 'face_recognition/register.html')


def login(request):
    # Method is POST
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_profile = UserProfile.objects.filter(username=username, password=password).first()
        
        # If username and password are correct
        if user_profile:
            detector = dlib.get_frontal_face_detector()
            shape_predictor_path = os.path.join('resources', 'shape_predictor_68_face_landmarks.dat')
            shape_predictor = dlib.shape_predictor(shape_predictor_path)
            face_database = load_face_database()

            video_capture = cv2.VideoCapture(0)

            while True:
                ret, frame = video_capture.read()
                if not ret:
                   break

                frame = cv2.flip(frame, 1)
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                print("Frame gray type:", type(frame_gray))
                print("Frame gray shape:", frame_gray.shape)
    
                faces = detector(frame_gray)
                
                print("Frame type:", type(frame))
                print("Frame shape:", frame.shape)

                for face in faces:
                    (x, y, w, h) = face_utils.rect_to_bb(face)
                    roi = frame[y:y + h, x:x + w]
                    landmarks = shape_predictor(roi, face)

                    encoding = [landmarks.part(i).x for i in range(68)] + [landmarks.part(i).y for i in range(68)]
                    encoding = np.array(encoding).flatten().astype(int)
                    if encoding.any():
                        video_capture.release()
                        cv2.destroyAllWindows()

                    # Compare with the saved encodings during registration
                    saved_encodings = user_profile.face_encoding
                    saved_encodings_decoded = pickle.loads(saved_encodings)
                    saved_encodings_np = np.array(saved_encodings_decoded, dtype=int)
                    saved_encodings_np = np.array(saved_encodings_np).flatten()
                    

                    if saved_encodings_np.any():
                        #saved_encodings_np = list(saved_encodings_np)
                        min_distance = distance.euclidean(saved_encodings_np, encoding)

                        # Compare the minimum distance with a threshold
                        if min_distance < 300:
                            messages.success(request, 'Face recognized! Login successful.')
                            return render(request, 'face_recognition/thankyou.html', {})
                        else:
                            messages.error(request, 'Face not recognized. Login failed.')
                            break
                
                #Saving the image during Login
                form = UserProfileForm(request.POST, request.FILES)
                name = form['username'].value()

                cv2.imshow('Captured Frame', frame)
    
                # Save the captured frame to the 'login_image' folder
                login_image_folder = 'login_image'
                if not os.path.exists(login_image_folder):
                    os.makedirs(login_image_folder)
    
                image_path = os.path.join(login_image_folder, f"{name}_captured_frame.jpg")
                cv2.imwrite(image_path, frame)

                break                         
            video_capture.release()
            cv2.destroyAllWindows()
            

    return render(request, 'face_recognition/index.html', {})

def load_face_database():
    face_database = {}
    path = 'images'

    # Load the shape predictor model used in the registration process
    shape_predictor_path = os.path.join('resources', 'shape_predictor_68_face_landmarks.dat')
    shape_predictor = dlib.shape_predictor(shape_predictor_path)

    for user_name in os.listdir(path):
        user_directory = os.path.join(path, user_name)

        if os.path.isdir(user_directory):
            face_encodings = []

            for image_file in os.listdir(user_directory):
                image_path = os.path.join(user_directory, image_file)

                # Load image using cv2
                image = cv2.imread(image_path)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Detect faces using dlib
                detector = dlib.get_frontal_face_detector()
                faces = detector(gray)

                if faces:
                    # Use the first detected face (only one face per image)
                    face = faces[0]

                    # Detect facial landmarks using the shape predictor model
                    landmarks = shape_predictor(gray, face)

                    # Extract facial features
                    encoding = [float(landmarks.part(i).x) for i in range(68)] + [float(landmarks.part(i).y) for i in range(68)]

                    face_encodings.append(encoding)

            if face_encodings:
                face_database[user_name] = face_encodings

    return face_database    

        
   

