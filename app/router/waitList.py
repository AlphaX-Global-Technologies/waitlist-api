from sqlalchemy.ext.asyncio import AsyncSession
from app.models import waitlistEntryCreate, waitlistResponse
from fastapi import Depends, APIRouter
from app.session import get_session
from app.waitlist import add_to_waitlist
from app.email import EmailService


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

    await EmailService.send_email(
        to=payload.email,
        subject="Welcome to the AlphaX!",
        template_name="waitlist.html",
        context={"email": payload.email}
    )

    return {
        "message": message
    }