# deployments/terraform/public.tf

locals {
  public_domain      = "www.${var.domain}"
  public_site_name   = "${var.project}-public"
  public_bucket_name = "${var.project}-org-public"
  log_bucket_name    = "${var.project}-logs"
  public_tags = {
    Project   = var.project
    Workspace = terraform.workspace
    Site      = "public"
  }
}

data "aws_cloudfront_cache_policy" "CachingOptimized" {
  name = "Managed-CachingOptimized"
}

# ACM 인증서 (www.geul.org + geul.org)
module "acm_site_public" {
  source  = "terraform-aws-modules/acm/aws"
  version = "~> 5.1.1"
  providers = {
    aws = aws.us_east_1
  }
  domain_name               = local.public_domain
  subject_alternative_names = [var.domain]
  validation_method         = "DNS"
  zone_id                   = local.zone_id
  tags                      = local.public_tags
}

# 정적 사이트 S3 버킷
module "bucket_public" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "4.7.0"
  providers = {
    aws = aws
  }
  bucket        = local.public_bucket_name
  versioning    = { enabled = false }
  force_destroy = false
  tags          = local.public_tags
}

# CloudFront 로그 버킷
module "bucket_logs" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "4.7.0"
  providers = {
    aws = aws
  }
  bucket        = local.log_bucket_name
  versioning    = { enabled = false }
  force_destroy = false

  object_ownership         = "BucketOwnerPreferred"
  control_object_ownership = true
  acl                      = "log-delivery-write"

  lifecycle_rule = [
    {
      id      = "expire-old-logs"
      enabled = true
      expiration = {
        days = 90
      }
    }
  ]

  tags = local.public_tags
}

# OAC (S3 접근 제어)
resource "aws_cloudfront_origin_access_control" "oac_public" {
  provider                          = aws.us_east_1
  name                              = "${local.public_site_name}-oac"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

# CloudFront Function (URL 리라이트)
resource "aws_cloudfront_function" "public_router" {
  name    = "${local.public_site_name}-router"
  runtime = "cloudfront-js-2.0"
  comment = "URL rewrite for Hugo static site"
  publish = true

  code = file("${path.module}/functions/cloudfront-public-router.js")
}

# CloudFront Distribution
resource "aws_cloudfront_distribution" "cdn_public" {
  provider            = aws.us_east_1
  enabled             = true
  comment             = local.public_site_name
  default_root_object = "index.html"
  aliases             = [local.public_domain, var.domain]

  logging_config {
    bucket          = module.bucket_logs.s3_bucket_bucket_regional_domain_name
    prefix          = "cdn/"
    include_cookies = false
  }

  origin {
    origin_id                = local.public_site_name
    domain_name              = module.bucket_public.s3_bucket_bucket_regional_domain_name
    origin_access_control_id = aws_cloudfront_origin_access_control.oac_public.id
  }

  default_cache_behavior {
    target_origin_id       = local.public_site_name
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD", "OPTIONS"]
    cached_methods         = ["GET", "HEAD", "OPTIONS"]
    compress               = true
    cache_policy_id        = data.aws_cloudfront_cache_policy.CachingOptimized.id
    trusted_key_groups     = null
    function_association {
      event_type   = "viewer-request"
      function_arn = aws_cloudfront_function.public_router.arn
    }
  }

  viewer_certificate {
    acm_certificate_arn      = module.acm_site_public.acm_certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  custom_error_response {
    error_code            = 403
    response_page_path    = "/404.html"
    response_code         = 404
    error_caching_min_ttl = 300
  }
  custom_error_response {
    error_code            = 404
    response_page_path    = "/404.html"
    response_code         = 404
    error_caching_min_ttl = 300
  }
  custom_error_response {
    error_code            = 500
    response_page_path    = "/404.html"
    response_code         = 404
    error_caching_min_ttl = 300
  }

  tags = local.public_tags
}

# Route53 A 레코드 (www → CloudFront)
resource "aws_route53_record" "alias_public" {
  zone_id = local.zone_id
  name    = local.public_domain
  type    = "A"
  alias {
    name                   = aws_cloudfront_distribution.cdn_public.domain_name
    zone_id                = aws_cloudfront_distribution.cdn_public.hosted_zone_id
    evaluate_target_health = false
  }
}

# Route53 A 레코드 (root → CloudFront)
resource "aws_route53_record" "alias_public2" {
  zone_id = local.zone_id
  name    = var.domain
  type    = "A"
  alias {
    name                   = aws_cloudfront_distribution.cdn_public.domain_name
    zone_id                = aws_cloudfront_distribution.cdn_public.hosted_zone_id
    evaluate_target_health = false
  }
}

# S3 버킷 정책 (CloudFront OAC 읽기 허용)
resource "aws_s3_bucket_policy" "bucket_public_oac" {
  bucket = module.bucket_public.s3_bucket_id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid       = "AllowCloudFrontOACRead"
        Effect    = "Allow"
        Principal = {
          Service = "cloudfront.amazonaws.com"
        }
        Action   = ["s3:GetObject"]
        Resource = "${module.bucket_public.s3_bucket_arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = aws_cloudfront_distribution.cdn_public.arn
          }
        }
      }
    ]
  })
}
