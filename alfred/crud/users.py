from asyncpg import Connection
from alred.models import User


async def create_user(conn: Connection, user: User) -> User:

    row = await conn.fetchrow(
        f"""
        INSERT INTO {str(user)}(name, price, quantity, image_url, image_width, image_height)
        VALUES($1, $2, $3, $4, $5, $6)
        RETURNING *
        """,
        user.name,
        user.price,
        user.quantity,
        user.image_url,
        user.image_width,
        user.image_height,
    )
    if row:
        return User(**row)
    else:
        raise UserWarning(
            f"{str(user).capitalize()} could not be inserted into the db."
        )