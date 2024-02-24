"""
Primary source file used to get a unique set of users from multiple groups,
get all groups that those users are in, and then tally up how many of the
unique users are in each of these groups in total as a sorted dict.
"""

import groups
import time

def convert_tuples_list_to_dict(tuples_list: list[tuple]) -> dict:
    """Converts a list of tuples into a dict."""

    if not type(tuples_list) is list:
        raise ValueError("Function argument 'tuples_list' must be a list.")

    holder = {}

    for tuple in tuples_list:
        holder[tuple[0]] = tuple[1]

    return holder

if __name__ == "__main__":
    # Amount of users to collect from each group.
    limit = 10
    # Integers for group IDs you want to check first.
    group_ids = []
    # The file where you want the results to be logged.
    results_file = "groups.txt"
    # Time to wait in between checking each user's groups.
    time_to_wait = 1

    # DO NOT MODIFY ANYTHING BELOW THIS LINE!

    print("Retrieving users from each group...")

    group_user_ids = groups.get_members_of_groups(group_ids, limit)
    results = {}

    print(f"{len(group_user_ids)} unique users were found.")
    print("Checking user groups now...")

    for iterator, user_id in enumerate(group_user_ids):
        user_groups = groups.get_user_groups(user_id)

        for group in user_groups:
            group_id = group["id"]

            if not group_id in results:
                results[group_id] = 1
            else:
                results[group_id] = results[group_id] + 1
        
        if (iterator + 1) % limit == 0:
            print(f"{iterator + 1}/{len(group_user_ids)} users processed.")
        
        # Artifical limitation here to avoid too many requests (HTTP 429).
        time.sleep(time_to_wait)

    # Fancy way of sorting list in descending order.
    results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    results = convert_tuples_list_to_dict(results)

    with open(results_file, "w") as log:
        for group_id in results:
            users = results[group_id]
            log.write(f"https://www.roblox.com/groups/{group_id} - {users}\n")