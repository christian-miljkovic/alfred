from asyncpg import Connection
from alfred.models import Client, ClientInDB
from alfred.core.utils import validate_phone_number
from typing import Union
from uuid import UUID
import logging


async def create_client(conn: Connection, client: Client) -> ClientInDB:
    row = await conn.fetchrow(
        """
        INSERT INTO client (first_name, last_name, phone_number, birthday)
        VALUES($1, $2, $3, $4)
        RETURNING *
        """,
        client.first_name,
        client.last_name,
        client.phone_number,
        client.birthday,
    )
    if row:
        return ClientInDB(**row)
    else:
        raise UserWarning(f"{str(client).capitalize()} could not be inserted into the db.")


async def update_client(conn: Connection, client: Client) -> ClientInDB:

    row = await conn.fetchrow(
        """
        UPDATE client
        SET first_name = $1, last_name = $2, phone_number = $3, birthday = $4
        RETURNING *
        """,
        client.first_name,
        client.last_name,
        client.phone_number,
        client.birthday,
    )
    if row:
        return ClientInDB(**row)
    else:
        raise UserWarning(f"{str(client).capitalize()} with id {client.id} could not be updated.")


async def delete_client(conn: Connection, client_id: UUID) -> ClientInDB:
    row = await conn.fetchrow(
        """
        DELETE FROM client
        WHERE id = $1
        RETURNING *
        """,
        client_id,
    )
    if row:
        return ClientInDB(**row)
    else:
        raise UserWarning(f"CLIENT with id {client_id} could not be deleted from the db.")


async def find_client_by_phone(conn: Connection, phone_number: str) -> Union[ClientInDB, None]:
    row = await conn.fetchrow(
        """
        SELECT * FROM client
        WHERE phone_number = $1
        """,
        phone_number,
    )
    if row:
        return ClientInDB(**row)
    else:
        if not validate_phone_number:
            raise UserWarning(f"Tried searching with invalid phone number {phone_number}.")

        return None


async def find_client_by_id(conn: Connection, client_id: str) -> Union[ClientInDB, None]:
    row = await conn.fetchrow(
        """
        SELECT * FROM client
        WHERE id = $1
        """,
        client_id,
    )
    if row:
        return ClientInDB(**row)
    else:
        if not validate_phone_number:
            raise UserWarning(f"Could not find client with id: {client_id}.")
        logging.warning(f"Could not find client with id: {client_id}.")
        return None
