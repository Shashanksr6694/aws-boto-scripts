import boto3
import csv
from aws_pricing import get_price
available_volumes=[]

access_key=" "                               #Write your aws access key
secret_key=" "                               #Write your aws secret key

unattached_ebs=0
stopped_ec2=0
total_cost=0
staging_ec2=0
production_ec2=0


client = boto3.client('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key,region_name='ap-south-1')

def getUnattachedVolumes():
	try:
		filename="UnattachedEBS.csv"
		fields=['EBS_Id','EBS_Type','EBS_Size','Cost($)']
		ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
		available_volumes=[]
		for region in ec2_regions:
			if region=='ap-southeast-1':
				factor=0.12
			elif region=='ap-south-1':
				factor=0.114
			ec2=boto3.resource('ec2',aws_access_key_id=access_key, aws_secret_access_key=secret_key,region_name=region)        
			volumes=ec2.volumes.filter(Filters=[{'Name':'status','Values':['available']}])
	
			for vol in volumes:
				iv=ec2.Volume(str(vol.id))
				global unattached_ebs
				global total_cost
				unattached_ebs=unattached_ebs+1
				total_cost+=iv.size*factor
				available_volumes.append({'EBS_Id': str(iv.volume_id),'EBS_Type':iv.volume_type,'EBS_Size':iv.size,'Cost($)':iv.size*factor})
		with open(filename,'w') as csvfile:
			writer=csv.DictWriter(csvfile,fieldnames=fields)
			writer.writeheader()
			writer.writerows(available_volumes)
		
	except:
		print "got an exception"



def getStoppedInstances():
	try:     
		filename="stopped_instances.csv"
		fields=['InstanceId','InstanceType','Region','EBS_Id','EBS_Type','EBS_Size','Cost($)']
		data=[]
		ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
		for region in ec2_regions:
			if region=='ap-southeast-1':
				factor=0.12
			elif region=='ap-south-1':
				factor=0.114

			conn = boto3.resource('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key,region_name=region)
		        instances = conn.instances.filter()
 			for instance in instances:
			        if instance.state["Name"] == "stopped":
					global stopped_ec2
					stopped_ec2=stopped_ec2+1
					volumes=instance.volumes.all()
					volume_data=[]
					ids=[]
					types=[]
					size=[]
					cost=0
					for v in volumes:
						volume_data.append({'volume_id':v.id,'volume_type':v.volume_type,'volume_size':v.size})
						ids.append(v.id)
						types.append(v.volume_type)
						size.append(v.size)
						cost+=v.size*factor
						global total_cost
						total_cost+=cost
			        	data.append({"InstanceId":instance.id,"InstanceType": instance.instance_type,"Region": region,'EBS_Id':ids,'EBS_Type':types,'EBS_Size':size,'Cost($)':cost})

		with open(filename,'w') as csvfile:
			writer=csv.DictWriter(csvfile,fieldnames=fields)
			writer.writeheader()
			writer.writerows(data)
	except:
		print "got an exception"



def getSummary():
	return {'stopped_ec2':stopped_ec2,'unattached_ebs':unattached_ebs,'total_cost':total_cost}


def getStagingInstances():
        try:     
		filename="staging.csv"
		fields=['InstanceId','InstanceType','Region','Cost($)(Hourly)']
		data=[]
		ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
		for region in ec2_regions:
			if region=='ap-southeast-1':
				Region='Asia Pacific (Singapore)'
			elif region=='ap-south-1':
				Region='Asia Pacific (Mumbai)'

			conn = boto3.resource('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key,region_name=region)
		        instances = conn.instances.filter(Filters=[{
   					 'Name': 'tag:Stack',
   					 'Values': ['Staging']}])
 			for instance in instances:
			        if instance.state["Name"] == "running":
					global staging_ec2
					staging_ec2=staging_ec2+1
					cost=get_price(Region,instance.instance_type,'Linux')
			        	data.append({"InstanceId":instance.id,"InstanceType": instance.instance_type,"Region": region,'Cost($)(Hourly)':cost})

		with open(filename,'w') as csvfile:
			writer=csv.DictWriter(csvfile,fieldnames=fields)
			writer.writeheader()
			writer.writerows(data)
	except:
		print "got an exception"

def getProductionInstances():
	try:     
		filename="production.csv"
		fields=['InstanceId','InstanceType','Region','Cost($)(Hourly)']
		data=[]
		ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
		for region in ec2_regions:
			if region=='ap-southeast-1':
				Region='Asia Pacific (Singapore)'
			elif region=='ap-south-1':
				Region='Asia Pacific (Mumbai)'

			conn = boto3.resource('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key,region_name=region)
		        instances = conn.instances.filter(Filters=[{
   					 'Name': 'tag:Stack',
   					 'Values': ['Production']}])
 			for instance in instances:
			        if instance.state["Name"] == "running":
					global production_ec2
					production_ec2=production_ec2+1
					cost=get_price(Region,instance.instance_type,'Linux')
			        	data.append({"InstanceId":instance.id,"InstanceType": instance.instance_type,"Region": region,'Cost($)(Hourly)':cost})

		with open(filename,'w') as csvfile:
			writer=csv.DictWriter(csvfile,fieldnames=fields)
			writer.writeheader()
			writer.writerows(data)
	except:
		print "got an exception"







getStoppedInstances()

getUnattachedVolumes()

getStagingInstances()

getProductionInstances()
