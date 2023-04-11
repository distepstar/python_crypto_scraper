import re


def get_item_by_regex(pattern, search_item, split_keyword=None):
    result = re.search(pattern, search_item)
    if result:
        result = result.group(0).split(split_keyword) if split_keyword is not None else result.group(0)
        return result
    else:
        return False
