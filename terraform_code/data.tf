
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

################################ AL AMI (LATEST) #################################

data "aws_ami" "amazon" {
  most_recent = true

  filter {
    name   = "name"
    values = ["amzn2-ami-kernel-*-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["amazon"] #Ubuntu
}



################################# Public IP Pull #################################
data "http" "curl_public_ip" {
  url    = "https://ipinfo.io/ip"
  method = "GET"
}

