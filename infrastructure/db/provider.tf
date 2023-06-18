terraform {
  required_providers {
    aws={
        source = "hashicorp/aws"
        version = "~>4.0"
    }
  }
}
provider "aws" {
  region = "us-east-1"
  access_key = "AKIA3ZD2WG2PC4DORPNW"
  secret_key = "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"
}

