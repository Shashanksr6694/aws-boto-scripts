import boto3
import csv
from aws_pricing import get_price

access_key=" "                          #Write your aws access key
secret_key=" "                          #Write your aws secret key

untagged_ec2=0

client = boto3.client('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key,region_name='us-east-1')

def getUntaggedInstances():
    #try:       
                filename="untagged_instances.csv"
                fields=['InstanceId','InstanceType','Region']
                data=[]
                ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
            
                for region in ec2_regions:
                        if region=='us-east-1':
                                Region='US East (N. Virginia)'                     
                        elif region=='ap-south-1':
                                Region='Asia Pacific (Mumbai)'
                        elif region=='ap-southeast-1':
                                Region='Asia Pacific (Singapore)'

                        conn = boto3.resource('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key,region_name=region)

                        running_instances = conn.instances.filter(Filters=[{'Name': 'instance-state-name','Values': ['running']}])

                        for instance in running_instances:
                            if instance.tags is None:
                                global untagged_ec2
                                untagged_ec2=untagged_ec2+1
                                data.append({"InstanceId":instance.id,"InstanceType": instance.instance_type,"Region": region})
                            
                            else:
                                for tag in instance.tags:
                                    if tag['Key'] == 'Jira_ticket':
                                        instanceName = tag['Value']
                                        print(instanceName)


                with open(filename,'w') as csvfile:
                        writer=csv.DictWriter(csvfile,fieldnames=fields)
                        writer.writeheader()
                        writer.writerows(data)

    #except:
    #    print "got an exception"




getUntaggedInstances()

