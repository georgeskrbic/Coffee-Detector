import cv2
import io
import time
import requests
import numpy as np
import os
import matplotlib.pyplot as plt
import argparse
import glob
from PIL import Image
import sys
from firebase import firebase
import picamera

def store_raw_images(): #image scraper for getting set  of 3000 negative images
    j = 1429
    neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00523513'   
    neg_image_urls = requests.get(neg_images_link).content
    pic_num = 1429
    print(neg_image_urls)
    if not os.path.exists('neg'):
        os.makedirs('neg')
        
    for i in neg_image_urls.decode().split('\r\n')[:-1]:
        try:
            print(i)
            f = open('neg/%d.jpg'%pic_num, "wb")
            f.write(requests.get(i, "neg/"+str(pic_num)+".jpg").content)
            pic_num += 1
            
        except Exception as e:
            print(str(e))  

    while j <= 3141:
        print('neg'+str(j)+'.jpg')
        img = cv2.imread('neg/'+str(j)+'.jpg',cv2.IMREAD_GRAYSCALE)
        if img is not None:
            # should be larger than samples / pos pic (so we can place our image on it)
            resized_image = cv2.resize(img, (100, 100))
            cv2.imwrite("neg/"+str(j)+".jpg",resized_image)
        j+=1
def remove_bad_images(): #remove any false or corrupt images that are scraped
    match = False
    for file_type in ['neg']:
        for img in os.listdir(file_type):
            for ugly in os.listdir('uglies'):
                try:
                    current_image_path = str(file_type)+'/'+str(img)
                    ugly = cv2.imread('uglies/'+str(ugly))
                    question = cv2.imread(current_image_path)
                    if ugly.shape == question.shape and not(np.bitwise_xor(ugly,question).any()):
                        print('That is one ugly pic! Deleting!')
                        print(current_image_path)
                        os.remove(current_image_path)
                except Exception as e:
                    print(str(e))
def create_pos_n_neg(): #create text list of both positive and negative images
    for file_type in ['neg']:
        
        for img in os.listdir(file_type):

            if file_type == 'pos':
                line = file_type+'/'+img+' 1 0 0 50 50\n'
                with open('info.dat','a') as f:
                    f.write(line)
            elif file_type == 'neg':
                line = file_type+'/'+img+'\n'
                with open('bg.txt','a') as f:
                    f.write(line)
def find_pot(debug = False):
    print('First take pictures of the empty pot')
    sleep(5)
    camera = picamera.PiCamera()
    for i in range(4):
        camera.start_preview()
        camera.awb_mode = "auto"
        camera.iso = 800
        sleep(5)
        camera.stop_preview()
        camera.capture('~/Desktop/empty_pot/image%d'+'.jpg'%i)
    print('Now take pictures with coffee')
    sleep(30)
    for i in range(2):
        camera.start_preview()
        amera.awb_mode = "auto"
        camera.iso = 800
        sleep(5)
        camera.stop_preview()
        camera.capture('~/Desktop/average_pics/image%d'+'.jpg'%i)
    img = cv2.imread('~/Desktop/average_pics/image1.jpg')
    face_cascade = cv2.CascadeClassifier('cascade3.xml')
    eye_cascade = cv2.CascadeClassifier('coffee.xml')
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rgb_val = 0
    faces = face_cascade.detectMultiScale(gray, 1.2, 500, minSize=(80, 100))
    for (x,y,w,h) in faces:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        # minPotWidth = w*0.8
        # minPotHeight = minPotWidth
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.2, 10, minSize=(70, 50))
        rgb_val = 0
        numPots = 0
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            roi_liquid_color = img[ey:ey+eh, ex:ex+ew]
            mean = cv2.mean(roi_liquid_color)
            rgb_val += mean[0] +mean[1] +mean[2]
            numPots += 1
        if(numPots == 0):
            numPots += 1

        try:
            rgb_val /= numPots
        except ZeroDivisionError:
            print("Zero div")
            return 0
        print(rgb_val)
    cv2.destroyAllWindows()
    cv2.imshow("coffeePot",img)
    cv2.waitKey(2000)
    return rgb_val
def find_coffee_amount():
    min = sys.maxsize
    fb = firebase.FirebaseApplication("https://blinding-heat-3035.firebaseio.com")
    query_rgb = 0
    empty_rgb = 0
    for filename in glob.glob("empty_pot"+"/*.jpg"):
        im = Image.open(filename)
        pix = cv2.imread(filename)
        mean = cv2.mean(pix)
        empty_rgb += mean[0] + mean[1] + mean[2]
    empty_rgb /= 2 #average out the rgb values for the empty pots
    for filename in glob.glob("average_pics"+"/*.jpg"):
        im = Image.open(filename)
        pix = cv2.imread(filename)
        mean = cv2.mean(pix)
        query_rgb += mean[0] + mean[1] + mean[2]
    query_rgb /= 2 #average out the rgb values for the current pot
    query_rgb -= empty_rgb #normalize rgb values of images by subtracting the empty pot 
    print('query rgb ' + str(query_rgb))
    for filename in glob.glob("rgb_cropped"+"/*.jpg"):
        im = Image.open(filename)
        pix = cv2.imread(filename)
        mean = cv2.mean(pix)
        rgb_val = mean[0] + mean[1] + mean[2]
        rgb_val -= empty_rgb
        print(str(rgb_val) + ' ' + filename)
        if(abs(query_rgb - rgb_val) <= min): # compare rgb values of reference images with the current pot to check for similarity in amount of coffee in pot
            min = abs(query_rgb - rgb_val)
            min_file = filename
            most_sim = cv2.imread(filename)
    print(min_file)#files are labeled based of percentage coffee within each pot
    min_file = os.path.splitext(min_file)[0]
    min_file = min_file.split('_',2)
    print(min_file)
    result = fb.put('/user','one', min_file[2]) #update server with current percentage of coffee in the pot
    # cv2.imshow('most similar',most_sim)
    # cv2.waitKey(1000)

find_pot()    
find_coffee_amount()


