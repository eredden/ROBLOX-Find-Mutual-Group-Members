"""
Source file containing functions for retrieving information from ROBLOX groups.
"""

import requests
from requests.exceptions import HTTPError

def get_user_groups(user_id: int) -> list:
    """Returns all names and IDs for groups that a ROBLOX user is in."""

    api = f"https://groups.roblox.com/v2/users/{user_id}/groups/roles"

    if not type(user_id) is int:
        raise ValueError("Function argument 'id' must be an integer.")

    raw_response = requests.get(api)
    raw_response.raise_for_status()

    json_response = raw_response.json()
    
    groups = []

    for item in json_response["data"]:
        groups.append(item["group"])

    return groups

def get_group_members(group_id: int, limit: int) -> list:
    """Returns a list of users in a group. Runs slowly."""

    cursor = "PLACEHOLDER"
    api = f"https://groups.roblox.com/v1/groups/{group_id}/users" \
        f"?limit=10&sortOrder=Desc"

    if not type(group_id) is int:
        raise ValueError("Function argument 'group_id' must be an integer.")
    
    if not type(limit) is int:
        raise ValueError("Function argument 'limit' must be an integer.")

    users = []

    while cursor:
        if cursor == "PLACEHOLDER":  
            cursor = ""
        
        raw_response = requests.get(f"{api}&cursor={cursor}")
        raw_response.raise_for_status()

        json_response = raw_response.json()

        for item in json_response["data"]:
            users.append(item)
        
        cursor = json_response["nextPageCursor"]

        if len(users) + 10 > limit: 
            break

    return users

def get_members_of_groups(group_ids: list[int], limit: int) -> set:
    """Returns unique user IDs (less than limit amount) from many groups."""

    group_user_ids = set()

    for group_id in group_ids:
        for member in get_group_members(group_id, limit):
            user_id = member["user"]["userId"]
            group_user_ids.add(user_id)
    
    return group_user_ids