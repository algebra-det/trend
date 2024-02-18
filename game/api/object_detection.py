from django.conf import settings

import cv2
import base64
import numpy as np
import tensorflow as tf


# For Production Server
# model_tf_path = "/home/django/trend/game/api/models/ObjectDetection/saved_model"

# For Development
model_tf_path = str(settings.BASE_DIR / "game/api/models/ObjectDetection/saved_model")



class ObjectDetector:
    model = None
    model_tf = None

    category_index = {
        1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane',
        6: 'bus', 7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light',
        11: 'fire hydrant', 13: 'stop sign', 14: 'parking meter', 15: 'bench',
        16: 'bird', 17: 'cat', 18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow',
        22: 'elephant', 23: 'bear', 24: 'zebra', 25: 'giraffe', 27: 'backpack',
        28: 'umbrella', 31: 'handbag', 32: 'tie', 33: 'suitcase', 34: 'frisbee',
        35: 'skis', 36: 'snowboard', 37: 'sports ball', 38: 'kite', 39: 'baseball bat',
        40: 'baseball glove', 41: 'skateboard', 42: 'surfboard', 43: 'tennis racket',
        44: 'bottle', 46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon',
        51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange',
        56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut',
        61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed',
        67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',
        75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven',
        80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock',
        86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush'
    }

    def __init__(self):
        ObjectDetector.load_model_tf()
        # ObjectDetector.test_model()

    @staticmethod
    def load_model_tf():
        if not ObjectDetector.model_tf:
            ObjectDetector.model_tf = tf.saved_model.load(model_tf_path)

    @staticmethod
    def test_model():
        print("Initializing Object Detector")

        # For Production Server
        # img = cv2.imread('/home/django/trend/game/api/models/test.jpg')

        # For Development Server
        img = cv2.imread(str(settings.BASE_DIR / '/game/api/models/test.jpg'))
        
        ObjectDetector.detect_image_tf(img)

    @staticmethod
    def is_base64(s):
        try:
            s = bytes(s, encoding='utf-8')
            return base64.b64encode(base64.b64decode(s)) == s
        except Exception:
            return False

    @staticmethod
    def base64_to_image(base64_img):
        try:
            if not ObjectDetector.is_base64(base64_img):
                return False, None
            img_data = bytes(base64_img, encoding='utf-8')
            jpg_original = base64.b64decode(img_data)
            jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
            img = cv2.imdecode(jpg_as_np, flags=1)
            return True, img
        except Exception:
            return False, None

    @staticmethod
    def image_to_base64(image):
        _, buffer = cv2.imencode('.jpg', image)
        base64_string = str(base64.b64encode(buffer))[2:-1]
        return base64_string

    @staticmethod
    def detect_image_tf(img, class_to_detect=None):
        (h, w) = img.shape[:2]
        input_tensor = np.expand_dims(img, 0)
        result = ObjectDetector.model_tf(input_tensor)

        boxes = result['detection_boxes'][0]
        classes = (result['detection_classes'][0].numpy()).astype(int)
        scores = result['detection_scores'][0]

        labels = {}

        for i in range(len(scores)):

            if scores[i] > 0.6:
                detected_class = ObjectDetector.category_index[classes[i]]
                if detected_class == class_to_detect:
                    top, left, bottom, right = boxes[i].numpy()
                    left, right = left * w, right * w
                    top, bottom = top * h, bottom * h

                    # BGR
                    cv2.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), (23, 230, 210), thickness=2)
                    labels[tuple(boxes[i].numpy())] = ObjectDetector.category_index[classes[i]]

        # cv2.imwrite("string of path", img)
        img = "data:image/jpeg;base64," + ObjectDetector.image_to_base64(img)
        return labels, img


def get_image_detection(image, class_to_detect=None):
    # ret, image = ObjectDetector.base64_to_image(image)
    # if not ret:
    #     return False, None
    npimg = np.frombuffer(image, np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR) 

    response = ObjectDetector.detect_image_tf(image, class_to_detect)

    return response


ObjectDetector()
