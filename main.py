from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette.middleware.sessions import SessionMiddleware

from pydantic import BaseModel

from langchain_core.messages import HumanMessage

from graph import graph
from employee_db import authenticate

# =====================================================
# FastAPI App
# =====================================================

app = FastAPI(
    title="Time-Off Management Agent",
    version="1.0"
)

# =====================================================
# Session Middleware
# =====================================================

app.add_middleware(
    SessionMiddleware,
    secret_key="your_secret_key_here"   # later move this to .env
)

# =====================================================
# Static Files
# =====================================================

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# =====================================================
# Request Models
# =====================================================

class LoginRequest(BaseModel):
    employee_id: str
    password: str


class ChatRequest(BaseModel):
    message: str


# =====================================================
# Login Page
# =====================================================

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request
        }
    )


# =====================================================
# Login API
# =====================================================

@app.post("/login")
async def login(req: LoginRequest, request: Request):

    employee = authenticate(
        req.employee_id,
        req.password
    )

    if employee is None:

        return JSONResponse(
            {
                "success": False,
                "message": "Invalid Employee ID or Password"
            },
            status_code=401
        )

    request.session["employee"] = employee

    return {
        "success": True
    }


# =====================================================
# Chat UI
# =====================================================

@app.get("/chat-ui", response_class=HTMLResponse)
async def chat_ui(request: Request):

    employee = request.session.get("employee")

    if employee is None:
        return RedirectResponse("/")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "employee": employee
        }
    )


# =====================================================
# Chat Endpoint
# =====================================================

@app.post("/chat")
async def chat(req: ChatRequest, request: Request):

    employee = request.session.get("employee")

    if employee is None:

        return JSONResponse(
            {
                "response": "Please login first."
            },
            status_code=401
        )

    state = {

        "messages": [
            HumanMessage(content=req.message)
        ],

        "employee_id": employee["employee_id"],

        "employee": {}

    }

    result = graph.invoke(state)

    last_message = result["messages"][-1]

    return {
        "response": last_message.content
    }


# =====================================================
# Logout
# =====================================================

@app.get("/logout")
async def logout(request: Request):

    request.session.clear()

    return RedirectResponse("/")