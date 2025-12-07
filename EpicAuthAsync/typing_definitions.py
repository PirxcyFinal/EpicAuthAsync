from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional, TypedDict

GRANT_TYPES: dict[str, list[str]] = {
    "authorization_code": [
        "code",
        "code_verifier",
    ],
    "client_credentials": [],
    "continuation_token": [
        "continuation_token",
    ],
    "device_auth": [
        "account_id",
        "device_id",
        "secret",
    ],
    "device_code": [
        "device_code",
    ],
    "exchange_code": [
        "exchange_code",
        "code_verifier",
    ],
    "external_auth": [
        "external_auth_type",
        "external_auth_token",
    ],
    "otp": [
        "otp",
        "challenge",
    ],
    "password": [
        "username",
        "password",
    ],
    "refresh_token": [
        "refresh_token",
    ],
    "token_to_token": [
        "access_token",
    ],
}


class TokenResponse(BaseModel):
    access_token: str
    expires_in: int
    expires_at: datetime
    token_type: str
    client_id: str
    internal_client: bool
    client_service: Optional[str] = None
    product_id: Optional[str] = None
    application_id: Optional[str] = None
    refresh_token: Optional[str] = None
    refresh_expires: Optional[int] = None
    refresh_expires_at: Optional[datetime] = None
    account_id: Optional[str] = None
    displayName: Optional[str] = None
    app: Optional[str] = None
    in_app_id: Optional[str] = None


class ExchangeCodeResponse(BaseModel):
    expiresInSeconds: int
    code: str
    creatingClientId: str
    consumingClientId: Optional[str] = None


class DeviceCodeCreateResponse(BaseModel):
    user_code: str
    device_code: str
    verification_uri: str
    verification_uri_complete: str
    prompt: str
    expires_in: int
    interval: int
    client_id: str


class ContinuationTokenInfo(BaseModel):
    tokenId: str
    shortTokenId: str
    clientId: str
    accountId: str
    scopes: List[str]
    correctiveAction: Optional[str] = None
    ageGateRequired: bool
    acr: str


class Perm(TypedDict):
    resource: str | None
    action: int | None


class TokenVerifyResponse(BaseModel):
    token: str
    session_id: str
    token_type: str
    client_id: str
    internal_client: bool
    client_service: Optional[str] = None
    account_id: Optional[str] = None
    expires_in: int
    expires_at: datetime
    auth_method: str
    display_name: Optional[str] = None
    app: Optional[str] = None
    in_app_id: Optional[str] = None
    perms: Optional[List[Perm]] = None


class ClientPerm(TypedDict, total=False):
    client: list[Perm] | None
    account: list[Perm] | None


class Client(BaseModel):
    id: str
    name: str
    secret: str | None
    note: str | None
    logo: str | None
    enabled: bool
    eos: bool
    epicId: bool
    features: list[str] | None
    service: str | None
    redirectUrl: str | None
    allowedScopes: list[str]
    requiredScopes: list[str]
    eulas: list[str]
    grantTypes: list[str] | None
    perms: ClientPerm | None = None
    hasTokenExchangeMethod: bool
