import requests

## Google Imports
from google.cloud import storage
from google.cloud import vision
from google.cloud.vision import types
import os
import urllib.request
from PIL import Image
from fuzzywuzzy import fuzz

def resize(credentials, project, bucket, id, url):
    #create images directory if not there
    os.makedirs("images", exist_ok=True)
    #set image name and location
    process_name = 'google_vision_api'
    food_image_name = "{}_image_food_{}.jpg".format(process_name, id) 
    food_image_location = "images/{}".format(food_image_name)
    #download image locally
    print("Downloading image from: {}".format(url))
    urllib.request.urlretrieve(url, food_image_location)
    img = Image.open(food_image_location)
    #resizing image to 640*480
    new_img = img.resize((640,480))
    new_img.save(food_image_location, "JPEG", optimize=True)
    ## Instantiate a client for project 'glucotune-dev'
    ## set the service account key file generated from google cloud to environment variable
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']=credentials
    bucket = storage.Client(project).get_bucket(bucket)

    blob = bucket.blob(food_image_location)
    blob.upload_from_filename(food_image_location)
    blob.make_public()

    print("Uploaded resized image to: {}".format(blob.public_url))

    return blob.public_url

def workflow(credentials, project, bucket, id, url):
    image_uri = resize(credentials, project, bucket, id, url)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']=credentials
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = image_uri
    label_annotations = client.label_detection(
        image=image,max_results=25
    ).label_annotations
    web_detections = client.web_detection(
        image = image,max_results=25
    ).web_detection
    best_guess = web_detections.best_guess_labels[0].label.lower()
    labels_result = [
        {
            "resize_url": image_uri,
            "name": label_annotation.description.lower(),
            "value": label_annotation.score,
            "label_topicality": label_annotation.topicality,
            "best_guess_label_score": fuzz.ratio(best_guess, label_annotation.description.lower())/100.0,
        } for label_annotation in label_annotations
    ]
    web_result = [
        {
            "resize_url": image_uri,
            "name": web_entity.description.lower(),
            "value": web_entity.score,
            "label_topicality": "N/A",
            "best_guess_label_score": fuzz.ratio(best_guess, web_entity.description.lower())/100.0,
        } for web_entity in web_detections.web_entities
    ]
    for w in web_result:
        found = False
        for l in labels_result:
            found = w["name"].lower() == l["name"].lower()
            if found:
                update = w["value"] > l["value"]
                if update:
                    l["value"] = w["value"]
                break
        if not found:
            labels_result.append(w)
    
    return labels_result
            

