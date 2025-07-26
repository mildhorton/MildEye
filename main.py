from fasthtml.common import *
from database import create_db_and_tables, create_user, get_user_by_email, verify_password
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles # <-- Import StaticFiles

# --- Application Setup ---
app, rt = fast_app()
app.add_middleware(SessionMiddleware, secret_key="a_very_secret_key_change_me")

# Mount the 'static' directory to serve files from it
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# --- Page Layout and Components ---
def page_layout(request, main_content, title="MildEye"):
    user = request.session.get('user')
    nav = Ul(
        Li(A("Home", href="/")),
        Li(A("Login", href="/login")) if not user else Li(A("Logout", href="/logout")),
        cls='nav'
    )
    return Html(
        Head(
            Title(title),
            Link(rel="stylesheet", href="https.cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"),
            Link(rel="stylesheet", href="/static/custom.css") # <-- Link our new CSS file
        ),
        Body(Div(nav, Main(main_content, cls='container')))
    )

# ... (The rest of your routes: '/', '/login', '/register', '/logout' remain exactly the same) ...
# ...

# --- Run the app ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)