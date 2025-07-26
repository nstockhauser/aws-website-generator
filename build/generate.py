import os
from jinja2 import Environment, FileSystemLoader
import random
import string
import boto3
from InquirerPy import inquirer



websites = [
    "apache",
    "wordpress" ## Add more options here if you want a custom userdata.sh
]

regions = [
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2"  # Add another region not included that you want to use
]


def get_unique_dir_name():
    website_name = input("What's the name of your website?\n> ")
    website_type = inquirer.select(
        message="Which kind of website do you want to build?",
        choices=websites
    ).execute()

    dir_name = website_name + website_type
    if os.path.exists(dir_name):
        print(f"⚠️ Directory '{dir_name}' already exists. Try again.")
        return get_unique_dir_name()  # recursion
    return website_name, website_type, dir_name


website_namqe, website_type, dir_name = get_unique_dir_name()




##### AWS Build Time ####

region = inquirer.select(
    message="Which Region do you want to Build In?",
    choices=regions
).execute()


def create_bucket(region):


    # Check if S3 bucket already exists:
    s3_client = boto3.client('s3', region_name=region)

    # get bucket_name
    bucket_list = s3_client.list_buckets()

    bucket_name = None

    for bucket in bucket_list['Buckets']:
        if bucket ['Name'].startswith('websites-tf-'):
            bucket_name = bucket['Name']
            print (f"Found existing bucket: {bucket_name}")
            return bucket_name
    


    # Generate a random string of 4
    characters = string.ascii_lowercase + string.digits  # Include both letters and digits
    random_string = ''.join(random.choice(characters) for _ in range(4))
    bucket_name = "websites-tf-" + random_string

    print(bucket_name)


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
    print(f"New Bucket: {bucket_name} Created")
    return bucket_name



## Make the DynamoDB Table #####

def create_dynamodb_table(region):

    ## Global 
    print("Working on DynamoDB for State Locking")
    table_name = "terraform-state-locking"
    dynamo_client = boto3.client('dynamodb', region_name=region)

    # List existing tables
    existing_tables = dynamo_client.list_tables()['TableNames']

    # Check if our table already exists
    if table_name in existing_tables:
        print(f"✅ Found existing DynamoDB table: {table_name}")
        return table_name  # stop here, no need to create    


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

    print(f"\n✅ Dynamo Table: {table_name} created successfully\n")
    return table_name

################ Run AWS functions ################

bucket_name = create_bucket(region)
create_dynamodb_table(region)




########################  JINJA2 Section #############################


# Makes initial Folder 
output_dir = os.path.join( "..", dir_name)
os.makedirs(output_dir, exist_ok=True)


# Establish Jinja Tempalt Directory and templates
template_dir = "templates"
env = Environment(loader=FileSystemLoader(template_dir))

# === Step 3: Template context ===
context = {
    "bucket": bucket_name,
    "region": region,
    "website-type": website_type,
    "website-name": website_name
}

# === Step 4: List of template files to process ===
template_files = [
    "providers.tf.j2",
    "data.tf.j2",
    "main.tf.j2",
    "outputs.tf.j2"
]

# === Step 5: Render each file ===
for template_file in template_files:
    template = env.get_template(template_file)
    rendered = template.render(context)

    # Output filename (strip .j2 extension)vv 
    output_filename = template_file.replace(".j2", "")
    output_path = os.path.join(output_dir, output_filename)

    with open(output_path, "w") as f:
        f.write(rendered)

print(f"\n✅ Terraform Provider File generated for {dir_name}\n")





