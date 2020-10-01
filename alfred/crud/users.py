from asyncpg import Connection
from alred.models import User


async def create_user(conn: Connection, user: User) -> User:
    row = await conn.fetchrow(
        f"""
        INSERT INTO {str(user)}(first_name, last_name, phone_number, birthday)
        VALUES($1, $2, $3, $4)
        RETURNING *
        """,
        user.first_name,
        user.last_name,
        user.phone_number,
        user.birthday,
    )
    if row:
        return User(**row)
    else:
        raise UserWarning(
            f"{str(user).capitalize()} could not be inserted into the db."
        )


async def update_user(conn: Connection, user: User) -> User:

    row = await conn.fetchrow(
        f"""
        UPDATE {str(user)}
        SET first_name = $1, last_name = $2, phone_number = $3, birthday = $4
        RETURNING *
        """,
        user.first_name,
        user.last_name,
        user.phone_number,
        user.birthday,
    )
    if row:
        return User(**row)
    else:
        raise UserWarning(
            f"{str(user).capitalize()} with id {user.id} could not be updated."
        )


async def delete_user(conn: Connection, user: User) -> User:
    row = await conn.fetchrow(
        f"""
        DELETE FROM {str(user)}
        WHERE id = $1
        RETURNING *
        """,
        user.id,
    )
    if row:
        return User(**row)
    else:
        raise UserWarning(
            f"{str(user).capitalize()} with id {user.id} could not be deleted from the db."
        )