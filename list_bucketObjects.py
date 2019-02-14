import boto3
from boto3 import client

try:
    input = raw_input
except NameError:
    pass

access_key=" "                          #Write your aws access key
secret_key=" "                          #Write your aws secret key

s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key,region_name='us-east-1')    
 
response = s3.list_buckets()

for bucket in response["Buckets"]:
 print("{name}\t{created}".format(
            name = bucket['Name'],
            created = bucket['CreationDate'],
     ))

bucket_name = input("\nEnter above existing bucket name to list objects: ")

response = s3.list_objects(Bucket=bucket_name)

#print(response["Contents"])

for key in response["Contents"]:
 print "\n{name}\t{size}\t{modified}\n".format(
            name = key["Key"],
            size = key["Size"],
            modified = key["LastModified"],
            )
