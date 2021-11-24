from resources.start_route import FirstRoute
from resources.prices import PriceRes, PriceConcretRes
from resources.parking import ParkRes

routes = (
    (FirstRoute, "/checkin"),
    (PriceRes, "/price"),
    (PriceConcretRes, "/price/<int:_id>"),
    (ParkRes, "/parking"),
)