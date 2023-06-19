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
  access_key = "AKIA5VNRRBBVCJAG4IGZ"
  secret_key = "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"
}

