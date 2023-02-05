def run_image_description(image_file_path):
    # pretrained model from https://huggingface.co/nlpconnect/vit-gpt2-image-captioning
    # TODO: use https://huggingface.co/spaces/laion/CoCa & https://github.com/mlfoundations/open_clip
    
    from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
    import torch
    from PIL import Image

    model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    max_length = 16
    num_beams = 4
    gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

    def predict_step(image_paths):
        images = []
        for image_path in image_paths:
            i_image = Image.open(image_path)
            if i_image.mode != "RGB":
                i_image = i_image.convert(mode="RGB")
            images.append(i_image)

        pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(device)
        output_ids = model.generate(pixel_values, **gen_kwargs)

        preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        preds = [pred.strip() for pred in preds]
        return preds

    preds = predict_step(image_file_path)
    return preds # this is `image_content_list`, or use test output: 'image description cat'


# ## test case
# test1 = r'D:\repo\clara-image-genie\test_images\wren-meinberg-AL2-t0GrSko-unsplash.jpg'.replace('\\', '/')
# test2 = r'D:\repo\clara-image-genie\test_images\sebastian-coman-travel-dtOTQYmTEs0-unsplash.jpg'.replace('\\', '/')
# image_content_list = run_image_description([test1, test2])
# # print('\n')
# # print(type(image_content_list))
# # print(image_content_list)


## a shorter version of the above code, but for some reason gets lower accuracy
# from transformers import pipeline
# image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
# output = image_to_text([test1, test2])
# print(output)

###################

def run_OCR(image_file_list):
    # https://github.com/JaidedAI/EasyOCR
    import easyocr
    reader = easyocr.Reader(['en']) # need to run only once to load model into memory

    print('model ready, start OCR')
    results = []
    for image_file_path in image_file_list:
        result = reader.readtext(image_file_path) #returns a list of lists where each element has the bounding box coordinates as the 0th element, the word as the 1st, and the confidence of interpreting that word correctly as the 2nd 
        # just_words = [(value[1], value[2])  for value in result] #only get the words
        # if len(just_words) == 0:
        #     just_words = (['No-text-in-this-image'], 0.5)
        just_words = str([value[1] for value in result]).replace(",", '') # prevent csv from splitting OCR text with commas
        # print(just_words)
        if len(just_words) == 0:
            just_words = ('No-text-in-this-image')
        results.append(just_words)
    # print(results) # Returns a list of lists where each sublist corresponds to an image and contains tuples of words in the image with associated probabilities for each word
    return results

###################

def run_object_detection(image_file_list):
    # https://github.com/OlafenwaMoses/ImageAI
    from imageai.Detection import ObjectDetection
    import os

    execution_path = os.getcwd()
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(os.path.join(execution_path , "yolov3.pt"))
    detector.loadModel()

    results = []
    for image_file_path in image_file_list:
        detections = detector.detectObjectsFromImage(input_image=image_file_path, minimum_percentage_probability=30)
        curr_img_objects = []
        for eachObject in detections:
            # curr_img_objects.append((eachObject["name"], eachObject["percentage_probability"]))
            curr_img_objects.append(eachObject["name"])
        results.append(curr_img_objects)
    # print(results) # Returns a list of lists where each sublists corresponds to an image and contains tuples of items in the image with associated probabilities for each item
    return results