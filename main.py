from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from api.config import APP_CONFIG
from api.routes import admin_router, auth_router, users_router

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8888",
]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(users_router)


@app.get('/')
def index() -> HTMLResponse:
    return HTMLResponse(content="""
<!DOCTYPE html>
<html>
    <head>
        <title>Login Page</title>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    </head>
    <body>
        <h2>Login Page</h2>

        <form id="login-form">
            <div class="container">
                <label for="username"><b>Username</b></label>
                <input type="text" placeholder="Enter Username" name="username" id="username" required>

                <label for="password"><b>Password</b></label>
                <input type="password" placeholder="Enter Password" name="password" id="password" required>

                <button type="submit">Login</button>
                <div id="error-message" style="color: red;"></div>
            </div>
        </form>
        
        <script>
            $('#login-form').on('submit', function(event) {
                event.preventDefault(); // prevent the form from refreshing the page
                
                var username = $('#username').val();
                var password = $('#password').val();
                
                $.post({
                    url: '/auth/token',
                    data: {
                        username: username,
                        password: password
                    }
                }).done(function(data) {
                    // If login was successful, the server should have set the token as an HttpOnly cookie.
                    // There's no need to handle it here.
                }).fail(function(jqXHR, textStatus, errorThrown) {
                    // Display error message
                    $('#error-message').text('Invalid username or password. Please try again.');
                });
            });
        </script>
    </body>
</html>
    """)


if __name__ == '__main__':  # pragma: no cover
    import uvicorn
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8888,
        reload=True,
    )
