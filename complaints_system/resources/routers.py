from resources.auth import RegisterComplainer, LoginComplainer

routers = (
    (RegisterComplainer, '/register'),
    (LoginComplainer, '/login')
)