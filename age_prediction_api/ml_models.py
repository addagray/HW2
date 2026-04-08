import cv2
import numpy as np
import os
import urllib.request

# URLs for the pre-trained Caffe models
FACE_PROTO = "https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt"
FACE_MODEL = "https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel"
AGE_PROTO = "https://raw.githubusercontent.com/GilLevi/AgeGenderDeepLearning/master/age_net_definitions/deploy.prototxt"
AGE_MODEL = "https://raw.githubusercontent.com/GilLevi/AgeGenderDeepLearning/master/models/age_net.caffemodel"

MODEL_DIR = "models"
AGE_LIST = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

class AgePredictor:
    def __init__(self):
        self._download_models()
        self.face_net = cv2.dnn.readNetFromCaffe(
            os.path.join(MODEL_DIR, "face_deploy.prototxt"), 
            os.path.join(MODEL_DIR, "face_net.caffemodel")
        )
        self.age_net = cv2.dnn.readNetFromCaffe(
            os.path.join(MODEL_DIR, "age_deploy.prototxt"), 
            os.path.join(MODEL_DIR, "age_net.caffemodel")
        )

    def _download(self, url, filename):
        filepath = os.path.join(MODEL_DIR, filename)
        if not os.path.exists(filepath):
            print(f"Downloading {filename}...")
            urllib.request.urlretrieve(url, filepath)

    def _download_models(self):
        os.makedirs(MODEL_DIR, exist_ok=True)
        self._download(FACE_PROTO, "face_deploy.prototxt")
        self._download(FACE_MODEL, "face_net.caffemodel")
        self._download(AGE_PROTO, "age_deploy.prototxt")
        self._download(AGE_MODEL, "age_net.caffemodel")

    def predict_age(self, image_bytes):
        # Decode the image from bytes
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Invalid image or unreadable format")

        h, w = img.shape[:2]
        
        # 1. Face Detection
        blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), (104.0, 177.0, 123.0))
        self.face_net.setInput(blob)
        detections = self.face_net.forward()

        face_boxes = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.7:  # Threshold
                x1 = int(detections[0, 0, i, 3] * w)
                y1 = int(detections[0, 0, i, 4] * h)
                x2 = int(detections[0, 0, i, 5] * w)
                y2 = int(detections[0, 0, i, 6] * h)
                face_boxes.append((x1, y1, x2, y2))
        
        if not face_boxes:
            return None

        # Predict age for the first face detected
        x1, y1, x2, y2 = face_boxes[0]
        padding = 20
        face_img = img[max(0, y1-padding):min(y2+padding, h-1), max(0, x1-padding):min(x2+padding, w-1)]
        
        if face_img.size == 0:
            return None

        # 2. Age Prediction
        blob = cv2.dnn.blobFromImage(face_img, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        self.age_net.setInput(blob)
        age_preds = self.age_net.forward()
        age_index = age_preds[0].argmax()
        predicted_age = AGE_LIST[age_index]

        return predicted_age
