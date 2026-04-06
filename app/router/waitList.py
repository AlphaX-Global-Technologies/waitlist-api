from sqlalchemy.ext.asyncio import AsyncSession
from app.models import waitlistEntryCreate, waitlistResponse
from fastapi import Depends, APIRouter
from app.session import get_session
from app.waitlist import add_to_waitlist


router = APIRouter(
    prefix="/waitlist",
    tags=["waitlist"]
)

@router.post("/waitlist", response_model=waitlistResponse)
async def create_waitlist_entry(
    payload: waitlistEntryCreate,
    db: AsyncSession = Depends(get_session)
):
    """Endpoint to add a new email to the waitlist"""

    message = await add_to_waitlist(payload, db)
    return {
        "message": message
    }