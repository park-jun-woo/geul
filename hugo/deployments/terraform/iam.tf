# deployments/terraform/iam.tf
# 사이트 배포 + 통계 수집 전용 IAM 유저

resource "aws_iam_user" "deployer" {
  name = "${var.project}-deployer"
  tags = local.tags
}

resource "aws_iam_user_policy" "deployer" {
  name = "${var.project}-deployer-policy"
  user = aws_iam_user.deployer.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      # S3: 사이트 배포 (public 버킷 쓰기/삭제)
      {
        Sid    = "DeploySync"
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:GetObject",
          "s3:ListBucket",
        ]
        Resource = [
          module.bucket_public.s3_bucket_arn,
          "${module.bucket_public.s3_bucket_arn}/*",
        ]
      },
      # S3: 로그 다운로드 (logs 버킷 읽기 전용)
      {
        Sid    = "DownloadLogs"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket",
        ]
        Resource = [
          module.bucket_logs.s3_bucket_arn,
          "${module.bucket_logs.s3_bucket_arn}/*",
        ]
      },
      # CloudFront: 캐시 무효화
      {
        Sid    = "InvalidateCache"
        Effect = "Allow"
        Action = [
          "cloudfront:CreateInvalidation",
        ]
        Resource = [
          aws_cloudfront_distribution.cdn_public.arn,
        ]
      },
    ]
  })
}
