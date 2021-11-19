from resources.auth import RegisterComplainer, LoginComplainer
from resources.complaint import CompplaintListCreate

routers = (
    (RegisterComplainer, '/register'),
    (LoginComplainer, '/login'),
    (CompplaintListCreate, '/complainers/complaints')
)