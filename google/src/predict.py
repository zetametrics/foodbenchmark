import argparse
import csv

import api

parser = argparse.ArgumentParser(
    prog='run.sh',
    description='Process images via Google Vision API'
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
    '-c', '--credentials',
    metavar = '',
    help = 'Google Credentials (JSON file). Requires permission to access your google storage and cloud vision api.',
)

parser.add_argument(
    '-b', '--bucket',
    metavar = '',
    help = 'Google Storage Bucket.',
)

parser.add_argument(
    '-p', '--project',
    metavar = '',
    help = 'Google Cloud Project.',
)

args = parser.parse_args()

input_file = args.input
output_file = args.output
credentials = args.credentials
bucket = args.bucket
project = args.project

if (credentials is None):
    print("Requires google cloud credentials. Please run -h to see required parameters.")
    exit(1)
else:
    print("Using google credetials from {} to access project {}".format(credentials,project))

with open(input_file, newline='') as csv_ip_file:
    with open(output_file, 'w', newline='') as csv_op_file:
        reader = csv.DictReader(csv_ip_file)
        fieldnames = [
            "id",
            "image",
            "resize_url",
            "label",
            "score",
            "label_topicality",
            "best_guess_label_score",
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
            resp = api.workflow(credentials, project, bucket, row["id"], url)
            print("Storing vision api results for image {}".format(url))
            for data in resp:
                output = {
                    "id": row["id"],
                    "resize_url": data["resize_url"],
                    "image": url,
                    "label": data["name"],
                    "score": data["value"],
                    "label_topicality": data["label_topicality"],
                    "best_guess_label_score": data["best_guess_label_score"],
                    "correct_label": row["correct_label"],
                }
                writer.writerow(output)
