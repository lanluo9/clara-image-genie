def img2text(search_type, query_str):
    import os # no install, built-in
    os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
    import numpy as np
    import pandas as pd
    from itertools import compress # no install, built-in


    ## get path and user input
    app_dir = r'D:\repo\clara-image-genie'.replace('\\', '/')
    image_dir = os.path.join(app_dir, 'app/mysite/images').replace('\\', '/')
    # image_dir = r'D:\repo\clara-image-genie\archive-deprecated\test_images'.replace('\\', '/') # test cache across folders: it works
    # search_type = 'OCR'
    # query_str = 'cat' # use test input for now, TODO: substitute image_dir, search_type, and query_str with user input 1-3
    query_str = query_str.lower().strip() # convert to lower case and remove white space


    ## get a list of all image files in the image folder. 
    ## possible extensions: .jpg, .jpeg, .png | future: add more extensions
    image_file_list = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    # image_file_list = image_file_list[:7] # test with n images. TODO: remove this line
    image_filename_list = [os.path.basename(image_file_path) for image_file_path in image_file_list] # only print file name, not the full path
    print(image_filename_list)


    ## initialize model_cache.csv to cache the image_content_list, if not exist
    model_cache_dir = os.path.join(app_dir, 'model_cache')
    if not os.path.exists(model_cache_dir):
        os.makedirs(model_cache_dir)
    model_cache_csv = os.path.join(model_cache_dir, 'model_cache.csv') # save image_content_list in csv file
    # print(model_cache_csv)
    if not os.path.exists(model_cache_csv):
        with open(model_cache_csv, 'w', newline='') as f:
            f.write('image_file_path,image_content,content_type\n')
            f.write('init_img,init_content,init_type\n') # note there should be no white space after the comma


    ## if some img in image_file_list exist in cache of corresponding search_type, retrieve image_content from cache
    df = pd.read_csv(model_cache_csv)
    # print(df)
    # search_type = 'init_type'; image_file_list[0] = 'init_img'
    # print(image_file_list)
    cached_bool = np.zeros(len(image_file_list), dtype=bool)
    image_content_cached = [None] * len(image_file_list) # use filename to determine if the image is cached, instead of the full path. now cache works even if img folder changes
    for i, image_file_path in enumerate(image_file_list):
        image_file_name = os.path.basename(image_file_path)
        if ((image_file_path in df[df.content_type == search_type].image_file_path.values)
                | (not df[df.content_type == search_type].image_file_path.str.contains(image_file_name).empty)
                ):
            cached_bool[i] = True
            image_content_cached[i] = df[(df.image_file_path.str.contains(image_file_name)) # future: use full path to avoid namesake
                                        & (df.content_type == search_type)].image_content.values[0]
    # print(df[df.content_type == search_type].image_file_path.values)
    print('not cached_bool: ', ~cached_bool)
    # print(image_content_cached)
    # print(list(compress(image_file_list, ~cached_bool))) # boolean indexing to get the list of uncached images
    image_cached_list = list(compress(image_file_list, cached_bool))
    image_uncached_list = list(compress(image_file_list, ~cached_bool))


    ## run corresponding model on the list of uncached images to get image_content_list, then save to model_cache.csv
    ## each model receives the single_image file absolute path [str] as input, and returns the image content [str] as output
    ## future: list dependency on git repo. pip install the model package during app installation, and import the model package in model functions
    if len(image_uncached_list) == 0:
        print('all images are cached')
        image_content_uncached = []
    else:
        if (search_type == 'image description'): # or (search_type == 'init_type'):
            from model_run import run_image_description
            image_content_uncached = run_image_description(image_uncached_list) # run model on uncached images
        elif search_type == 'object detection':
            from model_run import run_object_detection
            model_path = os.path.join(app_dir, 'backend/yolov3.pt')
            if not os.path.exists(model_path):
                import wget
                url = 'https://github.com/OlafenwaMoses/ImageAI/releases/download/3.0.0-pretrained/yolov3.pt/'
                wget.download(url, model_path)
            image_content_uncached = run_object_detection(image_uncached_list, model_path)
        elif search_type == 'OCR':
            from model_run import run_OCR
            image_content_uncached = run_OCR(image_uncached_list)
            query_str = ' ' + query_str # pad query_str with white space to avoid partial match with OCR. future: improve
        else:
            print('only support search type: image description, object detection, OCR')
    # print(image_content_cached)
    print(image_content_uncached)


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
    # image_filename_list = [os.path.basename(image_file_path) for image_file_path in image_file_list] # only print file name, not the full path
    # print(image_filename_list)


    ## calculate relevance between the image_content_list versus the keyword query_str
    ## for now, assume query_str is a single word. future: extend to multiple words
    ## for now, assume "relevance" is the number of times the query_str appears in the image_content string. future: extend to synonyms, LLM word embedding distance
    relevance_list = [image_content.count(query_str) for image_content in image_content_list]
    print('relevance_list: ', relevance_list)


    ## sort the image_file_list based on the relevance_list
    image_file_list_sorted = [x for _,x in sorted(zip(relevance_list, image_file_list), reverse=True)]
    relevance_arr = np.array(sorted(relevance_list, reverse=True)) # relevance should also be sorted in descending order to match the sorted image_file_list
    # print(relevance_arr)
    image_file_list_sorted = list(compress(image_file_list_sorted, relevance_arr>0)) # remove images with relevance = 0
    # print(image_file_list_sorted)
    # print(image_filename_list[:5])
    # print('\n')


    ## return the top n images
    top_n = 10 # only display top n images
    if len(image_file_list_sorted) <= top_n:
        relevant_images_top = image_file_list_sorted
    else:
        relevant_images_top = image_file_list_sorted[:top_n] # this is the output from the backend, send to frontend
    print('\n')
    print(relevant_images_top) # an list of strings, each string is the absolute path of the image file


    # ## change to relative path -> migrated to top of the file
    # relevant_images_top = [os.path.basename(image_file_path) for image_file_path in relevant_images_top] # only print file name, not the full path
    # relevant_images_top = [os.path.join(django_img_dir, image_file_path) for image_file_path in relevant_images_top] # add the django image directory to the file name
    # print(relevant_images_top)

    return relevant_images_top