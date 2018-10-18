# AWS Rekognition
## Instructions
1. `make install` to setup your environment
2. `./run.sh -h` to get help on command line interface
_Example: ./run.sh ../data/sample-input.csv ../data/sample-aws-output.csv -b 'aws-s3-bucket' -r 'us-east-1'_
3. `make clean` to teardown your environment

## First Time Use 
1. `make install` - Create a virtual environment
2. `source .venv/bin/activate` - Activate the virutal environment
3. `aws configure` - Confiugre credentials
3. Enter your AWS Key ID, Secret Access Key and if applicable a default region etc. when prompted
Read more at: https://aws.amazon.com/developers/getting-started/python/

# Image Size
Image size requirement. This code will resize images to 640x480 pixels before processing thru AWS Rekognition.

_Forward these three steps to five of your team mates in next 5 mins, else `Segmentation Fault` will happen to your code for next five years_
