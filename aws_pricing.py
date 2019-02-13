import boto3
import json

access_key=" "                              #Write your aws access key
secret_key=" "                              #Write your aws secret key

# Search product filter
FLT = '[{{"Field": "tenancy", "Value": "shared", "Type": "TERM_MATCH"}},'\
      '{{"Field": "operatingSystem", "Value": "{o}", "Type": "TERM_MATCH"}},'\
      '{{"Field": "preInstalledSw", "Value": "NA", "Type": "TERM_MATCH"}},'\
      '{{"Field": "instanceType", "Value": "{t}", "Type": "TERM_MATCH"}},'\
      '{{"Field": "location", "Value": "{r}", "Type": "TERM_MATCH"}}]'


# Get current AWS price for an on-demand instance
def get_price(region, instance, os):
    f = FLT.format(r=region, t=instance, o=os)
    data = client.get_products(ServiceCode='AmazonEC2', Filters=json.loads(f))
    od = json.loads(data['PriceList'][0])['terms']['OnDemand']
    id1 = list(od)[0]
    id2 = list(od[id1]['priceDimensions'])[0]
    return od[id1]['priceDimensions'][id2]['pricePerUnit']['USD']


# Use AWS Pricing API at US-East-1
client = boto3.client('pricing', aws_access_key_id=access_key, aws_secret_access_key=secret_key,region_name='ap-south-1')

# Get current price for a given instance, region and os
# Note that the region needs to be the full name, not just the short id
price = get_price('Asia Pacific (Mumbai)', 'c5.xlarge', 'Linux')
print(price)
