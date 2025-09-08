from fastapi import FastAPI
from .api.routes import auth,user,article,appointment,notifications

app=FastAPI()
@app.get("/")
def route():
    return {"message":"hello worddd"}
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(article.router)
app.include_router(appointment.router)
app.include_router(notifications.router)