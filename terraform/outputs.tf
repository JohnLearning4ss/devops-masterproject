output "server_ip" {
  description = "Public IP of your app server"
  value       = aws_eip.app_eip.public_ip
}

output "app_url" {
  description = "URL to access your app"
  value       = "http://${aws_eip.app_eip.public_ip}"
}

output "grafana_url" {
  description = "URL to access Grafana"
  value       = "http://${aws_eip.app_eip.public_ip}:3000"
}
