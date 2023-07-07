import boto3

bucket_name = 'vcf-userinfo-nfc'

def upload_vcf_to_bucket(vcf_file, user):

    s3_client = boto3.client('s3', aws_access_key_id='AKIASBMOA6HRYNLZF4FR', aws_secret_access_key='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')
    s3_client.upload_file(vcf_file, bucket_name, user.vcarf_file_path)
    return True

def get_bucket_url(vcf_file):

    # Create an S3 client
    s3_client = boto3.client('s3', aws_access_key_id='AKIASBMOA6HRYNLZF4FR', aws_secret_access_key='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')

    # Generate a presigned URL for the object in the bucket
    object_key = vcf_file
    expiration_time = 2629744  # URL expiration time in seconds
    presigned_url = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name, 'Key': object_key},
                                                    ExpiresIn=expiration_time)
    return presigned_url
