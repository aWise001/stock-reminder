resource "aws_ses_domain_identity" "ses_domain" {
    domain = var.domain_name
}

resource "aws_route53_record" "domain_identity_record" {
    zone_id = var.zone_id
    name = aws_ses_domain_identity.ses_domain.verification_token
    type = var.domain_identity_type
    ttl = var.ttl
    records = [aws_ses_domain_identity.ses_domain.verification_token]
}

resource "aws_ses_domain_dkim" "ses_dkim" {
    domain = aws_ses_domain_identity.ses_domain.domain
}

resource "aws_route53_record" "dkim_record" {
    count = length(aws_ses_domain_dkim.ses_dkim.dkim_tokens)
    zone_id = var.zone_id
    name = "${element(aws_ses_domain_dkim.ses_dkim.dkim_tokens, count.index)}._domainkey.${var.domain_name}"
    type = var.dkim_record_type
    ttl = var.ttl
    records = ["${element(aws_ses_domain_dkim.ses_dkim.dkim_tokens, count.index)}.dkim.amazonses.com"]
}

resource "aws_ses_domain_identity_verification" "name" {
  domain = aws_ses_domain_identity.ses_domain.id
  depends_on = [ aws_route53_record.domain_identity_record ]
}