import os

from fastapi import APIRouter, Request
from fastapi_sso.sso.google import GoogleSSO
from fastapi.templating import Jinja2Templates

from . import schemas, services


GOOGLE_CLIENT_ID = "20078867313-0al87fvq1vtnl0uvv9rv771h4a4jju84.apps.googleusercontent.com"
GOOGLE_SECRET = "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"
GOOGLE_REDIRECT = "http://127.0.0.1:8000/google/redirect"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = '1'

auth_router = APIRouter(tags=["auth"])
templates = Jinja2Templates(directory="templates")

google_sso = GoogleSSO(GOOGLE_CLIENT_ID, GOOGLE_SECRET, GOOGLE_REDIRECT, allow_insecure_http=True)


@auth_router.get("/")
async def google_login():
    """Generate login url and redirect"""

    return await google_sso.get_login_redirect()


@auth_router.get("/google/redirect", response_model=schemas.TokenBase)
async def google_redirect(request: Request):
    """Process login response from Google and return user info"""

    user = await google_sso.verify_and_process(request)
    token = await services.google_auth(user.display_name, user.email)
    return token
