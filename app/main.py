
import asyncio
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from .epic import EpicClient

app = FastAPI(title="Fortnite Party Dashboard v3")

app.add_middleware(SessionMiddleware, secret_key="supersecretfortnite456")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/login", response_class=HTMLResponse)
def login_page():
    return FileResponse("static/login.html")

@app.post("/login")
async def login(request: Request, accountId: str = Form(...), token: str = Form(...)):
    client = EpicClient(accountId, token)
    try:
        await client.get_party_for_user()
    except Exception:
        return HTMLResponse("Invalid token/accountId", status_code=400)
    request.session["accountId"] = accountId
    request.session["token"] = token
    return RedirectResponse("/", status_code=302)

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    if "token" not in request.session or "accountId" not in request.session:
        return RedirectResponse("/login")
    return FileResponse("static/index.html")

@app.get("/api/party")
async def get_party(request: Request):
    client = EpicClient(request.session.get("accountId"), request.session.get("token"))
    party = await client.get_party_for_user()
    for m in party.get("members", []):
        pres = await client.get_presence(m["accountId"])
        m["presence"] = pres
    return party

@app.post("/api/presence/set")
async def set_presence(request: Request, status: str = Form(...), statusMessage: str = Form(None), isPlaying: bool = Form(False), platform: str = Form(None)):
    client = EpicClient(request.session.get("accountId"), request.session.get("token"))
    res = await client.set_presence(status, statusMessage, isPlaying, platform)
    return res
