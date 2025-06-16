terraform {
  backend "s3" {
    bucket         = "nfvxulbsji0a73bqbzzt866fz"
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

