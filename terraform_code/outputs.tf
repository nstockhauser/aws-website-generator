

output "al2-ssh-login" {
  value = "ssh ${local.ssh_user}@${aws_instance.website.public_ip} -i local-key" #UBUNTU
}

output "wordpress-url" {
  value = "http://${aws_instance.website.public_ip}"
}



output "my_public_ip" {
  value = data.http.curl_public_ip.body
}

