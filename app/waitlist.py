from sqlalchemy.ext.asyncio import AsyncSession
from app.models import waitlistEntryCreate, WaitlistEntry
from sqlalchemy import select
from fastapi import HTTPException, status

async def add_to_waitlist(
        payload: waitlistEntryCreate,
        db: AsyncSession
):
    existing_email = await db.execute(
        select(WaitlistEntry).where(WaitlistEntry.email == payload.email)
    )
    result = existing_email.scalar_one_or_none()
    if result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists in the waitlist"
        )
    new_entry = WaitlistEntry(email=payload.email)

    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)

    message = f"Email {new_entry.email} added to the waitlist successfully!"
    
    return message