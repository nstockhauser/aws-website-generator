terraform {
  backend "s3" {
    bucket         = "3z9z8b4b1e4vy00ufn56g4rwf"
    key            = "tf-dev/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-locking"
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }

    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }

    http = {
      source  = "hashicorp/http"
      version = "3.3.0"
    }

  }
}

#### Windows
provider "aws" {
  shared_config_files      = ["${pathexpand("~/.aws/config")}"]
  shared_credentials_files = ["${pathexpand("~/.aws/credentials")}"]
  profile                  = "tf-user"
  region                   = "us-east-1"



  default_tags {
    tags = {
      Environment = "Lab"
    }
  }

}

