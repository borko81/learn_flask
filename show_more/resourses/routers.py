from resourses.userresourse import UserRegisterResourse, UserLoginResourse, GetAllUserResourse
from resourses.check_token_resourse import CheckToken
from resourses.place_resourse import PlaceResourse, PlaceSpecificResourse


routs = (
    (UserRegisterResourse, '/register'),
    (UserLoginResourse, '/login'),
    (GetAllUserResourse, '/all_users'),
    (CheckToken, '/check'),
    (PlaceResourse, '/places'),
    (PlaceSpecificResourse, '/place/<int:_id>'),
)