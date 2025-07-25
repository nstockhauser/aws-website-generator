

output "instance-ssh-login" {
  value = "ssh ubuntu@${aws_instance.website.public_ip} -i local-key"
}

output "wordpress-url" {
  value = "http://${aws_instance.website.public_ip}/wp-admin"
}


output "your_public_ip" {
  value = data.http.curl_public_ip.body
}

