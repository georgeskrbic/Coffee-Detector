# Coffee Detector

Detect the amount of coffee currently in a pot. This was made in python using OpenCV while utilizing a Raspberry Pi configured with a camera module to take still images of a coffee pot and detect the amount in it. This information is subsequently made available through a web interface. The overall purpose is to provide an easy method for knowing if coffee is available in a shared setting such as an office.  


## Training the classifier

The detection of the coffee pot was done using a trained classifier using OpenCV.  There is a clear and simple tutorial for first time users provided by [Coding Robin](http://coding-robin.de/2013/07/22/train-your-own-opencv-haar-classifier.html) that helps greatly in creating your first cascade classifier.

## Detecting amount of coffee

Once the pot is detected using the classifier, an algorithm was developed for comparing the rgb scalars of the current picture of a pot to reference images. These reference images contain a varying amount of coffee, specifically differing in amount by 25 percent. Based on which image the current picture was most similar to, we parsed the image name, which included the percentage, and updated the website accordingly. The website updating was handled in realtime using [Firebase](https://www.firebase.com/) and a sample can be found [here](tylorsarrafzadeh.com/dashboard.html) 