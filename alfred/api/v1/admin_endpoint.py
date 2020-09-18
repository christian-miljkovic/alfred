from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from jarvis.db.database import DataBase, get_database
from jarvis.core.models import Item
from jarvis.models import Beer, Liquor, Wine
import jarvis.crud as crud

router = APIRouter()


@router.post("/add/{drink_type}")
async def add_item_to_db(
    drink_type: str, item: Item, db: DataBase = Depends(get_database)
):
    type_mapping = {"beer": Beer, "liquor": Liquor, "wine": Wine}
    async with db.pool.acquire() as conn:
        try:
            type_converted_item = type_mapping.get(drink_type)(**item.dict())
            added_item = await crud.create_item(conn, type_converted_item)
            return added_item
        except UserWarning as warning:
            return JSONResponse(
                status_code=status.HTTP_202_ACCEPTED, content=str(warning)
            )


@router.post("/update/{drink_type}")
async def update_item_to_db(
    drink_type: str, item: Item, db: DataBase = Depends(get_database)
):
    type_mapping = {"beer": Beer, "liquor": Liquor, "wine": Wine}
    async with db.pool.acquire() as conn:
        try:
            type_converted_item = type_mapping.get(drink_type)(**item.dict())
            updated_item = await crud.update_item(conn, type_converted_item)
            return updated_item
        except UserWarning as warning:
            return JSONResponse(
                status_code=status.HTTP_202_ACCEPTED, content=str(warning)
            )


@router.post("/delete/{drink_type}")
async def delete_item_to_db(
    drink_type: str, item: Item, db: DataBase = Depends(get_database)
):
    type_mapping = {"beer": Beer, "liquor": Liquor, "wine": Wine}
    async with db.pool.acquire() as conn:
        try:
            type_converted_item = type_mapping.get(drink_type)(**item.dict())
            deleted_item = await crud.delete_item(conn, type_converted_item)
            return deleted_item
        except UserWarning as warning:
            return JSONResponse(
                status_code=status.HTTP_202_ACCEPTED, content=str(warning)
            )
