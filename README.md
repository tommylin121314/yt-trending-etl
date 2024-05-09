# YouTube Trending ETL Pipeline
## Overview
The YouTube Trending ETL Pipeline was created to collect data on YouTube's top 200 videos on an hourly basis. It uses Python code to perform the ETL, which is packaged into an AWS Lambda function. The function is called every hour using an AWS EventBridge scheduler. The data is stored as a .csv file and uploaded into an AWS S3 bucket. Finally, that data is queried into Tableau where the user can analyze it and create visualizations.

## Architecture
![architecture](architecture.png)
