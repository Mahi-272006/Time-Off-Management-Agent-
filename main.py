from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from langchain_core.messages import HumanMessage

from graph import graph

# -----------------------------------------------------
# FastAPI App
# -----------------------------------------------------

app = FastAPI(
    title="Time-Off Management Agent",
    version="1.0"
)

# -----------------------------------------------------
# Static Files & Templates
# -----------------------------------------------------

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# -----------------------------------------------------
# Request Schema
# -----------------------------------------------------

class ChatRequest(BaseModel):
    employee_id: str
    message: str

# -----------------------------------------------------
# Home Page
# -----------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

# -----------------------------------------------------
# Chat Endpoint
# -----------------------------------------------------

@app.post("/chat")
async def chat(request: ChatRequest):

    state = {
        "messages": [
            HumanMessage(content=request.message)
        ],
        "employee_id": request.employee_id,
        "employee": {}
    }

    result = graph.invoke(state)

    last_message = result["messages"][-1]

    return {
        "response": last_message.content
    }