The AWS Lambda folder contains two .zip files. These .zip files are used to create Lambda layers for the Lambda function that is responsible for extracting from YouTube API, performing transformations on the data, and loading the data into an AWS S3 Bucket. 

The .zip files should be unzipped, renamed to "python", then rezipped before creating a layer in AWS. 
Example: 'youtube_etl.zip' >> unzip >> 'youtube_etl' >> rename >> 'python' >> zip >> 'python.zip' >> create layer

These two layers will provide all the external dependencies needed to write the Lambda function.

The file "lambda_function.py" contains some base code used in the Lambda function that performs the ETL process. Personal access keys should be used where indicated.
