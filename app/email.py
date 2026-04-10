import resend
from fastapi import HTTPException
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates" / "emails"

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

class EmailService:
    @staticmethod
    async def send_email(to: str, subject: str, template_name: str, context: dict):
        try:
            template = env.get_template(template_name)
            html_content = template.render(**context)

            params = {
                "from": os.getenv("EMAIL_FROM"),
                "to": to,
                "subject": subject,
                "html": html_content,
            }

            resend.Emails.send(params)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Email sending failed: {str(e)}")
