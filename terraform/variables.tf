variable "aws_region" {
  description = "AWS region to deploy in"
  default     = "us-east-1"
}

variable "ami_id" {
  description = "Ubuntu 22.04 AMI ID (us-east-1)"
  default     = "ami-0c7217cdde317cfec"
}

variable "instance_type" {
  description = "EC2 instance size"
  default     = "t3.micro"  # Free tier eligible
}

variable "key_name" {
  description = "Name of your AWS key pair (for SSH)"
  default     = "devops-key"
}
