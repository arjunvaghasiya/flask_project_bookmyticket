from .models import CoupanCode, Flights, ManageTicket, Users
from email_validator import validate_email


from marshmallow import Schema, fields , validate


class SuperUserRegisterSerializer(Schema):
    password_verify = fields.String()

    class Meta:
        model = Users
        fields = (
            "email",
            "first_name",
            "last_name",
            "gender",
            "age",
            "address",
            "phone",
            "is_manager",
        )

class CoupanSerializer(Schema):
    class Meta:
        model = CoupanCode
        fields = (
            "user_id_fk",
            "coupan_code",
            "coupan_code_valid_upto",
        )

class RegisterSerializer(Schema):
    password_verify = fields.String()

    class Meta:
        model = Users
        fields = (
            "username",
            "email",
            "passport_number",
            "nationality",
            "first_name",
            "last_name",
            "address",
            "phone",
            "gender",
            "age",
        )


class UpdateRegisterSerializer(Schema):
    class Meta:
        model = Users
        fields = (
            "email",
            "first_name",
            "last_name",
            "passport_number",
            "nationality",
            "gender",
            "age",
            "address",
            "phone",
            "is_manager",
            "is_admin",
        )


class FlightsSerializer(Schema):
    class Meta:
        model = Flights
        fields = (
            "flight_id",
            "flight_name",
            "flight_airline",
            "flight_from",
            "flight_to",
            "business_class_total",
            "economy_class_total",
            "bus_cls_avl_seets",
            "ecn_cls_avl_seets",
            "dpt_date",
            "eta_date",
            "dpt_time",
            "eta_time",
            "business_class_price",
            "economy_class_price",
        )

class TicketSerializer(Schema):
    class Meta:
        model = ManageTicket
        fields = (
            "payment_id",
            "flight_id_fk",
            "booked_business_class_seats",
            "booked_economy_class_seats",
            "total_seats",
            "discount_amount_applied",
            "payment_amount",
            "ticket_valid_upto",
        )
