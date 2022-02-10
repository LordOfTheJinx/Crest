
import boto3
import boto3.session
import json
import datetime
from botocore.exceptions import ClientError
import logging
import os

# Create your own session
curr_session = boto3.session.Session(
    aws_access_key_id=None, \
    aws_secret_access_key=None, \
    aws_session_token=None, \
    region_name=None \
    )
# Create a client in the session
crawler = curr_session.client('s3')

def list_buckets():
    # Get the list of all the buckets 
    response = crawler.list_buckets()
    # Print the list of buckets
    for i in range(len((response.get('Buckets')))):
        print(response.get('Buckets')[i].get('Name'))

def list_objects():
    #bucket = input("The Name of the bucket to look in: ")
    bucket = 'mumbai-new-kops-example-com-state-store'
    response = crawler.list_objects(Bucket = bucket)
    for items in range(len(response.get('Contents'))):
        for keys in ['Key' , 'Size']:
            print(response.get('Contents')[items].get(keys), end = ' ')
        print('\n')

def create_bucket(bucket_name , region):
        try:
            crawler.create_bucket(Bucket=bucket_name)
        except ClientError as brr:
            logging.error(brr)
        else:
            location = {'LocationConstraint': region}
            crawler.create_bucket(Bucket=bucket_name, \
                                CreateBucketConfiguration=region)

def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    # Upload the file
    try:
        response = crawler.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)


wish = 100

while wish != 0:
    wish = int(input("""
++++++++++++++++++++++++++++++++++++
+++++What would you like to do?+++++
++++++++++++++++++++++++++++++++++++
\n########################################
Select your choice
 1) List S3 buckets
 2) List Bucket Objects
 3) Create Bucket
 4) Upload File
 0) Exit
########################################=====>"""))
    if wish == 1:
        list_buckets()
    if wish == 2:
        list_objects()
    if wish == 3:
        bucket_name , region = input("Bucket name to create and region : ").split()
        create_bucket(bucket_name,region)
    if wish == 4:
        file_name, bucket, object_name = input("Local File , Bucket , Destination Name: ").split()
        upload_file(file_name, bucket, object_name=None)