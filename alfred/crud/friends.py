from asyncpg import Connection
from alfred.models import Friend, FriendInDB
from typing import List, Union
from uuid import UUID
import logging


async def create_friend(conn: Connection, friend: Friend) -> FriendInDB:
    row = await conn.fetchrow(
        f"""
        INSERT INTO {str(friend)}(client_id, first_name, last_name, phone_number, birthday)
        VALUES($1, $2, $3, $4, $5)
        RETURNING *
        """,
        friend.client_id,
        friend.first_name,
        friend.last_name,
        friend.phone_number,
        friend.birthday,
    )
    if row:
        return FriendInDB(**row)
    else:
        raise UserWarning(f"{str(friend).capitalize()} could not be inserted into the db.")


async def update_friend(conn: Connection, friend: Friend) -> FriendInDB:

    row = await conn.fetchrow(
        f"""
        UPDATE {str(friend)}
        SET client_id = $1, first_name = $2, last_name = $3, phone_number = $4, birthday = $5
        RETURNING *
        """,
        friend.client_id,
        friend.first_name,
        friend.last_name,
        friend.phone_number,
        friend.birthday,
    )
    if row:
        return FriendInDB(**row)
    else:
        raise UserWarning(f"{str(friend).capitalize()} with id {friend.id} could not be updated.")


async def delete_friend(conn: Connection, friend_id: UUID) -> FriendInDB:
    row = await conn.fetchrow(
        """
        DELETE FROM friend
        WHERE id = $1
        RETURNING *
        """,
        friend_id,
    )
    if row:
        return FriendInDB(**row)
    else:
        raise UserWarning(f"FRIEND with id {friend_id} could not be deleted from the db.")


async def get_all_friends_by_client_id(conn: Connection, client_id: str) -> List[Union[FriendInDB, None]]:
    rows = await conn.fetch(
        """
        SELECT * FROM friend
        WHERE client_id = $1
        """,
        client_id,
    )

    if rows:
        return [FriendInDB(**row) for row in rows]
    logging.warning(f"Could not find friends associated with client id: {client_id}.")
    return None


async def get_friends_by_date(conn: Connection, date_dict: dict) -> List[Union[FriendInDB, None]]:
    day = date_dict.get("day", "-1")
    month = date_dict.get("month", "-1")
    rows = await conn.fetch(
        """
        SELECT * FROM friend
        WHERE  date_part('day', birthday) = $1 AND date_part('month', birthday) = $2
        """,
        day,
        month,
    )
    if rows:
        return [FriendInDB(**row) for row in rows]
    logging.warning(f"No friends with birthdays on {month}/{day}")
    return None
