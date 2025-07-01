

################################# INFRASTRUCTURE #################################

################################# VPC  #################################
resource "aws_vpc" "vpc" {
  cidr_block           = var.vpc_cidr_block
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = var.name_tag
  }
}


################################# IGW #################################

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = var.name_tag
  }
}





#################################  SUBNETs #################################


resource "aws_subnet" "subnet-1" {
  cidr_block              = var.subnet-1
  vpc_id                  = aws_vpc.vpc.id
  map_public_ip_on_launch = true
  availability_zone_id    = var.subnet_list[0]

  tags = {
    Name = "Wordpress Subnet"
  }
}



################################# ROUTE TABLE #################################
resource "aws_route_table" "subnet-rtb" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = var.name_tag
  }
}

################################# ROUTE TABLE ASSOCIATION - SUBNET #################################

resource "aws_route_table_association" "subnet-1" {
  subnet_id      = aws_subnet.subnet-1.id
  route_table_id = aws_route_table.subnet-rtb.id
}



################################# SECURITY GROUP #################################

resource "aws_security_group" "website" {
  name   = "Wordpress SG"
  vpc_id = aws_vpc.vpc.id


  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["${data.http.curl_public_ip.body}/32"]
  }


  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Wordpress"
  }

}







### Locals ####


locals {
  ssh_user = (
    aws_instance.test_wordpress.ami == data.aws_ami.amazon.id ? "ec2-user" :
    aws_instance.test_wordpress.ami == data.aws_ami.ubuntu.id ? "ubuntu" :
    "ec2-user"
  )
}
