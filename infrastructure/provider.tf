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
  access_key = "AKIA3CSPUR2NK6WXCE6X"
  secret_key = "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"
}

