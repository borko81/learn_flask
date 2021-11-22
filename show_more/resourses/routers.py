from resourses.userresourse import UserRegisterResourse, UserLoginResourse, GetAllUserResourse
from resourses.check_token_resourse import CheckToken


routs = (
    (UserRegisterResourse, '/register'),
    (UserLoginResourse, '/login'),
    (GetAllUserResourse, '/all_users'),
    (CheckToken, '/check'),
)