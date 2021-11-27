The Folder "Before Images" contains all the initial photos before transformation that are used and mentioned in the report

Requirments.txt contains all the versions mentioned of each library

Interface.py is for GUI Interface
transform.py contains all the image processing transformations
In Interface.py, we import transform.py
So, to start the application run Interface.py in python

Buttons on the Interface and thier functions:
Open:
	when clicked the button, we can access any image on the disk to display on the interface
Undo:
	Goes back to the prev image, that was before applying any transform
Original:
	Undoes all the transforms and goes back to the original image
Histogram Equalization: 
	Applies Histogram equalisation of intensities on the current displaying image
Logarithm:
	Applies Logarithmic Transformation on the current displaying image
Negative:
	Applies the Negative color transform of the current displaying button
Gamma Transform:
	Enter the value of gamma in the entry box above this button and press the button, this applies the gamma power transform on the current displaying image
Blur Image: 
	Set the slider aboove this button to control the amount of blurness and click the button to blur the current displaying image
Sharpen Image: 
	Set the slider aboove this button to control the amount of sharpness and click the button to sharpen the current displaying image
Save:
	enter the desired name, u wish to save the current displaying image in the entry box above this button and click the button, this saves the current displaying image in jpeg format in the current file location(where the code is running)
	Eg: U wanna save the image as Edited,jpeg, then enter "Edited" into the entry box and click save
Quit:
	Click this button to close and quit the whole interface