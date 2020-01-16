import requests
import re


def get_likers(image_link):
    who_liked = []
    end_cursor = "first_attempt"
    query_hash_like = "e0f59e4a1c8d78d0161873bc2ee7ec44"
    short_code = image_link.split("/")[4]

    session = requests.Session()
    response = session.get(image_link)
    csrf_token = re.search('"csrf_token":"(.*?)"', response.text)[1]
    session.headers.update({"X-CSRFToken": csrf_token})

    while True:
        if end_cursor == "first_attempt":
            query_variable = '{"shortcode":"' + short_code + '","first":50}'
        else:
            query_variable = '{"shortcode":"' + short_code + '","first":50,"after":"' + end_cursor + '"}'
        payload = {"query_hash": query_hash_like, "variables": query_variable}
        json_response = session.get("https://www.instagram.com/graphql/query/?", params=payload).json()
        end_cursor = json_response["data"]["shortcode_media"]["edge_liked_by"]["page_info"]["end_cursor"]
        users = json_response["data"]["shortcode_media"]["edge_liked_by"]["edges"]
        for user in users:
            who_liked.append(user["node"]["username"])
        if end_cursor is None:
            break
        
    return who_liked
