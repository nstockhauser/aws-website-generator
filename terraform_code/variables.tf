

################# VARIABLES #################


variable "vpc_cidr_block" {
  type        = string
  description = "Base CIDR Block for VPC"
  default     = "10.0.0.0/16"
}

variable "subnet-1" {
  type        = string
  description = "Public CIDR Block for Subnet 1 in VPC"
  default     = "10.0.1.0/24"
}




variable "subnet_list" {
  description = "AWS Subnets"
  type        = list(string)
  default     = ["use1-az1", "use1-az2", "use1-az3"]
}


variable "instance_type" {
  type        = string
  description = "Type for EC2 Instnace"
  default     = "t2.micro"
}

variable "name_tag" {
  type        = string
  description = "AWS Lab"
  default     = "AWS Lab"
}

