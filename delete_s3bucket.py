import boto3
import json 
import re
from boto3 import client

access_key="AKIAIXF2AZZVCUYPJUTA"
secret_key="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"

try:
    input = raw_input
except NameError:
    pass


s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key,region_name='us-east-1')    
response = s3.list_buckets()


#list buckets

for bucket in response["Buckets"]:
    print "{name}\t{created}".format(
                name = bucket['Name'],
                created = bucket['CreationDate'],
            )



#list objects before deleting bucket

bucket_name = input("\nEnter above existing bucket name to list objects before deleting bucket: ")
response = s3.list_objects(Bucket=bucket_name)


for key in response["Contents"]:
    print "{name}\t{size}\t{modified}".format(
                name = key["Key"],
                size = key["Size"],
                modified = key["LastModified"],
            )



#Deleting bucket

del_bucket = input("\nEnter above existing bucket name to delete: ")
bucket = s3.delete_bucket(Bucket=del_bucket)



#now list the bucket to check available buckets

response = s3.list_buckets()
    
for bucket in response["Buckets"]:
 print "{name}\t{created}".format(
            name = bucket['Name'],
            created = bucket['CreationDate'],
            )
