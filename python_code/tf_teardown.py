## automated teardown process of resources provisioned ion boot strap for the terraform services

import boto3
from botocore.exceptions import ClientError
import os


# Delete Bucket
def delete_bucket(bucket_name):
    s3_client = boto3.client('s3', region_name='us-east-1')

    try:
        buckets = s3_client.list_buckets()
        bucket_string = bucket_name
        print(f"Found bucket name as {bucket_string}")
        
        #Delete the versions
        object_versions = s3_client.list_object_versions(Bucket=bucket_string)
        versions = object_versions.get('Versions', []) + object_versions.get('DeleteMarkers', [])
        for version in versions:
            s3_client.delete_object(
                Bucket = bucket_string,
                Key=version['Key'],
                VersionId=version['VersionId']
            )

        print (f"All Objects and versions in {bucket_string} were deleted successfully")
        
        #actually delete teh bucket
        s3_client.delete_bucket(Bucket=bucket_string)

        print(f'{bucket_string} was removed')
    
    except ClientError as e:
        print(f"Error deleting bucket: {e}")


# Delete Dynamo DB Table
def delete_db_table():
    dynamo_client = boto3.client('dynamodb')
    try:
        dynamo_client.delete_table(
            TableName = 'terraform-state-locking'
        )

        print(f"deleted the DynamoDB table for state locking")

    except ClientError as e:
        print(f"Error deleting DynamoDB table: {e}")



# Delete IAM user
def delete_iam_user():
    iam_client = boto3.client('iam')

    try:
        #get the access Key id and delete it
        key_data = iam_client.list_access_keys(UserName='tf-user')
        access_key = key_data['AccessKeyMetadata'][0]['AccessKeyId']

        iam_client.delete_access_key(
            UserName='tf-user',
            AccessKeyId=access_key)
        
        print(f'deleted tf-user Access Key:{access_key}')

        #Detach Permissions
        iam_client.detach_user_policy(
            UserName = 'tf-user',
            PolicyArn = 'arn:aws:iam::aws:policy/AdministratorAccess'
        )

        print(f'detached tf-user Admin Policy')

        # Delete teh user itself
        iam_client.delete_user(UserName = 'tf-user')

        print(f'Deleted tf-user')

    except ClientError as e:
        print(f"Error deleting tf-user: {e}")


def main():
    with open("s3_bucket.txt", mode="r") as file:
        bucket_name = file.read().strip()  # Use strip to remove any trailing newlines or spaces
    
    # Call the delete_bucket function with the bucket name from the file
    delete_bucket(bucket_name)
    delete_db_table()
    delete_iam_user()


if __name__ == "__main__":
    main()

