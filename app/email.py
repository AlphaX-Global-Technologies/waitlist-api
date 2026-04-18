import resend
from fastapi import HTTPException
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import os
import base64
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates" / "emails"
IMAGES_DIR = TEMPLATE_DIR / "images"

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

class EmailService:
    @staticmethod
    def _embed_images(html_content: str) -> str:
        """Convert relative image paths to base64 data URIs"""
        import re

        def replace_image_src(match):
            img_tag = match.group(0)
            src_match = re.search(r'src="([^"]*)"', img_tag)
            if not src_match:
                return img_tag

            src_path = src_match.group(1)

            # Only process relative paths starting with "images/"
            if not src_path.startswith('images/'):
                return img_tag

            # Get the full path to the image
            image_path = IMAGES_DIR / src_path.replace('images/', '')

            try:
                # Read and encode the image
                with open(image_path, 'rb') as f:
                    image_data = f.read()

                # Determine MIME type
                if src_path.endswith('.png'):
                    mime_type = 'image/png'
                elif src_path.endswith('.jpg') or src_path.endswith('.jpeg'):
                    mime_type = 'image/jpeg'
                elif src_path.endswith('.gif'):
                    mime_type = 'image/gif'
                else:
                    mime_type = 'image/png'  # fallback

                # Create data URI
                encoded = base64.b64encode(image_data).decode('utf-8')
                data_uri = f'data:{mime_type};base64,{encoded}'

                # Replace the src attribute
                return img_tag.replace(src_match.group(0), f'src="{data_uri}"')

            except (FileNotFoundError, IOError):
                # If image can't be read, leave the original path
                return img_tag

        # Replace all img tags with src attributes
        return re.sub(r'<img[^>]*>', replace_image_src, html_content)

    @staticmethod
    async def send_email(to: str, subject: str, template_name: str, context: dict):
        try:
            template = env.get_template(template_name)
            html_content = template.render(**context)

            # Embed images as base64 data URIs
            html_content = EmailService._embed_images(html_content)

            params = {
                "from": os.getenv("EMAIL_FROM"),
                "to": to,
                "subject": subject,
                "html": html_content,
            }

            resend.Emails.send(params)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Email sending failed: {str(e)}")
