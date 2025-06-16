

output "al2-ssh-login" {
  value = "ssh ${local.ssh_user}@${aws_instance.test_wordpress.public_ip} -i local-key" #UBUNTU
}

output "wordpress-url" {
  value = "http://${aws_instance.test_wordpress.public_ip}/wp-admin"
}



output "my_public_ip" {
  value = data.http.curl_public_ip.body
}

