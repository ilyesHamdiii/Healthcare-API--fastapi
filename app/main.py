from fastapi import FastAPI
from .api.routes import auth,user,article,appointment,notifications
from fastapi.responses import RedirectResponse

app=FastAPI()
@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(article.router)
app.include_router(appointment.router)
app.include_router(notifications.router)