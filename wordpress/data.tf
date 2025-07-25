
######################### Default infrastructure Data #############

data "aws_vpc" "default" {
  default = true
}


data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "random_shuffle" "subnet_pick" {
  input        = data.aws_subnets.default.ids
  result_count = 1
}


data "aws_security_group" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
  filter {
    name   = "group-name"
    values = ["default"]
  }
}


################################# UBUNTU IMAGE (LATEST) #################################

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-*-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] #Ubuntu
}



################################# Public IP Pull #################################
data "http" "curl_public_ip" {
  url    = "https://ipinfo.io/ip"
  method = "GET"
}

