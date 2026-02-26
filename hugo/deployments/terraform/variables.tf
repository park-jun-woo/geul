# deployments/terraform/variables.tf

variable "project" {
  description = "프로젝트명, 예: geul"
  type        = string
}

variable "aws_region" {
  description = "예: ap-northeast-2"
  type        = string
}

variable "domain" {
  description = "루트 도메인, 예: geul.org"
  type        = string
}
