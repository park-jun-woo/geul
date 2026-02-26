# deployments/terraform/main.tf

terraform {
  required_version = ">= 1.5.0"

  backend "s3" {}

  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.95.0" }
  }
}

provider "aws" {
  region = var.aws_region
}

provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"
}

locals {
  zone_id = data.aws_route53_zone.main.zone_id
  tags = {
    Project   = var.project
    Workspace = terraform.workspace
  }
}

# Route53 Hosted Zone (도메인 등록 시 자동 생성됨 — data source로 참조)
data "aws_route53_zone" "main" {
  name         = var.domain
  private_zone = false
}

# Google Search Console 도메인 인증
resource "aws_route53_record" "txt_google_verification" {
  zone_id = local.zone_id
  name    = var.domain
  type    = "TXT"
  ttl     = 300

  records = [
    "google-site-verification=PLACEHOLDER",
  ]
}

# Gmail MX 레코드
resource "aws_route53_record" "mx_gmail" {
  zone_id = local.zone_id
  name    = var.domain
  type    = "MX"
  ttl     = 86400 * 7

  records = [
    "1 ASPMX.L.GOOGLE.COM.",
    "5 ALT1.ASPMX.L.GOOGLE.COM.",
    "5 ALT2.ASPMX.L.GOOGLE.COM.",
    "10 ALT3.ASPMX.L.GOOGLE.COM.",
    "10 ALT4.ASPMX.L.GOOGLE.COM.",
  ]
}
