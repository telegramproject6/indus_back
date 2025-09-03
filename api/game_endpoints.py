from fastapi import APIRouter

from schemas.schemas_in import GamerSchemaIn, UpdateGamerSchemaIn
from schemas.schemas_out import GamerSchemaOut, UpdateGamerSchemaOut
from database.database_queries import GamerService


router = APIRouter(
    tags=['Game endpoints']
)


# ─────────────────────── Game endpoints ─────────────────────────
@router.post('/gamer')
async def get_or_add_gamer(gamer_id: GamerSchemaIn):

    result = GamerService.get_or_add_gamer(gamer_id)

    return result

# ----------------------------------------------------------------------------------------------------------------------

@router.post('/update_gamer')
async def update_gamer(gamer_id: UpdateGamerSchemaIn):

    result = GamerService.update_gamer(gamer_id)

    return result