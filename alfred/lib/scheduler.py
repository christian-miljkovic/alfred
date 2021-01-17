from collections import defaultdict
from typing import DefaultDict, List
from alfred.models import FriendInDB


def group_friends_by_client_id(friends_list: List[FriendInDB] = []) -> DefaultDict:
    friend_map = defaultdict(list)
    # should add some sort of unique id here
    for friend in friends_list:
        friend_map[str(friend.client_id)].append(friend.first_name + " " + friend.last_name)
    return friend_map
