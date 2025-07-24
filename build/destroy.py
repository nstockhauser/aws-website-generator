import boto3
import os
from InquirerPy import inquirer


regions = [
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2"
]

region = inquirer.select(
    message="Which Region do you want to Tear Down?",
    choices=regions
).execute()

# Delete Bucket
def delete_bucket(region):

    s3_client = boto3.client('s3', region_name=region)

    # get bucket_name
    bucket_list = s3_client.list_buckets()

    bucket_name = None

    for bucket in bucket_list['Buckets']:
        if bucket ['Name'].startswith('wordpress-tf-'):
            bucket_name = bucket['Name']
            break


    print(f"Found bucket name as {bucket_name}")
    
    #Delete the versions
    object_versions = s3_client.list_object_versions(Bucket=bucket_name)
    versions = object_versions.get('Versions', []) + object_versions.get('DeleteMarkers', [])
    for version in versions:
        s3_client.delete_object(
            Bucket = bucket_name,
            Key=version['Key'],
            VersionId=version['VersionId']
        )

    print (f"All Objects and versions in {bucket_name} were deleted successfully")
    
    #actually delete teh bucket
    s3_client.delete_bucket(Bucket=bucket_name)

    print(f'{bucket_name} was removed')






# Delete Dynamo DB Table
def delete_db_table(region):
    dynamo_client = boto3.client('dynamodb', region_name=region)
    dynamo_client.delete_table(TableName = 'terraform-state-locking')
    print(f"deleted the DynamoDB table for state locking")




delete_bucket(region)
delete_db_table(region)

provider_file = "../wordpress/providers.tf"

if os.path.exists(provider_file):
    os.remove(provider_file)
    print(f"✅ Deleted {provider_file}")
else:
    print(f"⚠️ File not found: {provider_file}")