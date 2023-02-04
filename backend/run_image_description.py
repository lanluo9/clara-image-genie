def run_image_description(image_file_path):
    # pretrained model from https://huggingface.co/nlpconnect/vit-gpt2-image-captioning
    
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
    return preds # or test output: 'image description cat'



test1 = r'D:\repo\clara-image-genie\test_images\wren-meinberg-AL2-t0GrSko-unsplash.jpg'.replace('\\', '/')
test2 = r'D:\repo\clara-image-genie\test_images\sebastian-coman-travel-dtOTQYmTEs0-unsplash.jpg'.replace('\\', '/')
# # print(test_image_path)
# # from PIL import Image
# # Image.open(test_image_path)

image_content = run_image_description([test1, test2])
print('\n')
print(image_content)


# from transformers import pipeline
# image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
# output = image_to_text([test1, test2])
# # print(output)