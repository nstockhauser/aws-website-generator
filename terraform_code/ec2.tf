

#################### Bastion Host ###########################
resource "aws_instance" "test_wordpress" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.subnet-1.id
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.website.id]
  private_ip                  = "10.0.1.100"
  key_name                    = "cloud-key"

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "optional"
  }

  user_data = file("userdata.sh")

  tags = {
    Name = "Wordpress Website"
  }

}






################### Key Pairs  ##################

####   SSH Keys and PEM File ########

resource "aws_key_pair" "deployer" {
  key_name   = "cloud-key"
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

