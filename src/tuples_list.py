"""
Source file containing functions for working with lists of tuples.
"""

def convert_to_dict(tuples_list: list[tuple]) -> dict:
    """Converts a list of tuples into a dict."""

    if not type(tuples_list) is list:
        raise ValueError("Function argument 'tuples_list' must be a list.")

    holder = {}

    for tuple in tuples_list:
        holder[tuple[0]] = tuple[1]

    return holder