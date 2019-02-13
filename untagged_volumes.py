import boto3
import csv
from aws_pricing import get_price


access_key=" "                       #Write your aws access key
secret_key=" "                       #Write your aws secret key

untagged_ebs=0

client = boto3.client('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key,region_name='us-east-1')

def getUntaggedVolumes():
    #try:       
                filename="untagged_volumes.csv"
                fields=['EBS_Id','EBS_Type','EBS_Size','Region','Status']
                volume=[]
                ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
            
                for region in ec2_regions:
                        if region=='us-east-1':
                                Region='US East (N. Virginia)'
                        elif region=='ap-south-1':
                                Region='Asia Pacific (Mumbai)'
                        elif region=='ap-southeast-1':
                                Region='Asia Pacific (Singapore)' 

                        conn = boto3.resource('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key,region_name=region)
                        volumes = conn.volumes.filter(Filters=[{'Name':'status','Values':['available','in-use']}])

                        for vol in volumes:
                            if vol.tags is None:
                                iv=conn.Volume(str(vol.id))
                                global untagged_ebs
                                untagged_ebs=untagged_ebs+1
                                volume.append({'EBS_Id': str(iv.volume_id),'EBS_Type':iv.volume_type,'EBS_Size':iv.size,"Region": region,"Status":iv.state})
                            
                            else:
                                for tag in vol.tags:
                                    if tag['Key'] == 'Jira_ticket':
                                        volumeName = tag['Value']
                                        print(volumeName)


                with open(filename,'w') as csvfile:
                        writer=csv.DictWriter(csvfile,fieldnames=fields)
                        writer.writeheader()
                        writer.writerows(volume)

    #except:
    #    print "got an exception"




getUntaggedVolumes()
