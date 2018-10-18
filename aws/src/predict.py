import argparse
import csv

import api

parser = argparse.ArgumentParser(
    prog='run.sh',
    description='Process images via AWS Rekognition'
)

parser.add_argument(
    'input',
    metavar = 'ipfile',
    help = 'input csv file containing image_url and correct_label',
)

parser.add_argument(
    'output',
    metavar = 'opfile',
    help = 'output csv file',
)

parser.add_argument(
    '-b', '--bucket',
    metavar = '',
    help = 'AWS S3 Bucket.',
)

parser.add_argument(
    '-r', '--region',
    metavar = '',
    help = 'AWS S3 Region.',
)

args = parser.parse_args()

input_file = args.input
output_file = args.output
bucket = args.bucket
region = args.region

with open(input_file, newline='') as csv_ip_file:
    with open(output_file, 'w', newline='') as csv_op_file:
        reader = csv.DictReader(csv_ip_file)
        fieldnames = [
            "id",
            "image",
            "resize_url",
            "label",
            "score",
            "correct_label",
        ]
        writer = csv.DictWriter(
            csv_op_file,
            fieldnames=fieldnames,
            quoting=csv.QUOTE_ALL,
        )
        writer.writeheader()
        for row in reader:
            url = row["image_url"]
            print("Processing image at {}".format(url))
            resp = api.workflow(region, bucket, row["id"], url)
            print("Storing rekognition api results for image {}".format(url))
            for data in resp:
                output = {
                    "id": row["id"],
                    "resize_url": data["resize_url"],
                    "image": url,
                    "label": data["name"],
                    "score": data["value"],
                    "correct_label": row["correct_label"],
                }
                writer.writerow(output)
