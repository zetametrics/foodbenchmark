import requests

import pandas as pd
import os
import urllib.request
from PIL import Image
import urllib.request
from fuzzywuzzy import fuzz
## AWS Imports
import boto3

def resize(region, bucket, id, url):
    #create images directory if not there
    os.makedirs("images", exist_ok=True)
    #set image name and location
    process_name = 'aws_rekognition'
    food_image_name = "{}_image_food_{}.jpg".format(process_name, id) 
    food_image_location = "images/{}".format(food_image_name)
    #download image locally
    print("Downloading image from: {}".format(url))
    urllib.request.urlretrieve(url, food_image_location)
    img = Image.open(food_image_location)
    #resizing image to 640*480
    new_img = img.resize((640,480))
    new_img.save(food_image_location, "JPEG", optimize=True)

    #AWS
    s3 = boto3.resource('s3')
    s3_bucket = s3.Bucket(bucket)
    data = open(food_image_location, 'rb')
    s3_bucket.put_object(Key=food_image_name, Body=data)
    
    object_acl = s3.ObjectAcl(bucket,food_image_name)
    object_acl.put(ACL='public-read')
    
    data.close()
    
     ##remove local file - to reduce clutter
    os.remove(food_image_location)
    image_url = '{}/{}/{}'.format("https://s3.amazonaws.com", bucket, food_image_name)

    print(str.format("Uploaded image to s3 bucket: {}", image_url))
    region=region

    return (food_image_name, image_url)

def workflow(region, bucket, id, url):
    food_image_name, image_url = resize(region, bucket, id, url)
    rekognition = boto3.client("rekognition", region)    
    max_labels=25
    min_confidence=50
    response = rekognition.detect_labels(
		Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": food_image_name,
			}
		},
		MaxLabels=max_labels,
		MinConfidence=min_confidence,
	)    

    label_result = [
        {
            "resize_url": image_url,
            "name": entity['Name'].lower(),
            "value": entity['Confidence'],
        } for entity in response['Labels']
    ]
    return label_result
            

