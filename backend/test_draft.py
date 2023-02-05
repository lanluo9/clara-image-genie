model_path = r'D:\temp'.replace('\\', '/')

import wget
url = 'https://github.com/OlafenwaMoses/ImageAI/releases/download/3.0.0-pretrained/yolov3.pt/'
wget.download(url, model_path)