import os
import numpy as np
import pandas as pd
from itertools import compress

## get path and user input
app_dir = r'D:\repo\clara-image-genie'.replace('\\', '/')
image_dir = os.path.join(app_dir, 'test_images')
search_type = 'image description'
query_str = 'cat' # use test input for now, TODO: substitute image_dir, search_type, and query_str with user input 1-3


## get a list of all image files in the image folder. 
## possible extensions: .jpg, .jpeg, .png | future: add more extensions
image_file_list = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
image_file_list = image_file_list[:10] # test with n images. TODO: remove this line
# image_filename_list = [os.path.basename(image_file_path) for image_file_path in image_file_list] # only print file name, not the full path
# print(image_filename_list)


## initialize model_cache.csv to cache the image_content_list, if not exist
model_cache_dir = os.path.join(app_dir, 'model_cache')
if not os.path.exists(model_cache_dir):
    os.makedirs(model_cache_dir)
model_cache_csv = os.path.join(model_cache_dir, 'model_cache.csv') # save image_content_list in csv file
# print(model_cache_csv)
if not os.path.exists(model_cache_csv): # TODO: uncomment this line
    with open(model_cache_csv, 'w', newline='') as f:
        f.write('image_file_path,image_content,content_type\n')
        f.write('init_img,init_content,init_type\n') # note there should be no white space after the comma


## if some img in image_file_list exist in cache of corresponding search_type, retrieve image_content from cache
df = pd.read_csv(model_cache_csv)
# print(df)
# search_type = 'init_type'; image_file_list[0] = 'init_img'
# print(image_file_list)

cached_bool = np.zeros(len(image_file_list), dtype=bool)
image_content_cached = [None] * len(image_file_list)
for i, image_file_path in enumerate(image_file_list):
    if image_file_path in df[df.content_type == search_type].image_file_path.values:
        cached_bool[i] = True
        image_content_cached[i] = df[(df.image_file_path == image_file_path) & (df.content_type == search_type)].image_content.values[0]
# print(df[df.content_type == search_type].image_file_path.values)
print(~cached_bool)
# print(image_content_cached)
# print(list(compress(image_file_list, ~cached_bool))) # boolean indexing to get the list of uncached images
image_cached_list = list(compress(image_file_list, cached_bool))
image_uncached_list = list(compress(image_file_list, ~cached_bool))


## TODO: import functions from .py to run models on images
def run_object_detection(image_file_path):
    return 'object detection cat'
def run_OCR(image_file_path):
    return 'OCR cat'


## run corresponding model on the list of uncached images to get image_content_list, then save to model_cache.csv
## each model receives the single_image file absolute path [str] as input, and returns the image content [str] as output
## future: list dependency on git repo. pip install the model package during app installation, and import the model package in model functions
if len(image_uncached_list) == 0:
    print('all images are cached')
    image_content_uncached = []
else:
    if (search_type == 'image description'): # or (search_type == 'init_type'):
        from model_image_description import run_image_description
        image_content_uncached = run_image_description(image_uncached_list) # run model on uncached images
    elif search_type == 'object detection':
        image_content_uncached = run_object_detection(image_uncached_list)
    elif search_type == 'OCR':
        image_content_uncached = run_OCR(image_uncached_list)
    else:
        print('only support search type: image description, object detection, OCR')
# print(image_content_cached)
# print(image_content_uncached)


## save image_content_uncached to cache
with open(model_cache_csv, 'a', newline='') as f:
    for i, image_file_path in enumerate(image_uncached_list):
        f.write(image_file_path + ',' + image_content_uncached[i] + ',' + search_type + '\n')


## fill in where image_content_cached is None with image_content_list
image_content_list = []
uncached_counter = 0
for i in range(len(image_content_cached)):
    if image_content_cached[i] is None:
        image_content_list.append(image_content_uncached[uncached_counter])
        uncached_counter += 1
    else:
        image_content_list.append(image_content_cached[i])
# print(image_content_list)
image_filename_list = [os.path.basename(image_file_path) for image_file_path in image_file_list] # only print file name, not the full path
print(image_filename_list)


## calculate relevance between the image_content_list versus the keyword query_str
## for now, assume query_str is a single word. future: extend to multiple words
## for now, assume "relevance" is the number of times the query_str appears in the image_content string. future: extend to synonyms, LLM word embedding distance
relevance_list = [image_content.count(query_str) for image_content in image_content_list]
print(relevance_list)


## sort the image_file_list based on the relevance_list
image_file_list_sorted = [x for _,x in sorted(zip(relevance_list, image_file_list), reverse=True)]
relevance_arr = np.array(sorted(relevance_list, reverse=True)) # relevance should also be sorted in descending order to match the sorted image_file_list
# print(relevance_arr)
image_file_list_sorted = list(compress(image_file_list_sorted, relevance_arr>0)) # remove images with relevance = 0
# print(image_file_list_sorted)
# print(image_filename_list[:5])
# print('\n')


## return the top n images
if len(image_file_list_sorted) < 10:
    relevant_images_top = image_file_list_sorted
else:
    relevant_images_top = image_file_list_sorted[:10] # this is the output from the backend, send to frontend
print('\n')
print(relevant_images_top)

