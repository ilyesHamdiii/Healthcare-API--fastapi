from fastapi import FastAPI
from .api.routes import auth,user,article,doctors

app=FastAPI()
@app.get("/")
def route():
    return {"message":"hello worddd"}
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(article.router)
app.include_router(doctors.router)