from fastapi import FastAPI, Request, Form, Depends, Query
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
from database import get_db

app = FastAPI()

# Session Middleware
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

# Templates 與 Static Files 設定
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

class UpdateNameRequest(BaseModel):
    name:str

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/signup")
def signup(
    request: Request,
    name: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    db=Depends(get_db)
):
    conn, cursor = db

    # 檢查是否有重複的 username
    cursor.execute("SELECT id FROM member WHERE username = %s", (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        return RedirectResponse("/error?message=Repeated username", status_code=303)

    # 新增會員
    cursor.execute("INSERT INTO member (name, username, password) VALUES (%s, %s, %s)", (name, username, password))
    conn.commit()

    return RedirectResponse("/", status_code=303)

@app.post("/signin")
def signin(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db=Depends(get_db)
):
    conn, cursor = db

    # 檢查帳號密碼
    cursor.execute("SELECT id, name FROM member WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    if user:
        request.session["user"] = {
            "id": user["id"],
            "username": username,
            "name": user["name"]
        }
        return RedirectResponse("/member", status_code=303)
    else:
        return RedirectResponse("/error?message=帳號或密碼錯誤", status_code=303)


@app.get("/member")
def member(request: Request, db=Depends(get_db)):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/", status_code=303)

    conn, cursor = db

    # 取得所有留言
    cursor.execute("SELECT message.id, message.content, message.time, member.name, message.member_id FROM message JOIN member ON message.member_id = member.id ORDER BY message.time DESC")
    messages = cursor.fetchall()

    return templates.TemplateResponse("member.html", {
        "request": request,
        "user": user,
        "messages": messages
    })

@app.get("/api/member")
def get_member(
    request : Request,
    username : str = Query(None),
    db=Depends(get_db)
):
    user = request.session.get("user")
    if not user:
        return JSONResponse(content={"data":None})
    conn,cursor =db
    cursor.execute("SELECT id, name, username FROM member WHERE username = %s",(username,))
    member = cursor.fetchone()

    if member:
        return JSONResponse(content={"data":member})
    else:
        return JSONResponse(content={"data":None})
    
@app.patch("/api/member")
def update_member_name(
    request: Request,
    update_data: UpdateNameRequest,
    db=Depends(get_db)
):
    user = request.session.get("user")
    if not user:
        return JSONResponse(content={"error":True})
    conn,cursor =db
    cursor.execute("UPDATE member SET name = %s WHERE id = %s", (update_data.name,user["id"]))
    conn.commit()

    user["name"] = update_data.name
    request.session["user"] = user

    return JSONResponse(content={"ok": True, "new_name": update_data.name})

@app.get("/signout")
def signout(request: Request):
    request.session.clear()  # 清除 session
    return RedirectResponse("/", status_code=303)

@app.post("/createMessage")
def create_message(
    request: Request,
    content: str = Form(...),
    db=Depends(get_db)
):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/", status_code=303)

    conn, cursor = db

    # 新增留言
    cursor.execute("INSERT INTO message (member_id, content) VALUES (%s, %s)", (user["id"], content))
    conn.commit()

    return RedirectResponse("/member", status_code=303)


@app.post("/deleteMessage")
def delete_message(
    request: Request,
    message_id: int = Form(...),
    db=Depends(get_db)
):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/", status_code=303)

    conn, cursor = db

    # 確保留言是自己的
    cursor.execute("SELECT id FROM message WHERE id = %s AND member_id = %s", (message_id, user["id"]))
    message = cursor.fetchone()
    if message:
        cursor.execute("DELETE FROM message WHERE id = %s", (message_id,))
        conn.commit()

    return RedirectResponse("/member", status_code=303)


@app.get("/error")
def error(request: Request, message: str):
    return templates.TemplateResponse("error.html", {"request": request, "message": message})
