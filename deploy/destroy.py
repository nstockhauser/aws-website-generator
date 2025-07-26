import boto3
import os
from InquirerPy import inquirer
import shutil
import glob




##Core or Website?

destroy_options = [
    "core",
    "website"
]

destroy = inquirer.select(
    message="Which do you want to destroy",
    choices=destroy_options
).execute()

#Core portion

# Delete Bucket
def delete_bucket():

    s3_client = boto3.client('s3')

    # get bucket_name
    bucket_list = s3_client.list_buckets()

    bucket_name = None

    for bucket in bucket_list['Buckets']:
        if bucket ['Name'].startswith('websites-tf-'):
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




## Website portion
def delete_website_folder():
    base_dir = "sites/"

    dir_choices = [
        name for name in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, name))
    ]

    dir_to_delete = inquirer.select(
        message="Which website do you want to remove?",
        choices = dir_choices
    ).execute()

    target_path = os.path.join(base_dir,dir_to_delete)
    shutil.rmtree(target_path)
    print(f"✅ Deleted directory: {target_path}")

# def delete_website_state():




# Basic decision logic

if destroy == "core":
    delete_bucket()
    delete_db_table("us-east-1")
else:
    delete_website_folder()
    # delete_website_state()



