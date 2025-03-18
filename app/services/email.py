from fastapi import BackgroundTasks
from app.core.settings import get_settings
from app.models.user.user import User
from app.core.email import send_email
from app.utils.email_context import FORGOT_PASSWORD, USER_VERIFY_ACCOUNT


settings = get_settings()




async def send_account_verification_email(user: User, background_tasks: BackgroundTasks):
    from app.core.security import hash_password
    print("Preparando el correo de verificación para el usuario %s", user.email)
    
    try:
        string_context = user.get_context_string(context=USER_VERIFY_ACCOUNT)
        token = hash_password(string_context)
        activate_url = f"{settings.FRONTEND_HOST}/auth/account-verify?token={token}&email={user.email}"

        # Crear datos para la plantilla
        data = {
            'app_name': settings.APP_NAME,
            'name': user.username,
            'activate_url': activate_url
        }

        subject = f"Account Verification - {settings.APP_NAME}"
        print("Datos preparados para el correo de verificación")

        # Llamar al envío del correo
        await send_email(
            recipients=[user.email],
            subject=subject,
            template_name="user/account-verification.html",
            context=data,
            background_tasks=background_tasks
        )
        print("Correo de verificación enviado a %s", user.email)
    
    except Exception as e:
       print("Error al enviar el correo de verificación a %s: %s", user.email, str(e))
    
async def send_account_activation_confirmation_email(user: User, background_tasks: BackgroundTasks):
    data = {
        'app_name': settings.APP_NAME,
        'username': user.username,
        'login_url': f'{settings.FRONTEND_HOST}'
    }
    subject = f"Welcome - {settings.APP_NAME}"
    await send_email(
        recipients=[user.email],
        subject=subject,
        template_name="user/account-verification-confirmation.html",
        context=data,
        background_tasks=background_tasks
    )
    

async def send_password_reset_email(user: User, background_tasks: BackgroundTasks):
    from app.core.security import hash_password
    string_context = user.get_context_string(context=FORGOT_PASSWORD)
    token = hash_password(string_context)
    reset_url = f"{settings.FRONTEND_HOST}/reset-password?token={token}&email={user.email}"
    data = {
        'app_name': settings.APP_NAME,
        "username": user.username,
        'activate_url': reset_url,
    }
    subject = f"Reset Password - {settings.APP_NAME}"
    await send_email(
        recipients=[user.email],
        subject=subject,
        template_name="user/password-reset.html",
        context=data,
        background_tasks=background_tasks
    )