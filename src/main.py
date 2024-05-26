"""
Primary source file used to get a unique set of users from multiple groups,
get all groups that those users are in, and then tally up how many of the
unique users are in each of these groups in total as a sorted dictionary.
"""

import time
import concurrent.futures

import groups
import tuples_list

if __name__ == "__main__":
    """
    user_limit - Maximum # of users to check from each group.
    group_ids - Group IDs with users to check for mutual groups.
    minimum_common_users - Minimum # of users to have a group recorded.
    results_file - Where all common groups are listed with mutual user counts. 
    time_to_wait - Time in seconds to wait between sending HTTP requests.
    """

    user_limit = 10
    group_ids = []
    minimum_common_users = 2
    results_file = "groups.txt"
    time_to_wait = 0.5

    # DO NOT MODIFY ANYTHING BELOW THIS LINE!

    # Get set of users from supplied groups.
    print("Retrieving users from each group...")

    user_ids = set()

    for group_id in group_ids:
        for id in groups.get_members_of_group(group_id, user_limit):
            user_ids.add(id)

    print(f"{len(user_ids)} unique users were found.")

    # Using multithreading to check multiple user groups at the same time.
    print("Retrieving user groups now...")

    results = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for id in user_ids:
            executor.submit(groups.log_common_groups, id, results)
            time.sleep(time_to_wait)

    print(f"{len(results)} unique groups were found.")

    # Fancy way of sorting list of tuples in descending order.
    results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    results = tuples_list.convert_to_dict(results)

    # Remove groups without multiple common users.
    for group_id in list(results):
        if results[group_id] < minimum_common_users:
            results.pop(group_id)
    
    print(f"{len(results)} groups have more than {minimum_common_users} members.")
    print(f"Logging results to {results_file}...")

    # Log results to desired text file.
    with open(results_file, "w") as log:
        for group_id in results: 
            log.write(f"https://www.roblox.com/groups/{group_id} - {results[group_id]}\n")
    
    print(f"Results have been logged to {results_file}.")