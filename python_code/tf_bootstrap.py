import boto3
from botocore.exceptions import ClientError
import random
import string

def generate_random_string(length):
    """Generate a random string of specified length."""
    characters = string.ascii_lowercase + string.digits  # Include both letters and digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    
    with open("s3_bucket.txt", mode="w") as file:
        file.write(random_string)
    
    return random_string


def create_s3_bucket(bucket_name, region=None):
    #establish Client Sessions for Service
    s3_client = boto3.client('s3', region_name=region)

    try:
        # Create the bucket with or without a location constraint
        if region == 'us-east-1':
            # No location constraint needed for 'us-east-1'
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            # Set location for other regions
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)


        #Enable Versioning, then test it out. do the initial, make  achange re apply, check the versiojing, thats kind of dope actually. 
        s3_client.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={
            'Status': 'Enabled'
            }
        )

        ## Addign enforced Server side encryption
        s3_client.put_bucket_encryption(
            Bucket=bucket_name,
            ServerSideEncryptionConfiguration={
                'Rules': [
                    {
                        'ApplyServerSideEncryptionByDefault': {
                            'SSEAlgorithm': 'AES256'
                        }
                    },
                ]
            }
        )

        #Final Output
        print(f'''
#######  S3 Bucket Info ##############
              
Bucket Name: {bucket_name} created successfully

Replace the backend resource block in the provider tab with: 

  backend "s3" {{
    bucket         = "{bucket_name}"
    key            = "tf-dev/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-locking"
    encrypt        = true
  }}

-------------------------------------------''')

    except ClientError as e:
        print(f"Error creating bucket: {e}")



###############################################################################

import boto3
from botocore.exceptions import ClientError

def create_dynamodb_table(table_name, region):
    dynamo_client = boto3.client('dynamodb', region_name=region)
    
    try:
        print(f"Creating DynamoDB table: {table_name}...")

        # Try to create the table
        response = dynamo_client.create_table(
            TableName=table_name,
            BillingMode='PAY_PER_REQUEST',
            KeySchema=[{
                'AttributeName': 'LockID',
                'KeyType': 'HASH'
            }],
            AttributeDefinitions=[{
                'AttributeName': 'LockID',
                'AttributeType': 'S'
            }]
        )
        
        # Wait for table to be created (optional, for confirmation)
        waiter = dynamo_client.get_waiter('table_exists')
        waiter.wait(TableName=table_name)

        # Log response from AWS, use this for debugging, turn it on
        # print(f"Table creation response: {response}")

        print(f"""
#######  Dynamo DB ##############
Dynamo Table: {table_name} created successfully
-------------------------------------------""")

    except ClientError as e:
        print(f"Error creating DynamoDB Table: {e.response['Error']['Message']}")
        print(f"Full error: {e}")

###############################################################################

def create_tf_iam_user(user_name):
    #establish Client Sessions for Service
    iam_client = boto3.client('iam')

    try:
        # Create a new IAM user
        iam_user_response = iam_client.create_user(UserName=user_name)
        print(f"""
#######  IAM TF-User information ##############
""")

#         #Codified record of when user was created for reference later
#         creation_date = iam_user_response['User']
#         print(f"""
# {user_name} was created on: {creation_date['CreateDate']}
# -------------------------------------------""")

        # Attach a policy to the user
        policy_arn = 'arn:aws:iam::aws:policy/AdministratorAccess'
        iam_client.attach_user_policy(UserName=user_name, PolicyArn=policy_arn)

        # Create access key for the user
        access_key_response = iam_client.create_access_key(UserName=user_name)
        access_key = access_key_response['AccessKey']
        
        # Print All the Outputs
        print(f"""           
Copy this into the ~/user/.aws/credentials file
              
[{user_name}] 
aws_access_key_id = {access_key['AccessKeyId']}
aws_secret_access_key = {access_key['SecretAccessKey']}

Copy this under the ~/user/.aws/config file

[{user_name}]
region = us-east-1
output = json
""")
        
    except ClientError as e:
        print(f"Error creating IAM user: {e}")

def main():
    #Assign Variables
    bucket_name = generate_random_string(25)
    region = 'us-east-1'
    user_name = "tf-user"
    table_name = 'terraform-state-locking'

    # Selecting the functions to be run
    create_tf_iam_user(user_name)
    create_s3_bucket(bucket_name, region)
    create_dynamodb_table(table_name, region)


#One final print instead of each area, so the function returns the vaule?? since its ran here in main
#     print(f"""
          
#  {user_name}                  
        
# """)
if __name__ == "__main__":
    main()



