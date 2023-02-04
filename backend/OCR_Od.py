#Incorporate this chunk of code into the image_content_extract.py
#This code uses the following libraries: 
# https://github.com/JaidedAI/EasyOCR
# https://github.com/OlafenwaMoses/ImageAI
import os

import easyocr
from imageai.Detection import ObjectDetection


#Returns a list of lists where each sublist corresponds to an image and contains tuples of words in the image with associated probabilities for each word
def run_OCR(image_file_list, reader):
    results = []
    for image_file_path in image_file_list:
        result = reader.readtext(image_file_path) #returns a list of lists where each element has the bounding box coordinates as the 0th element, the word as the 1st, and the confidence of interpreting that word correctly as the 2nd 
        just_words = [(value[1], value[2])  for value in result] #only get the words
        if len(just_words) == 0:
            just_words = (['No text in this image'], 0.5)
        results.append(just_words)
    return results


#Returns a list of lists where each sublists corresponds to an image and contains tuples of items in the image with associated probabilities for each item
def run_object_detection(image_file_list, detector):
    results = []
    for image_file_path in image_file_list:
        detections = detector.detectObjectsFromImage(input_image=image_file_path, minimum_percentage_probability=30)
        curr_img_objects = []
        for eachObject in detections:
            curr_img_objects.append((eachObject["name"], eachObject["percentage_probability"]))
        results.append(curr_img_objects)
    return results


if __name__ == '__main__':
    # this needs to run only once to load the OCR model into memory
    reader = easyocr.Reader(['en']) 

    execution_path = os.getcwd()
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(os.path.join(execution_path , "yolov3.pt"))
    detector.loadModel()

    #example call:
    print(image_file_list[:4]) # print the images being used
    image_file_list = [os.path.join('/Users/kirill/Desktop/test_images/', f) for f in os.listdir('/Users/kirill/Desktop/test_images/') if f.endswith(('.jpg', '.jpeg', '.png'))]
    print(image_file_list[:4])

    #Test OCR
    OCR_results = run_OCR(image_file_list[:4], reader)
    print(OCR_results)

    #Test object detection
    object_detection_results = run_object_detection(image_file_list[:4], detector)
    print(object_detection_results)
