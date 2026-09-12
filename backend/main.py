import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BACKEND_DIR))

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

#to validate the structure of incoming API requests
from pydantic import BaseModel

from langchain_core.messages import HumanMessage

from backend.auth import authenticate
from backend.graph import graph

app = FastAPI(title="Time-Off Assistant")


# Session
app.add_middleware(
    SessionMiddleware,
    secret_key="timeoff_secret_key",  
)


# Static & Templates
app.mount(
    "/static",
    StaticFiles(directory=BACKEND_DIR / "static"),
    name="static",
)

templates = Jinja2Templates(
    directory=BACKEND_DIR / "templates"
)

# Models
class LoginRequest(BaseModel):
    employee_id: str
    password: str

class ChatRequest(BaseModel):
    message: str


# Login Page
@app.get("/")
async def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request
        }
    )


# Login API
@app.post("/login")
async def login(req: LoginRequest, request: Request):

    #calls auth.py
    employee = authenticate(
        req.employee_id,
        req.password
    )

    if employee is None:
        return {
            "success": False,
            "message": "Invalid Employee ID or Password"
        }

    #stores authenticated employee in the session
    request.session["employee"] = employee

    return {
        "success": True
    }


# Chat Page
@app.get("/chat")
async def chat_page(request: Request):

    #checks whether the user is logged in
    employee = request.session.get("employee")

    if employee is None:
        return RedirectResponse("/")

    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "employee": employee
        }
    )


# Chat API
@app.post("/ask")
async def ask(req: ChatRequest, request: Request):

    employee = request.session.get("employee")

    if employee is None:
        return {
            "response": "Please login first."
        }

    state = {

        "messages": [
            HumanMessage(content=req.message)
        ],
        "employee_id": employee["employee_id"],
        "role": employee.get("role", "employee"),
        "employee": employee

    }

    print("GRAPH STATE ROLE:", state["role"])

    result = graph.invoke(
    state,
    config={
        "configurable": {
            "thread_id": employee["employee_id"]  #tells langgraph which state the convo belong
        }
    }
    )
    print("\n===== STORED MESSAGES =====")
    for msg in result["messages"]:
        print(type(msg).__name__, ":", msg.content)
    print("===========================\n")

    answer = result["messages"][-1].content

    return {
        "response": answer
    }


# Logout
@app.get("/logout")
async def logout(request: Request):

    request.session.clear()

    return RedirectResponse("/")