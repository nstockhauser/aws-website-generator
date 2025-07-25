



################################# SECURITY GROUP #################################


resource "aws_security_group_rule" "allow_in_443" {
  type              = "ingress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = data.aws_security_group.default.id
}

resource "aws_security_group_rule" "allow_in_80" {
  type              = "ingress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = data.aws_security_group.default.id
}

resource "aws_security_group_rule" "allow_in_22" {
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["${data.http.curl_public_ip.body}/32"]
  security_group_id = data.aws_security_group.default.id
}









#################### Bastion Host ###########################
resource "aws_instance" "website" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t2.micro"
  subnet_id                   = random_shuffle.subnet_pick.result[0]
  associate_public_ip_address = true
  vpc_security_group_ids      = [data.aws_security_group.default.id]
  key_name                    = aws_key_pair.deployer.key_name

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "optional"
  }

  user_data = file("../build/apache.sh")

  tags = {
    Name = "Website"
  }

}






################### Key Pairs  ##################

####   SSH Keys and PEM File ########

resource "aws_key_pair" "deployer" {
  key_name   = "instance-key"
  public_key = tls_private_key.rsa.public_key_openssh
}

resource "tls_private_key" "rsa" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "local_file" "test-key" {
  content  = tls_private_key.rsa.private_key_pem
  filename = "local-key"

}

