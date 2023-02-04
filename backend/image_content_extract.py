import os

app_dir = r'D:\repo\clara-image-genie'.replace('\\', '/')

image_dir = os.path.join(app_dir, 'test_images') # use test image for now. TODO: substitute with user input 1
search_type = 'object detection' # TODO: substitute with user input 2
query_str = 'cat' # TODO: substitute with user input 3


## get a list of all image files in the image folder. 
## possible extensions: .jpg, .jpeg, .png | future: add more extensions
image_file_list = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
# print(type(image_file_list))

## TODO: define functions to run models on images
def run_image_description(image_file):
    return 'image description cat'

def run_object_detection(image_file):
    return 'object detection cat'

def run_OCR(image_file):
    return 'OCR cat'


## loop through all image files, run corresponding model on image to get image content
image_content_list = []

for i, single_image in enumerate(image_file_list): # future: scaling - GPU parallelize batch process images in model
    print(i)
    print(single_image)

    if search_type == 'image description':
        image_content = run_image_description(single_image)
    elif search_type == 'object detection':
        image_content = run_object_detection(single_image)
    elif search_type == 'OCR':
        image_content = run_OCR(single_image)
    else:
        print('only support search type: image description, object detection, OCR')

    print(image_content)
    image_content_list.append(image_content)
    
    if i >= 4: # for now, only process 5 images. TODO: remove this line
        break


## calculate relevance between the image_content_list versus the keyword query_str
## for now, assume query_str is a single word. future: extend to multiple words
## for now, assume "relevance" is the number of times the query_str appears in the image_content string. future: extend to synonyms
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

