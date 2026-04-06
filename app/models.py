from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import EmailStr


class WaitlistEntry(SQLModel, table=True):
    """Model representing an entry in the waitlist"""

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    email: EmailStr = Field(..., unique=True, index=True)
    joined_at: datetime = Field(default_factory=datetime.utcnow)


class waitlistEntryCreate(SQLModel):
    """Model for creating a new waitlist entry"""

    email: EmailStr


class waitlistResponse(SQLModel):
    """Model for returning waitlist entry data"""

    message: str

    # id: UUID
    # email: EmailStr
    # joined_at: datetime