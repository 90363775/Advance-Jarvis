import cv2
import numpy as np
from PIL import Image #pillow package
import os

path = 'Jarvis-2025-master\\backend\\auth\\trainer\\samples' # Path for samples already taken

recognizer = cv2.face.LBPHFaceRecognizer_create() # Local Binary Patterns Histograms
detector = cv2.CascadeClassifier("Jarvis-2025-master\\backend\\auth\\haarcascade_frontalface_default.xml")
#Haar Cascade classifier is an effective object detection approach


def Images_And_Labels(path): # function to fetch the images and labels

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []

    for imagePath in imagePaths: # to iterate particular image path
        try:
            gray_img = Image.open(imagePath).convert('L') # convert it to grayscale
            img_arr = np.array(gray_img,'uint8') #creating an array

            # Extract filename and parse ID more robustly
            filename = os.path.split(imagePath)[-1]
            # Split by '.' and get the second part, but handle cases where it might not be a valid integer
            parts = filename.split(".")
            if len(parts) >= 2:
                id_part = parts[1]
                # Extract only the numeric part (ignore text like "copy")
                id_str = ''.join(filter(str.isdigit, id_part))
                if id_str:  # If we found digits
                    id = int(id_str)
                else:
                    print(f"Warning: Skipping file {filename} - no valid ID found")
                    continue
            else:
                print(f"Warning: Skipping file {filename} - invalid format")
                continue
                
            faces = detector.detectMultiScale(img_arr)

            for (x,y,w,h) in faces:
                faceSamples.append(img_arr[y:y+h,x:x+w])
                ids.append(id)
                
        except Exception as e:
            print(f"Error processing {imagePath}: {str(e)}")
            continue

    return faceSamples,ids

print ("Training faces. It will take a few seconds. Wait ...")

faces,ids = Images_And_Labels(path)
recognizer.train(faces, np.array(ids))

recognizer.write('Jarvis-2025-master\\backend\\auth\\trainer\\trainer.yml')  # Save the trained model as trainer.yml

print("Model trained, Now we can recognize your face.")
 