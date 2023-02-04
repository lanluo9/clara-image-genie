we will test our app on this `test_images` folder

---

what happens in the front end:  

- receive user input 1: let user select a folder of images that they want to search in  
	- when testing our app, this folder is always the `test_images` folder 
	- pass user input 1 as a string of folder directory to back end
	
- receive user input 2: a query dictating what the user wants to search for  
	- pass user input 2 as a string to back end
	
- wait for back end to return output
	- output will be 3 arrays of strings
	- each string in the arrays is the absolute path of an image relevant to the search query from user
	- each array of string has been sorted by relevance based on:
		- image content 1: alt text / image description for blind users / screen readers
		- image content 2: object detected
		- image content 3: OCR generated text
		
- receive user input 3: click on one of the tabs
	- see https://github.com/lanluo9/clara-image-genie/blob/main/front-end/UI-concept-draft.png
- make UI exhibit the images corresponding to the absolute paths in the output
	- UI contains 3 tabs
	- each tab correspond to an output column, sorted by relevance based on "image content" 1-3

---

what happens in the back end: 

- receive front end user input 1: folder directory as a string
	- when testing our app, this folder is always the `test_images` folder  
	
- index all images in this folder. for each image
	- run object recognition model
	- run OCR model
	- run alt text / image description generation model
	
- build database / dataframe, containing columns of
	- image path: absolute path of each image in this folder
	- image content 1: alt text / image description for blind users / screen readers
	- image content 2: object detected
	- image content 3: OCR generated text
	- (all columns only contain strings)
	
- receive front end user input 2: keyword query as a string
- calculate relevance between the "image content" columns versus the keyword query
	- sort "image path" by relevance based on 3 "image content" columns, respectively
	- only keep the top n images (let's start with n=10)
	- return the sorted "image path" column as 3 array of strings to the front end
		- each array of string has been sorted by relevance based on "image content" 1-3
	
---

what happens when front end and back end talk to each other

1. front end 
	- receive user input 1, a string: let user select a folder of images that they want to search in  
	- receive user input 2, a string: a query dictating what the user wants to search for  
	- send input 1 & 2 to back end

2. back end
	- receive input 1 & 2 from front end
	- run model, build database
	- send the sorted "image path" as 3 array of strings to the front end

3. front end
	- receive user input 1, a mouse click to select tab that decides what kind of image content (blind, obj, OCR) to search
	- exhibit image search result 
	