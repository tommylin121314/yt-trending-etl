CATEGORIES = {
    "1": "Film & Animation", 
    "2": "Autos & Vehicles", 
    "10": "Music", 
    "15": "Pets & Animals", 
    "17": "Sports", 
    "18": "Short Movies", 
    "19": "Travel & Events", 
    "20": "Gaming", 
    "21": "Videoblogging", 
    "22": "People & Blogs", 
    "23": "Comedy", 
    "24": "Entertainment", 
    "25": "News & Politics", 
    "26": "Howto & Style", 
    "27": "Education", 
    "28": "Science & Technology", 
    "29": "Nonprofits & Activism", 
    "30": "Movies", 
    "31": "Anime/Animation", 
    "32": "Action/Adventure", 
    "33": "Classics", 
    "34": "Comedy", 
    "35": "Documentary", 
    "36": "Drama", 
    "37": "Family", 
    "38": "Foreign", 
    "39": "Horror", 
    "40": "Sci-Fi/Fantasy", 
    "41": "Thriller", 
    "42": "Shorts", 
    "43": "Shows", 
    "44": "Trailers"
}

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
        "Views": view_count, 
        "Likes": like_count, 
        "Comments": comment_count
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