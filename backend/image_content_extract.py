import os

## get path and user input
app_dir = r'D:\repo\clara-image-genie'.replace('\\', '/')
image_dir = os.path.join(app_dir, 'test_images')
search_type = 'image description'
query_str = 'cat' # use test input for now, TODO: substitute image_dir, search_type, and query_str with user input 1-3


## get a list of all image files in the image folder. 
## possible extensions: .jpg, .jpeg, .png | future: add more extensions
image_file_list = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
image_file_list = image_file_list[:5] # test with 5 images. TODO: remove this line
# image_filename_list = [os.path.basename(image_file_path) for image_file_path in image_file_list] # only print file name, not the full path
# print(image_filename_list)


## TODO: cache the image content_list, so that we don't need to run the model on the same image again
## check if image has been cached. if yes, load the cached image content_list. if no, run the model on the image, and cache the image content_list


## TODO: define functions to run models on images
## each model receives the single_image file absolute path [str] as input, and returns the image content [str] as output
## future: list dependency on git repo. pip install the model package during app installation, and import the model package in model functions
from model_image_description import run_image_description
def run_object_detection(image_file_path):
    return 'object detection cat'
def run_OCR(image_file_path):
    return 'OCR cat'


## run corresponding model on the list of all images to get image content_list
if search_type == 'image description':
    image_content_list = run_image_description(image_file_list)
elif search_type == 'object detection':
    image_content_list = run_object_detection(image_file_list)
elif search_type == 'OCR':
    image_content_list = run_OCR(image_file_list)
else:
    print('only support search type: image description, object detection, OCR')
print(image_content_list)


## calculate relevance between the image_content_list versus the keyword query_str
## for now, assume query_str is a single word. future: extend to multiple words
## for now, assume "relevance" is the number of times the query_str appears in the image_content string. future: extend to synonyms, LLM word embedding distance
relevance_list = [image_content.count(query_str) for image_content in image_content_list]
# print(relevance_list)
relevance_list = [3,1,2,5,99] # test sorting. TODO: remove this line
# print(relevance_list)


## sort the image_file_list based on the relevance_list
image_file_list_sorted = [x for _,x in sorted(zip(relevance_list, image_file_list), reverse=True)]
# print(image_file_list[:5])
# print('\n')
# print(image_file_list_sorted)

## return the top 5 images
relevant_images_top5 = image_file_list_sorted[:5] # this is the output from the backend, send to frontend
print(relevant_images_top5)

