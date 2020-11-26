from collections import defaultdict
from typing import DefaultDict, List

def group_friends_by_client_id(friends_list: List[FriendInDB] = []) -> DefaultDict:
    friend_map = defaultdict(list)
    for friend in friends_list:
        friend_map[friend.get("client_id")] = friend.first_name + " " + friend.last_name
    return friend_map