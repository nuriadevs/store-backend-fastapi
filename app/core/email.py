import os
from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from fastapi.background import BackgroundTasks
from app.core.settings import get_settings


settings = get_settings()

conf = ConnectionConfig(

    MAIL_SERVER=os.environ.get("MAIL_SERVER", "mailpit"),  
    MAIL_PORT=os.environ.get("MAIL_PORT", 1025), 
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME", ""), 
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD", ""),  
    MAIL_FROM=os.environ.get("MAIL_FROM", 'noreply@test.com'),
    MAIL_FROM_NAME=os.environ.get("MAIL_FROM_NAME", settings.APP_NAME),
    MAIL_STARTTLS=os.environ.get("MAIL_STARTTLS", False),  
    MAIL_SSL_TLS=os.environ.get("MAIL_SSL_TLS", False),  
    MAIL_DEBUG=True,
    TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates",
    USE_CREDENTIALS=os.environ.get("USE_CREDENTIALS", False),  
)

fm = FastMail(conf)


async def send_email(recipients: list, subject: str, context: dict, template_name: str,
                     background_tasks: BackgroundTasks):
    print("Comenzando a enviar el correo a %s con el asunto %s", recipients, subject)

    try:
        # Crea el mensaje
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            template_body=context,
            subtype="html"  # Puedes ajustar el tipo si no es HTML
        )
        print("Mensaje creado correctamente, enviando ahora...")

        # Enviar el correo en segundo plano
        background_tasks.add_task(fm.send_message, message, template_name=template_name)
        print("Correo enviado exitosamente a %s", recipients)
    except Exception as e:
        print("Error al enviar el correo: %s", str(e))
