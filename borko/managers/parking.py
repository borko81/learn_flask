from db import db
from models import PricesModel
from models.parking import ParkModel
from schemas.parking import ParkEnterSchema, ParkResponseSchema
from datetime import datetime


# PricesModel.query.filter(PricesModel.stay_time <= '03:56')[-1]

def validate_car_already_in_park(user_name):
    return ParkModel.query.filter_by(name=user_name).filter_by(get_out=None)


def conv_to_zerofill(param):
    return str(param).zfill(2)


def hours_and_minutes_from_seconds(sec):
    hours = int(sec // 3600)
    minutes = int((sec % 3600) // 60)
    return f"{conv_to_zerofill(hours)}:{conv_to_zerofill(minutes)}"


def calculate_total_time(time_enter, time_leave):
    total_time = (
            time_leave - time_enter
    ).total_seconds()

    return hours_and_minutes_from_seconds(total_time)


def calculate_taxes_of_car(car):
    enter_time = car.first().get_in
    leave_time = datetime.now()
    total_time = calculate_total_time(enter_time, leave_time)
    price = PricesModel.query.filter(PricesModel.stay_time <= total_time)[-1]
    return price.price



def total_update_car_end_time_and_tax(car):
    price = calculate_taxes_of_car(car)
    car.update({'get_out': datetime.now(), 'tax': price})
    return price


class ParkingManager:

    @staticmethod
    def input_new_car_in_park(data):
        test_car_already_in_park = validate_car_already_in_park(data['name'])
        if test_car_already_in_park.first() is None:
            car = ParkModel(**data)
            schema = ParkResponseSchema()
            db.session.add(car)
            db.session.flush()
            return schema.dump(car)
        price = total_update_car_end_time_and_tax(test_car_already_in_park)
        return {"message": "Car update successfully", 'price': price}

    @staticmethod
    def show_car_in_park():
        schemas = ParkResponseSchema()
        return schemas.dump(ParkModel.query.all(), many=True)
