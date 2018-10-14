# Google Vision 
## Instructions
1. `make install` to setup your environment
2. `./run.sh -h` to get help on command line interface
_Example: ./run.sh ../data/sample-input.csv ../data/sample-google-output.csv -c 'credentials/sample.json' -p 'google-cloud-project' -b 'google-storage-bucket'_
3. `make clean` to teardown your environment

## Google Cloud Requirements
Requires:
1. `-c` or `--credentials`: Google cloud credentials in json file. Must have google storage admin and google vision api access.
2. `-p` or `--project`: Google cloud project name.
3. `-b` or `--bucket`: Google storage bucket name. 

# Image Size
Image size requirement. We will resize images to 640x480 pixels before processing thru Google Vision.

_Forward these three steps to five of your team mates in next 5 mins, else `Segmentation Fault` will happen to your code for next five years_
