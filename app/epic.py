
import time
from typing import Optional, Dict, Any
import httpx

PARTY_USER_URL = "https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/user/{account_id}"
PRESENCE_GET_URL = "https://friends-public-service-prod.ol.epicgames.com/friends/api/public/friends/{account_id}/presence"
PRESENCE_SET_URL = "https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account_id}/presence"

class EpicClient:
    def __init__(self, account_id: Optional[str]=None, access_token: Optional[str]=None):
        self.account_id = account_id
        self.access_token = access_token

    async def _headers(self):
        return {"Authorization": f"bearer {self.access_token}", "Content-Type":"application/json"}

    async def get_party_for_user(self):
        url = PARTY_USER_URL.format(account_id=self.account_id)
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.get(url, headers=await self._headers())
            r.raise_for_status()
            party = r.json()
        # Add cosmetic placeholders if missing
        for m in party.get("members", []):
            if "skin" not in m: m["skin"]="DefaultSkin"
            if "backbling" not in m: m["backbling"]="None"
            if "pickaxe" not in m: m["pickaxe"]="DefaultPickaxe"
            if "platform" not in m: m["platform"]="UNKNOWN"
        return party

    async def get_presence(self, account_id: str):
        url = PRESENCE_GET_URL.format(account_id=account_id)
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.get(url, headers=await self._headers())
            r.raise_for_status()
            pres = r.json()
        # Ensure keys exist
        pres.setdefault("status", "Lobby")
        pres.setdefault("message", "")
        pres.setdefault("isPlaying", True)
        pres.setdefault("platform", "UNKNOWN")
        pres.setdefault("updatedAt", int(time.time()))
        return pres

    async def set_presence(self, status: str, status_message: Optional[str]=None, is_playing: Optional[bool]=None, platform: Optional[str]=None):
        payload = {"status": status}
        if status_message: payload["statusMessage"] = status_message
        if is_playing is not None: payload["isPlaying"] = is_playing
        if platform: payload["platform"] = platform
        url = PRESENCE_SET_URL.format(account_id=self.account_id)
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.patch(url, headers=await self._headers(), json=payload)
            r.raise_for_status()
            return r.json()
