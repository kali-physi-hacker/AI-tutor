from __future__ import annotations

import datetime as dt
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.config import settings
from ...core.deps import get_db
from ...core.security import create_token, hash_password, verify_password
from ...db.models import User

router = APIRouter()


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class TokenPair(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/register", response_model=TokenPair)
async def register(data: RegisterRequest, response: Response, db: Annotated[AsyncSession, Depends(get_db)]):
    existing = await User.get_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=str(data.email), password_hash=hash_password(data.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return await _issue_tokens_for_user(user, response)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/login", response_model=TokenPair)
async def login(data: LoginRequest, response: Response, db: Annotated[AsyncSession, Depends(get_db)]):
    user = await User.get_by_email(db, data.email)
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return await _issue_tokens_for_user(user, response)


@router.post("/refresh", response_model=TokenPair)
async def refresh(response: Response, db: Annotated[AsyncSession, Depends(get_db)]):
    # Fast re-issue using refresh cookie is handled by dependency decode in frontend; keep stateless here
    # For simplicity, this endpoint just returns 401; frontend should call with cookie via browser
    raise HTTPException(status_code=501, detail="Use httpOnly cookie flow via browser")


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=False,
        samesite="lax",
        path="/",
    )
    return {"ok": True}


async def _issue_tokens_for_user(user: User, response: Response) -> TokenPair:
    access = create_token(str(user.id), dt.timedelta(minutes=settings.access_token_expire_minutes), "access")
    refresh = create_token(str(user.id), dt.timedelta(days=settings.refresh_token_expire_days), "refresh")
    response.set_cookie(
        key="refresh_token",
        value=refresh,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/",
        max_age=settings.refresh_token_expire_days * 24 * 3600,
    )
    return TokenPair(access_token=access)


# --- OAuth (Google) stubs ---
@router.get("/oauth/google/start")
async def oauth_google_start():
    # Redirect user to Google OAuth consent screen (stub)
    return {"url": "https://accounts.google.com/o/oauth2/v2/auth?client_id=..."}


@router.get("/oauth/google/callback")
async def oauth_google_callback(code: str):
    # Exchange code for tokens and issue app tokens (stub)
    return {"ok": True}
