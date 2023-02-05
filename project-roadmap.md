we will test our app on this `test_images` folder

---

what happens in the front end:  

[data privacy note: all data must remain local. our app, especialy the django part, should not connect to the internet]

- receive user input 1: let user select a folder of images that they want to search in  
	- when testing our app, this folder is always the `test_images` folder 
	- pass user input 1 as a string of folder directory to back end

- receive user input 2: a button push indicating which kind of search user wants to do
	- button 1: "image description" (alt text for blind users)
	- button 2: "object detection"
	- button 3: "OCR"
	- pass user input 2 as a string to back end
	
- receive user input 3: a query dictating what the user wants to search for  
	- pass user input 3 as a string to back end
	
- wait for back end to return output
	- output will be an array of strings
	- each string in the arrays is the absolute path of an image relevant to the search query from user
	- the array of string has been sorted by relevance based on image content 1-3, depending on which button the user pushed (user input 2) 
		
- make UI exhibit the images corresponding to the image paths in the output

---

what happens in the back end: 

[data privacy note: all data must remain local. our app should not connect to the internet, and all models were pretrained and offline]

- receive front end user input 1: folder directory as a string
	- when testing our app, this folder is always the `test_images` folder  

- receive user input 2: which kind of search user wants to do, as a string. possible inputs include:
	- "image description" (alt text for blind users)
	- "object detection"
	- "OCR"
	
- index all images in this folder. for each image, run one of these following model, depending on user input 2
	- run object recognition model, or
	- run OCR model, or
	- run alt text / image description generation model
	
- build dataframe, containing columns of
	- image path: absolute path of each image in this folder
	- image content detected by model, depending on user input 2
	- (all columns only contain strings)
	
- receive front end user input 3: keyword query as a string
- calculate relevance between the "image content" columns versus the keyword query
	- sort "image path" by relevance based on "image content" columns
	- only keep the top n images (let's start with n=10)
	- return the sorted "image path" column as an array of strings to the front end
		- the array of string has been sorted by relevance based on "image content"
	
---

what happens when front end and back end talk to each other

1. front end 
	- receive user input 1, navigate in the file explorer to select by clicking: let user select a folder of images that they want to search in  
	- receive user input 2, a button push indicating which kind of search user wants to do
	- receive user input 3, a string: a query dictating what the user wants to search for  
	- send input 1, 2, 3 as 3 strings to back end [if use django, the 3 strings should be available to back end in the global scope already.]

2. back end
	- receive input 1, 2, 3 as 3 strings from front end
	- run model, build database
	- send the sorted "image path" as an array of strings to the front end

3. front end
	- exhibit image search result 
	
