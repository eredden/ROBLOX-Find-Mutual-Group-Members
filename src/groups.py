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

    response = raw_response.json()
    
    groups = []

    for group in response["data"]:
        groups.append(group["group"])

    return groups

def get_members_of_group(group_id: int, limit: int) -> set:
    """Returns a set of unique user IDs from a group."""

    api = f"https://groups.roblox.com/v1/groups/{group_id}/users" \
        f"?limit=10&sortOrder=Desc"

    if not type(group_id) is int:
        raise ValueError("Function argument 'group_id' must be an integer.")
    
    if not type(limit) is int:
        raise ValueError("Function argument 'limit' must be an integer.")

    cursor = "  "
    users = set()

    while cursor:
        if len(users) + 10 > limit: break

        raw_response = requests.get(api + "&cursor=" + cursor)
        raw_response.raise_for_status()

        response = raw_response.json()

        for user in response["data"]:
            users.add(user["user"]["userId"])
        
        cursor = response["nextPageCursor"]

    return users

def log_common_groups(user_id: int, output: dict) -> None:
    """
    Gets groups that a user is in and logs them into an output dict as
    a tuple, containing the group ID and the number of common users
    in that group (added through subsequent runs of this function).
    """

    user_groups = get_user_groups(user_id)

    for group in user_groups:
        group_id = group["id"]

        if not group_id in output:
            output[group_id] = 1
        else:
            output[group_id] = output[group_id] + 1