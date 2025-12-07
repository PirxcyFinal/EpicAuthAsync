"""
- Originally made this for my own personal use, but decided to share it with the community because why not :)

Credits:
EpicAuthAsync - An asynchronous Epic Games authentication library
Jaren - API endpoints for fetching clients (https://egs.jaren.wtf/)
LeleDerGrasshalmi - Endpoints and what they do (https://github.com/LeleDerGrasshalmi/FortniteEndpointsDocumentation)
"""

import asyncio
import aiohttp

from EpicAuthAsync.typing_definitions import Client
from EpicAuthAsync.typing_definitions import TokenResponse
from EpicAuthAsync.typing_definitions import TokenVerifyResponse
from EpicAuthAsync.typing_definitions import ExchangeCodeResponse
from EpicAuthAsync.typing_definitions import ContinuationTokenInfo
from EpicAuthAsync.typing_definitions import DeviceCodeCreateResponse


class Authentication:
    def __init__(self):
        self.clients = []
        asyncio.run(self._fetch_all_clients())

    async def _fetch_all_clients(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://egs.jaren.wtf/api/clients") as resp:
                data = await resp.json()
                clients = data["clients"]
                self.clients = [Client(**client) for client in clients]

    async def verify_token(
        self, access_token: str, include_perms: bool = False
    ) -> TokenVerifyResponse:
        """
        GET /account/api/oauth/verify
        Verifies the current OAuth session.

        Parameters:
        - access_token: Bearer token of the session to verify
        - include_perms: Whether to include 'perms' field in the response

        Returns:
        - TokenVerifyResponse: Parsed response including session info and optional permissions
        """
        url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/verify"

        headers = {"Authorization": f"Bearer {access_token}"}

        params: dict[str, str] = {}
        if include_perms:
            params["includePerms"] = "true"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                data = await resp.json()
                return TokenVerifyResponse(**data)

    async def request_oauth_token(
        self,
        client_id: str,
        client_secret: str,
        grant_type: str,
        body_params: dict[str, str],
        device_id: str | None = None,
    ) -> TokenResponse:
        """
        POST /account/api/oauth/token
        Requires Basic Authentication using Client Id and Client Secret.

        Parameters:
        - grant_type: see GrantTypes
        - body_params: dictionary containing required fields for the grant type
        - device_id: optional, sets X-Epic-Device-ID header
        """
        url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        if device_id:
            headers["X-Epic-Device-ID"] = device_id

        auth = aiohttp.BasicAuth(login=client_id, password=client_secret)

        async with aiohttp.ClientSession(auth=auth) as session:
            async with session.post(
                url, data={**body_params, "grant_type": grant_type}, headers=headers
            ) as resp:
                data = await resp.json()
                return TokenResponse(**data)

    async def kill_sessions(self, access_token: str, kill_type: str):
        """
        DELETE /account/api/oauth/sessions/kill
        Kills multiple sessions depending on killType.

        kill_type must be one of:
        - OTHERS_ACCOUNT_CLIENT_SERVICE
        - OTHERS_ACCOUNT_CLIENT
        - OTHERS_SAME_SOURCE_ID
        - OTHERS
        - ALL
        - ALL_ACCOUNT_CLIENT
        """
        url = (
            "https://account-public-service-prod.ol.epicgames.com/"
            "account/api/oauth/sessions/kill"
        )

        params = {"killType": kill_type}

        headers = {"Authorization": f"Bearer {access_token}"}

        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=headers, params=params) as resp:
                return resp.status == 204

    async def kill_session(
        self,
        session_token: str,
        access_token: str,
        kill_all_with_same_source: bool | None = None,
    ):
        """
        DELETE /account/api/oauth/sessions/kill/:session
        Kills a session by access token.
        """
        base_url = (
            "https://account-public-service-prod.ol.epicgames.com/"
            f"account/api/oauth/sessions/kill/{session_token}"
        )

        params: dict[str, str] = {}
        if kill_all_with_same_source is not None:
            params["killAllWithSameSource"] = str(kill_all_with_same_source).lower()

        headers = {"Authorization": f"Bearer {access_token}"}

        async with aiohttp.ClientSession() as session:
            async with session.delete(base_url, headers=headers, params=params) as resp:
                # Success is HTTP 204
                return resp.status == 204

    async def create_exchange_code(
        self,
        access_token: str,
        consuming_client_id: str | None = None,
        code_challenge: str | None = None,
        code_challenge_method: str | None = None,
    ):
        """
        GET /account/api/oauth/exchange
        Requires scope: account:oauth:exchangeTokenCode CREATE
        """
        base_url = (
            "https://account-public-service-prod.ol.epicgames.com/"
            "account/api/oauth/exchange"
        )

        params: dict[str, str] = {}

        if consuming_client_id:
            params["consumingClientId"] = consuming_client_id
        if code_challenge:
            params["codeChallenge"] = code_challenge
        if code_challenge_method:
            params["codeChallengeMethod"] = code_challenge_method

        headers = {"Authorization": f"Bearer {access_token}"}

        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, headers=headers, params=params) as resp:
                data = await resp.json()
                return ExchangeCodeResponse(**data)

    async def get_continuation_token_info(
        self, continuation_token: str, access_token: str
    ):
        """
        GET /account/api/oauth/continuationToken/:continuationToken
        Requires Bearer token with scope: account:oauth:continuationToken READ
        """
        url = (
            "https://account-public-service-prod.ol.epicgames.com/"
            f"account/api/oauth/continuationToken/{continuation_token}"
        )

        headers = {"Authorization": f"Bearer {access_token}"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                data = await resp.json()
                return ContinuationTokenInfo(**data)

    async def create_device_code(self, access_token: str):
        """
        POST /account/api/oauth/deviceAuthorization
        Requires client_credentials auth
        """
        url = (
            "https://account-public-service-prod.ol.epicgames.com/"
            "account/api/oauth/deviceAuthorization"
        )

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json={}) as resp:
                data = await resp.json()
                return DeviceCodeCreateResponse(**data)

    async def delete_device_code(self, user_code: str, access_token: str):
        """
        DELETE /account/api/oauth/deviceAuthorization/:userCode
        Returns True if successful (204)
        """
        url = (
            "https://account-public-service-prod.ol.epicgames.com/"
            f"account/api/oauth/deviceAuthorization/{user_code}"
        )

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=headers) as resp:
                if resp.status == 204:
                    return True
                return False
