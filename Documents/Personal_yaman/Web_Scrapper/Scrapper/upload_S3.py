import boto3
import os
import glob
import configparser


def upload_and_delete_csv():
   config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'config.ini')
   dataset_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'DataSet','*.csv')
   config = configparser.ConfigParser()
   config.read(config_path)
   access_key = config['aws_credentials']['access_key'].strip()
   secret_key = config['aws_credentials']['secret_key'].strip()
   bucket_name = config['aws_credentials']['bucket_name'].strip()
   s3_client = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

    # Get the first CSV file in the directory
   csv_files = glob.glob(dataset_path)

   if not csv_files:
        return  # Exit if no CSV files are found

    # Assume we're uploading the first found CSV file
   file_name = csv_files[0]
   object_name = os.path.basename(file_name)  # Name in S3 will be the same as the local file name

   try:
        # Upload the file
        s3_client.upload_file(file_name, bucket_name, object_name)
        
        # Delete the file after uploading
        os.remove(file_name)
   except Exception:
        return  # Exit if there's an error during upload or deletion


   
# Call the function to upload the CSV file and delete it
upload_and_delete_csv()
