import boto3
import os
import pathlib
from pprint import pprint


AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_ENDPOINT_URL = os.getenv('AWS_ENDPOINT_URL')

print("AWS_ACCESS_KEY_ID:", AWS_ACCESS_KEY_ID)
print("AWS_SECRET_ACCESS_KEY:", AWS_SECRET_ACCESS_KEY)
print("AWS_ENDPOINT_URL:", AWS_ENDPOINT_URL)

s3 = boto3.client(
    "s3",
    endpoint_url=AWS_ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
bucket_name = "fluigi"
object_name = "sample1.txt"
file_name = os.path.join(pathlib.Path(__file__).parent.resolve(), "sample_file.txt")

response = s3.upload_file(file_name, bucket_name, object_name)
pprint(response)  # prints None
