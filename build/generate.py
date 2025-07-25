import os
from jinja2 import Environment, FileSystemLoader
import random
import string
import boto3
from InquirerPy import inquirer


# Global Variable grab

regions = [
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2"
]

region = inquirer.select(
    message="Which Region do you want to Build In?",
    choices=regions
).execute()


# Make S3 Bucket for state
def create_bucket(region):

    # Generate a random string of 4
    characters = string.ascii_lowercase + string.digits  # Include both letters and digits
    random_string = ''.join(random.choice(characters) for _ in range(4))
    bucket_name = "wordpress-tf-" + random_string

    print(bucket_name)

    s3_client = boto3.client('s3', region_name=region)

    if region == "us-east-1":
        s3_client.create_bucket(Bucket=bucket_name)
    else:
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )

    # Enable Versioning
    s3_client.put_bucket_versioning(
        Bucket=bucket_name,
        VersioningConfiguration={
        'Status': 'Enabled'
        }
    )

    ## Adding enforced SSE
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
    print(f"Bucket {bucket_name} Created")
    return bucket_name

## Make teh DynamoDB Table #####

def create_dynamodb_table(region):

    print("Working on DynamoDB for State Locking")

    table_name = "terraform-state-locking"
    dynamo_client = boto3.client('dynamodb', region_name=region)
    dynamo_client.create_table(
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

    print(f"""
#######  Dynamo DB ##############
\n✅ Dynamo Table: {table_name} created successfully
-------------------------------------------""")


bucket_name = create_bucket(region)
create_dynamodb_table(region)




########################  JINJA2 Section #############################


# Establish Jinja Tempalt Directory and templates
template_dir = "templates"
env = Environment(loader=FileSystemLoader(template_dir))

# === Step 3: Template context ===
context = {
    "bucket": bucket_name,
    "region": region
}

# === Step 4: List of template files to process ===
template_files = [
    "providers.tf.j2"
]

# === Step 5: Render each file ===
for template_file in template_files:
    template = env.get_template(template_file)
    rendered = template.render(context)

    # Output filename (strip .j2 extension)vv 
    output_filename = template_file.replace(".j2", "")
    output_path = os.path.join("..", "wordpress", output_filename)

    with open(output_path, "w") as f:
        f.write(rendered)

print(f"\n✅ Terraform Provider File generated for Wordpress\n")





