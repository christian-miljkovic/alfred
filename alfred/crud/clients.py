from asyncpg import Connection
from alfred.models import Client, ClientInDB
from alfred.core.utils import validate_phone_number
from typing import Union


async def create_client(conn: Connection, client: Client) -> ClientInDB:
    row = await conn.fetchrow(
        f"""
        INSERT INTO {str(client)} (first_name, last_name, phone_number, birthday)
        VALUES($1, $2, $3, $4)
        RETURNING *
        """,
        client.first_name,
        client.last_name,
        client.phone_number,
        client.birthday,
    )
    if row:
        return Client(**row)
    else:
        raise UserWarning(
            f"{str(client).capitalize()} could not be inserted into the db."
        )


async def update_client(conn: Connection, client: Client) -> ClientInDB:

    row = await conn.fetchrow(
        f"""
        UPDATE {str(client)}
        SET first_name = $1, last_name = $2, phone_number = $3, birthday = $4
        RETURNING *
        """,
        client.first_name,
        client.last_name,
        client.phone_number,
        client.birthday,
    )
    if row:
        return Client(**row)
    else:
        raise UserWarning(
            f"{str(client).capitalize()} with id {client.id} could not be updated."
        )


async def delete_client(conn: Connection, client: Client) -> ClientInDB:
    row = await conn.fetchrow(
        f"""
        DELETE FROM {str(client)}
        WHERE id = $1
        RETURNING *
        """,
        client.id,
    )
    if row:
        return Client(**row)
    else:
        raise UserWarning(
            f"{str(client).capitalize()} with id {client.id} could not be deleted from the db."
        )


async def find_client_by_phone(
    conn: Connection, phone_number: str
) -> Union[ClientInDB, None]:
    row = await conn.fetchrow(
        """
        SELECT * FROM client
        WHERE phone_number = $1
        """,
        phone_number,
    )
    if row:
        return Client(**row)
    else:
        if not validate_phone_number:
            raise UserWarning(
                f"Tried searching with invalid phone number {phone_number}."
            )

        return None
