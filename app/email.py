import resend
from fastapi import HTTPException
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from dotenv import load_dotenv
import os

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

            await resend.Emails.send_async(params)
        except Exception as e:
            print(f"Error sending email: {e}")