import hashlib
import requests
import re

def get_likers(link):
    
    def calculate_x_instagram_gis(rhx_gis, variables):
        text = rhx_gis + ":" + variables
        x_i_gis = hashlib.md5(text.encode()).hexdigest()
        return x_i_gis

    who_liked = []
    end_cursor = "first_attempt"
    query_hash_like = "e0f59e4a1c8d78d0161873bc2ee7ec44"
    short_code = link.split("/")[4]
    user_agent = "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.127"
    header = {"user-agent": user_agent}

    s = requests.Session()
    s.headers.update(header)
    r = s.get(link)

    rhx_gis = re.findall('rhx_gis":"(.*?)"',r.text)[0]

    while True:
        if end_cursor == "first_attempt":
            query_variable = '{"shortcode":"' + short_code + '","include_reel":true,"first":50}'
        else:
            query_variable = '{"shortcode":"' + short_code + '","include_reel":true,"first":50,"after":"' + end_cursor + '"}'
           
        x_instagram_gis = calculate_x_instagram_gis(rhx_gis, query_variable)
        header = {"user-agent": user_agent, "x-instagram-gis": x_instagram_gis}
        s.headers.update(header)
        
        payload = {"query_hash": query_hash_like,"variables" : query_variable}
        r = s.get("https://www.instagram.com/graphql/query/?", params = payload)
        json_response = r.json()
        end_cursor = json_response["data"]["shortcode_media"]["edge_liked_by"]["page_info"]["end_cursor"]
        users = json_response["data"]["shortcode_media"]["edge_liked_by"]["edges"]
        
        for user in users:
            who_liked.append(user["node"]["username"])
        if end_cursor is None:
            break
            
    return who_liked
