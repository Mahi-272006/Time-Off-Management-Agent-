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


# --------------------------------------------------
# Per-employee conversation state
# --------------------------------------------------
# Instead of one shared dict for every visitor, each employee_id gets
# its own separate state so concurrent users don't interfere with
# each other's conversations or leave requests.

conversation_states: dict[str, dict] = {}


def get_conversation_state(employee: dict) -> dict:
    employee_id = employee["employee_id"]

    if employee_id not in conversation_states:
        conversation_states[employee_id] = {
            "messages": [],
            "employee_id": employee_id,
            "employee": employee,
            "tool_results": {},
            "retrieved_docs": [],
            "final_response": "",
            "needs_clarification": False,
            "clarification_question": "",
            "summary": "",
            "intent": "",
            "can_proceed": False,
        }

    return conversation_states[employee_id]


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

    # Look up (or create) this employee's own conversation state
    state = get_conversation_state(employee)

    # Add the new user message to their own message history
    state["messages"].append(
        HumanMessage(content=req.message)
    )
    state["role"] = employee.get("role", "employee")

    print("GRAPH STATE ROLE:", state["role"])

    result = graph.invoke(
        state,
        config={
            "configurable": {
                "thread_id": employee["employee_id"]  #tells langgraph which state the convo belong
            }
        }
    )

    # Persist the updated state back into this employee's slot
    conversation_states[employee["employee_id"]] = result

    print("\n===== STORED MESSAGES =====")
    for msg in result["messages"]:
        print(type(msg).__name__, ":", msg.content)
    print("===========================\n")

    answer = result["messages"][-1].content

    # Gemini (and sometimes Anthropic) can return content as a list of
    # structured blocks instead of a plain string. Flatten it here so the
    # frontend always receives a plain string.
    if isinstance(answer, str):
        final_response = answer

    elif isinstance(answer, list):
        text_parts = []
        for block in answer:
            if isinstance(block, dict) and block.get("type") == "text":
                text_parts.append(block.get("text", ""))
        final_response = "\n".join(text_parts).strip()

    else:
        final_response = str(answer)

    print(f"DEBUG main.py: type(answer)={type(answer).__name__}, final_response={final_response!r}")

    return {
        "response": final_response
    }


# Logout
@app.get("/logout")
async def logout(request: Request):

    request.session.clear()

    return RedirectResponse("/")