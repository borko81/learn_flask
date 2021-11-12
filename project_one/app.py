from configurations.resourse import ForTest, ShopResourse, GetToken
from configurations import api, app

api.add_resource(ForTest, '/users')
api.add_resource(ShopResourse, '/shop')
api.add_resource(GetToken, '/token')


if __name__ == '__main__':
    from configurations import models
    app.run(debug=True)