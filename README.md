Pre reqs:
aws account
Aws user with access and secret access keys. 
aws configure on your own terminal: 


python
terraform
pip
awscli

Destroy.py
import boto3
import os
from InquirerPy import inquirer


Generate.py
import os
from jinja2 import Environment, FileSystemLoader
import random
import string
import boto3
from InquirerPy import inquirer


the rest of this Readme.md is not completed or relevant. 

## Project Structure:

```bash
aws-tf-python-basics/
├── README.md
├── statelock_works.PNG
├── python_code/
│   ├── s3_bucket.txt
│   ├── tf_bootstrap.py
│   ├── tf_teardown.py
├── terraform_code/
│   ├── data.tf
│   ├── ec2.tf
│   ├── main.tf
│   ├── outputs.tf
│   ├── providers.tf
│   ├── userdata.sh
│   ├── variables.tf
```

## AWS Setup

- Active AWS Account

  - This is all done through the AWS website and it does require a credit card on file, you can still complete this project on a free tier account.

- AWS CLIv2 installed locally

  - This link is incredibly useful and will help you set this up regardless of OS. [Installing or updating to the latest version of the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

- Developer User and AccessKeys
  - This is done through the Identity Access Management (IAM) service inside of the AWS Console. You will first make a new user: [Create an IAM user in your AWS account](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html)
    - :exclamation: You do not need Console Access, but you do need to assign the AdministratorAccess IAM policy to this user.
  - Then you have to create AccessKeys for programmatic Access for that user in the AWS console **Make sure to download the CSV**: [Create new access keys for an IAM user](https://docs.aws.amazon.com/keyspaces/latest/devguide/create.keypair.html)
- Now you need to use the terminal box in your vscode editor and enter

```bash
aws configure


# follow the prompts with this information
AccessKey: See CSV you downloaded earlier
SecretKey: See CSV you downloaded earlier
region: us-east-1
output: json
```

To validate you did this all correctly run the command

```bash
aws sts get-caller-identity


## you should see something like this:
{
    "UserId": "AIDA2CEXAMPLEMKKXQ",
    "Account": "123456789101",
    "Arn": "arn:aws:iam::123456789101:user/developer"
}
```

## Python Setup

- First we need to cover the prerequisites:
  You need to install python v3, [Download Python](https://www.python.org/downloads/), make sure you add the to PATH (the optional setting when installing python)
- Verify python is installed:

```bash
python --version
Python 3.12.2
```

- Install dependencies
  - pip (python package installer): [install pip](https://bootstrap.pypa.io/get-pip.py)

```bash
# verify pip install
pip --version


# use pip to install other dependencies
pip install boto3
pip install botocore
```

## Terraform Setup

- [Terraform install](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) this covers major operating system differences

```bash
#verify Terraform was installed
terraform --version
```

## How to Use

Under the python folder run `python tf_bootstrap.py`, This will create and output the following:

- S3 bucket for your remote backend state location
- Dynamodb Table for State locking functionality
- IAM user called "tf-user" with credentials

After you run the tf_bootstrap.py you have to copy and paste the new tf-user credentials and configs into the appropriate files (**~/.aws/config** and **~/.aws/credentials**) and update the provider file in the **terraform/providers.tf** file.

```bash
#######  IAM TF-User information ##############


Copy this into the ~/user/.aws/credentials file


[tf-user]
aws_access_key_id = EXAMPLELQ7VCRJVXP4VH6
aws_secret_access_key = EXAMPLEV7eY7iAOBCVWvyy4nmZqZhgnJX6YEW


Copy this under the ~/user/.aws/config file


[tf-user]
region = us-east-1
output = json


```

```bash
#######  S3 Bucket Info ##############


Bucket Name: 1z5s9grnp8audqovsrnck2huz created successfully


Replace the backend resource block in the provider tab with:


  backend "s3" {
    bucket         = "1z5s9grnp8audqovsrnck2huz"
    key            = "tf-dev/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-locking"
    encrypt        = true
  }
```

Now move into the terraform folder and run:

```bash
# Initialize your Terraform providers
terraform init


#Show what is going to be built
terraform plan


#Actually build the infrastructure
terraform apply -y
```

This will create the network infrastructure and systems for this project and will output the following values:

- an SSH command you can copy and paste to get into the server
- your Public IP address (for validation)
- the url of the public website.

## Cleanup

1. In the terraform repo, run `terraform destroy`
2. delete local terraform files from repo (**.terraform** and **.terraform.lock.hcl**)
3. run the `python python/tf_teardown.py` script
4. delete the tf-user credentials and configs in your **~/.aws/config** and **~/.aws/credentials** folder
5. In both **python/s3_bucket.txt** and in **terraform/providers.tf** replace the bucket string with <placeholder>

Useful Commands:
curl https://ipinfo.io/ip
-> Grab Public IP. (output as string)

---

### Future release notes:

- Cloudformation for initial IAM user creation
- More secure custom policies instead of AdminAccess
- Companion Video on Youtube
- Companion Blog on Website
