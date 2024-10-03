variable "domain_name" {
  description = "domain name"
  type        = string
}

variable "zone_id" {
  description = "route53 domain zone id"
  type        = string
}

variable "domain_identity_type" {
  description = "aws route53 verification record type"
  type        = string
}

variable "ttl" {
  description = "time to load value"
  type        = number
}

variable "dkim_record_type" {
  description = "dkim record type"
  type        = string
}