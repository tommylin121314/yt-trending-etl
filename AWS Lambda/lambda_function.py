import json
import boto3
import io
import csv
import os
from yt_etl import parse_first, parse_next, fetch_info
from googleapiclient.discovery import build
from datetime import datetime, timedelta


# FETCH YOUR YOUTUBE API DEVELOPER KEY HERE
def fetch_key():
    return None

# UPLOAD DATA TO YOUR S3 BUCKET HERE
def upload_to_s3():
    return None

def extract_youtube_trending():
    # Builds youtube connection
    youtube = build("youtube", 
                    "v3", 
                    developerKey=fetch_key())

    # Parses each page of returned data
    all_item_ids, all_snippets, all_stats, snip_req, snip_res = parse_first(youtube)
    while 'nextPageToken' in snip_res:
        item_ids, snippets, stats, snip_req, snip_res = parse_next(youtube, snip_req, snip_res)
        all_item_ids += item_ids
        all_snippets += snippets
        all_stats += stats

    # Transform parsed data
    top_200 = []
    for index, item_id in enumerate(all_item_ids):
        info = fetch_info(index+1, item_id, all_snippets[index], all_stats[index])
        top_200.append(info)
    
    return top_200

def lambda_handler(event, context):
    trending_data = extract_youtube_trending()
    upload_to_s3(trending_data)
    