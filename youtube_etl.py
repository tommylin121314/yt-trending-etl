from googleapiclient.discovery import build
from config import config
import pandas as pd
from youtube_constants import CATEGORIES

def fetch_id(response_item):
    return response_item["id"]

def fetch_title(response_snippet):
    return response_snippet["title"]

def fetch_published_at(response_snippet):
    return response_snippet["publishedAt"]

def fetch_channel_title(response_snippet):
    return response_snippet["channelTitle"]

def fetch_category(response_snippet):
    cat_id = response_snippet["categoryId"]
    return CATEGORIES[cat_id]

def fetch_view_count(response_statistics):
    return response_statistics["viewCount"]

def fetch_like_count(response_statistics):
    try:
        return response_statistics["likeCount"]
    except KeyError:
        return 0 
    
def fetch_comment_count(response_statistics):
    try:
        return response_statistics["commentCount"]
    except KeyError:
        return 0
    
def fetch_info(rank, video_id, response_snippet, response_statistics):
    title = fetch_title(response_snippet)
    published_at = fetch_published_at(response_snippet)
    channel_title = fetch_channel_title(response_snippet)
    category = fetch_category(response_snippet)
    view_count = fetch_view_count(response_statistics)
    like_count = fetch_like_count(response_statistics)
    comment_count = fetch_comment_count(response_statistics)
    return {
        "Rank": rank,
        "Video ID": video_id, 
        "Title": title, 
        "Publish Time": published_at, 
        "Channel": channel_title, 
        "Category": category, 
        "Views": int(view_count), 
        "Likes": int(like_count), 
        "Comments": int(comment_count)
    }

def parse_first(youtube):
    snip_req = youtube.videos().list(part="snippet",
                                     chart='mostPopular',
                                     regionCode='US',
                                     maxResults=50)
    snip_res = snip_req.execute()
    item_ids = [item["id"] for item in snip_res['items']]
    snippets = [item["snippet"] for item in snip_res['items']]
    stats_req = youtube.videos().list(part="statistics",id=item_ids)
    stats_res = stats_req.execute()
    stats = [item["statistics"] for item in stats_res['items']]
    return item_ids, snippets, stats, snip_req, snip_res

def parse_next(youtube, snip_req, snip_res):
    snip_req = youtube.videos().list_next(snip_req, snip_res)
    snip_res = snip_req.execute()
    item_ids = [item["id"] for item in snip_res['items']]
    snippets = [item["snippet"] for item in snip_res['items']]
    stats_req = youtube.videos().list(part="statistics",id=item_ids)
    stats_res = stats_req.execute()
    stats = [item["statistics"] for item in stats_res['items']]
    return item_ids, snippets, stats, snip_req, snip_res

def extract_youtube_trending():
    youtube = build(config["API_NAME"], 
                    config["API_VERSION"], 
                    developerKey=config["API_KEY"])

    all_item_ids, all_snippets, all_stats, snip_req, snip_res = parse_first(youtube)
    while 'nextPageToken' in snip_res:
        item_ids, snippets, stats, snip_req, snip_res = parse_next(youtube, snip_req, snip_res)
        all_item_ids += item_ids
        all_snippets += snippets
        all_stats += stats

    top_200 = []
    for index, item_id in enumerate(all_item_ids):
        top_200.append(fetch_info(index+1, item_id, all_snippets[index], all_stats[index]))

    yt_df = pd.DataFrame.from_records(top_200)
    yt_df.to_csv("curr-yt-trending.csv")

extract_youtube_trending()