==> Project Built using Python 3.5



############################
#
###INSTRUCTIONS FOR ENCODING

############################


1) Run MyServer.py

2) Go to localhost:55555 and you'll get a 400 Bad Request response since this request is not programmed to do anything as per the API
3) Go to localhost:55555/file1.txt to recieve the contents of file1 encoded into a random image from the 5 present in the project directory
4) Save the encoded image file. Make sure to select right file type (i.e. png) while saving
5) You can fetch any of the ten files (from file1.txt to file10.txt). But fetching a file that is not present in the directory (i.e. file50 for example) will result in a 404 Not Found response



############################

###INSTRUCTIONS FOR DECODING

############################



1) Copy the encoded image to the project root

2) Open Decoder.py and set the variable imageName to the name of the encoded image file.

3) Run the script and you'll see the decoded text
