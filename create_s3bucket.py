import boto3
import json 
import re
from boto3 import client

access_key=" "                          #Write your aws access key
secret_key=" "                          #Write your aws secret key

try:
    input = raw_input
except NameError:
    pass


bucket_name = input("Enter S3 bucket name: ")


s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key,region_name='us-east-1')    
    
bucket = s3.create_bucket(Bucket=bucket_name)

#print(bucket)

response = s3.list_buckets()
    
for bucket in response["Buckets"]:
 print "{name}\t{created}".format(
            name = bucket['Name'],
            created = bucket['CreationDate'],
            )
