from resources.start_route import FirstRoute
from resources.prices import PriceRes, PriceConcretRes

routes = (
    (FirstRoute, "/checkin"),
    (PriceRes, "/price"),
    (PriceConcretRes, "/price/<int:_id>"),
)