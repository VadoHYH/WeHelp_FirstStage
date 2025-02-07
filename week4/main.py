from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from pathlib import Path

app=FastAPI()

#設置SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key="your_secrect_key")

#設定Jinja2
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

#設定靜態檔案
app.mount("/static",StaticFiles(directory=str(BASE_DIR / "static")), name="static")

#Home page
@app.get("/")
def home(request : Request):
    return templates.TemplateResponse("index.html",{"request":request})

@app.get("/square/{number}")
def square(request : Request, number : int):
    square_number =number*number
    return templates.TemplateResponse("square.html",{"request":request,"number":number,"squared":square_number})

@app.post("/signin")
def signin(request : Request,username: str = Form(...), password : str = Form(...)):
    if not username or not password:
        return RedirectResponse("/error?message=帳號、或密碼輸入錯誤", status_code=303)
    if username == "test" and password == "test":
        request.session["SIGNED-IN"]=True
        return RedirectResponse("/member",status_code=303)
    else:
        return RedirectResponse("/error?message=帳號、或密碼輸入錯誤", status_code=303)
    
@app.get("/member")
def member(request : Request):
    if not request.session.get("SIGNED-IN"):
        return RedirectResponse("/",status_code=303)
    return templates.TemplateResponse("member.html",{"request":request})

@app.get("/signout")
def signout(request : Request):
    if "SIGNED-IN" in request.session:
        del request.session["SIGNED-IN"]
    return RedirectResponse("/",status_code=303)

@app.get("/error")
def error(request:Request,message:str):
    return templates.TemplateResponse("error.html",{"request":request,"message":message})