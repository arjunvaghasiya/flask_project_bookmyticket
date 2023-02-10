from website import api, app, mail
from flask_restful import Resource, request
from .models import Users, db
from .serializer import *
from flask import jsonify, request, Flask, make_response
from email_validator import validate_email, EmailNotValidError
from website.authentication import *
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from flask_mail import Mail, Message
from datetime import datetime
import string
import random


def coupan_code():
    length = 15
    characterList = ""
    characterList += string.ascii_letters
    characterList += string.digits

    password = ""
    for i in range(length):
        randomchar = random.choice(characterList)
        password += randomchar
    return password


@app.post("/create/admin/<int:pk>")
def admin_crt(pk):
    create_admin_key = "ihsa99cn9aKAGIA344ADF4bf8d7f21eb"
    data = request.get_json()
    if create_admin_key == data.get("admin_key"):
        user = Users.query.filter_by(user_id=pk).first()
        user.is_guest = True
        user.is_registered = True
        user.is_manager = True
        user.is_admin = True
        db.session.add(user)
        db.session.commit()
        return "ADMIN CREATED SUCCESSFULLY"
    else:
        return "ADMIN KEY IS WRONG"


@app.get("/login/")
@basic_authentication_user
def login(a, b):
    user = Users.query.filter_by(username=request.authorization.username).first()
    is_pass_correct = user.verify_password(request.authorization.password)
    if is_pass_correct:
        refresh = create_refresh_token(identity=user.username)
        access = create_access_token(identity=user.username)
        context = {}
        context = {
            "Username  ": user.username,
            "Refresh_Token  ": refresh,
            "Access_Token  ": access,
        }
        return context, 200
    else:
        return make_response(
            jsonify({"error": "Invalid username or password"}), status=401
        )


def send_email(user, token, un):
    msg = Message("hello User", sender="arjunvaghasiya361@gmail.com", recipients=[user])
    msg.body = f"Hit This Link For Email Activation \n \n === > 'Veryfy for Activation' : \n http://127.0.0.1:5000/verify/{token}/{un}/"
    mail.send(msg)


def verify(token, un):
    # import pdb;pdb.set_trace()
    user = Users.query.filter_by(username=un).first()
    if user:
        user.is_registered = True
        db.session.add(user)
        db.session.commit()
        return {
            "Status": "you have registerd succesfully",
            "Username": f"Username is {user}",
            "Token": f"{token}",
        }, 200
    else:
        return {"Error": "User Not Found"}


app.add_url_rule("/verify/<token>/<un>/", "verify", verify)


class RegisterUser(Resource):
    def post(self):
        try:
            data = request.get_json()
            # import pdb;pdb.set_trace()
            if data.get("password") == data.get("password_verify"):
                try:
                    validate_email(data.get("email"))
                    user = Users(
                        username=data.get("username"),
                        email=data.get("email"),
                        first_name=data.get("first_name"),
                        last_name=data.get("last_name"),
                        gender=data.get("gender"),
                        age=data.get("age"),
                        phone=data.get("phone"),
                        address=data.get("address"),
                        password=data.get("password"),
                        passport_number=data.get("passport_number"),
                        nationality=data.get("nationality"),
                    )
                    db.session.add(user)
                    db.session.commit()
                    access = create_access_token(identity=user.username)
                    send_email(user.email, access, user.username)
                    serializer = RegisterSerializer()
                    data = serializer.dump(user)
                    return data, 200
                except EmailNotValidError as e:
                    return make_response(
                        jsonify({"error": f"email is not proper {e}"}), 401
                    )

            else:
                return make_response(jsonify({"error": "passsord is not matched"}), 401)
        except:
            return make_response(jsonify({"error": "DATABASE ERROR"}), 401)

    # @basic_authentication_SuperUser_Admin
    def get(self):
        # import pdb;pdb.set_trace()
        try:
            db.create_all()
            return "Tables Created"
        except:
            return "Database Error"


api.add_resource(RegisterUser, "/")


class AdminUpdateUser(Resource):
    @basic_authentication_for_super_admin
    def put(self, pk):
        query = Users.query.filter_by(user_id=int(pk)).first()
        data = request.get_json()
        if data.get("email") != "":
            query.email = data.get("email")
        if data.get("gender") != "":
            query.gender = data.get("gender")
        if data.get("age") != "":
            query.age = data.get("age")
        if data.get("is_manager") != "":
            query.is_manager = data.get("is_manager")
        if data.get("first_name") != "":
            query.first_name = data.get("first_name")
        if data.get("nationality") != "":
            query.nationality = data.get("nationality")
        if data.get("passport_number") != "":
            query.passport_number = data.get("passport_number")
        if data.get("last_name") != "":
            query.last_name = data.get("last_name")
        if data.get("address") != "":
            query.address = data.get("address")
        if data.get("phone") != "":
            query.phone = data.get("phone")
        db.session.add(query)
        db.session.commit()
        result = Users.query.filter_by(user_id=int(pk)).first()
        serializer = SuperUserRegisterSerializer()
        data1 = serializer.dump(result)
        return jsonify(data1)
        # import pdb;pdb.set_trace()

    @basic_authentication_SuperUser_Admin
    def get(self, pk):
        users = Users.query.all()
        serializer = RegisterSerializer(many=True)
        data = serializer.dump(users)
        return jsonify(data)


api.add_resource(AdminUpdateUser, "/admin/user_update/<int:pk>", endpoint="user_update")
api.add_resource(AdminUpdateUser, "/admin/all_users/", endpoint="all_users")


class CoupanManagement(Resource):
    @basic_authentication_SuperUser_Admin
    def get(self, pk):
        try:
            coupan = CoupanCode.query.filter_by(user_id_fk=int(pk)).all()
        except:
            return make_response(jsonify({"error": "SQL error"}), 401)
        serializer = CoupanSerializer(many=True)
        data = serializer.dump(coupan)
        if not data:
            return make_response(jsonify({"error": "Data not found"}), 401)
        else:

            return jsonify(data)

    @basic_authentication_SuperUser_Admin
    def post(self, pk):
        data = request.get_json()
        cpn_code = coupan_code()
        try:
            user = Users.query.filter_by(user_id=int(pk)).first()
            coupan = CoupanCode(
                user_id_fk=int(user.user_id),
                coupan_code=cpn_code,
                coupan_code_valid_upto=data.get("coupan_code_valid_upto"),
            )
            db.session.add(coupan)
            db.session.commit()
        except:
            return make_response(jsonify({"error": "SQL error"}), 401)

        return make_response(jsonify({"success": "Coupan alloted successfully"}), 200)

    @basic_authentication_SuperUser_Admin
    def delete(self, pk):
        data = request.get_json()
        try:
            coupan = CoupanCode.query.filter_by(
                coupan_code=str(data.get("coupan_code"))
            ).first()
            db.session.delete(coupan)
            db.session.commit()
        except:
            return make_response(jsonify({"error": "SQL error"}), 401)

        return make_response(jsonify({"success": "Coupan deleted successfully"}), 200)


api.add_resource(CoupanManagement, "/allot_coupan/<pk>", endpoint="allot_coupan")


@app.get("/coupan")
@jwt_required()
def my_coupan():
    try:
        # import pdb; pdb.set_trace()
        user = Users.query.filter_by(username=str(get_jwt_identity())).first()
        coupan = CoupanCode.query.filter_by(user_id_fk=int(user.user_id)).all()
    except:
        return make_response(jsonify({"error": "SQL error"}), 401)
    serializer = CoupanSerializer(many=True)
    data = serializer.dump(coupan)
    if not data:
        return make_response(jsonify({"error": "Data not found"}), 401)
    else:
        return jsonify(data)


class AdminAddFlight(Resource):
    @basic_authentication_for_super_admin
    def post(self, pk):
        try:
            data = request.get_json()
            user = Flights(
                flight_id=data.get("flight_id"),
                flight_name=data.get("flight_name"),
                flight_airline=data.get("flight_airline"),
                flight_from=data.get("flight_from"),
                flight_to=data.get("flight_to"),
                business_class_total=data.get("business_class_total"),
                economy_class_total=data.get("economy_class_total"),
                bus_cls_avl_seets=data.get("bus_cls_avl_seets"),
                ecn_cls_avl_seets=data.get("ecn_cls_avl_seets"),
                dpt_date=data.get("dpt_date"),
                eta_date=data.get("eta_date"),
                dpt_time=data.get("dpt_time"),
                eta_time=data.get("eta_time"),
                business_class_price=data.get("business_class_price"),
                economy_class_price=data.get("economy_class_price"),
            )
            db.session.add(user)
            db.session.commit()
            return jsonify(data)
        except:
            return make_response(jsonify({"error": "DATABASE ERROR"}), 401)
        # import pdb;pdb.set_trace()

    @basic_authentication_for_super_admin
    def put(self, pk):
        query = Flights.query.filter_by(flight_id=str(pk)).first()
        data = request.get_json()
        if data.get("flight_id") != "":
            query.flight_id = data.get("flight_id")
        if data.get("flight_name") != "":
            query.flight_name = data.get("flight_name")
        if data.get("flight_airline") != "":
            query.flight_airline = data.get("flight_airline")
        if data.get("flight_from") != "":
            query.flight_from = data.get("flight_from")
        if data.get("flight_to") != "":
            query.flight_to = data.get("flight_to")
        if data.get("business_class_total") != "":
            query.business_class_total = data.get("business_class_total")
        if data.get("economy_class_total") != "":
            query.economy_class_total = data.get("economy_class_total")
        if data.get("bus_cls_avl_seets") != "":
            query.bus_cls_avl_seets = data.get("bus_cls_avl_seets")
        if data.get("ecn_cls_avl_seets") != "":
            query.ecn_cls_avl_seets = data.get("ecn_cls_avl_seets")
        if data.get("dpt_date") != "":
            query.dpt_date = data.get("dpt_date")
        if data.get("eta_date") != "":
            query.eta_date = data.get("eta_date")
        if data.get("dpt_time") != "":
            query.dpt_time = data.get("dpt_time")
        if data.get("eta_time") != "":
            query.eta_time = data.get("eta_time")
        if data.get("business_class_price") != "":
            query.business_class_price = data.get("business_class_price")
        if data.get("economy_class_price") != "":
            query.economy_class_price = data.get("economy_class_price")
        db.session.add(query)
        db.session.commit()
        return jsonify(data)


api.add_resource(AdminAddFlight, "/admin/flight_add/", endpoint="flight_add")
api.add_resource(AdminAddFlight, "/admin/flight_update/<pk>", endpoint="flight_update")


@app.post('/update/user/')
@jwt_required()
def update_user():
    user = Users.query.filter_by(username = str(get_jwt_identity())).first()
    data = request.get_json()    
    if data.get('email') != "":
        user.email = data.get('email')
    if data.get('passport_number') != "":
        user.passport_number = data.get('passport_number')
    if data.get('nationality') != "":
        user.nationality = data.get('nationality')        
    if data.get('gender') != "":
        user.gender = data.get('gender')
    if data.get('first_name') != "":
        user.first_name = data.get('first_name')
    if data.get('last_name') != "":
        user.last_name = data.get('last_name')
    if data.get('address') != "":
        user.address = data.get('address')        
    if data.get('phone') != "":
        user.phone = data.get('phone')
    if data.get('age') != "":
        user.age = data.get('age')
    db.session.add(user)
    db.session.commit()
    return jsonify(data)


@app.route("/flights/<int:pgno>")
@app.route("/flights/<from_>/<to_>/<int:pgno>")
@app.route("/flights/<from_>/<to_>/<float:price>/<int:pgno>")
@app.route(
    "/flights/date/<from_>/<to_>/<int:year>/<int:month>/<int:day>/<int:pgno>"
)  # according to the date search
def flights(from_="", to_="", price="", date_="", pgno="", year="", month="", day=""):
    # import pdb;pdb.set_trace()user1
    ROWS_PER_PAGE = 2
    page = request.args.get("page", pgno, type=int)
    # import pdb;pdb.set_trace()
    if from_ == "" and to_ == "" and price == "" and date_ == "":
        flights = Flights.query.order_by(Flights.flight_id.desc()).paginate(
            page=page, per_page=ROWS_PER_PAGE
        )
        serializer = FlightsSerializer(many=True)
        data = serializer.dump(flights.items)
        return jsonify(data)

    if (
        from_ != ""
        and to_ != ""
        and pgno != ""
        and not price
        and not year
        and not month
    ):
        flights = Flights.query.filter(
            (Flights.flight_from == from_) | (Flights.flight_to == to_)
        ).paginate(page=page, per_page=ROWS_PER_PAGE)
        serializer = FlightsSerializer(many=True)
        data = serializer.dump(flights.items)
        return jsonify(data)

    if from_ != "" and to_ != "" and price != "" and pgno != "":
        # import pdb;pdb.set_trace()
        flights = Flights.query.filter(
            Flights.flight_from == from_,
            Flights.flight_to == to_,
            Flights.business_class_price <= price,
            Flights.economy_class_price <= price,
        ).paginate(page=page, per_page=ROWS_PER_PAGE)
        serializer = FlightsSerializer(many=True)
        data = serializer.dump(flights.items)
        return jsonify(data)

    if (
        from_ != ""
        and to_ != ""
        and year != ""
        and month != ""
        and day != ""
        and pgno != ""
    ):

        d_ = f"{year}-{month}-{day}"

        flights = Flights.query.filter(
            Flights.flight_from == str(from_),
            Flights.flight_to == str(to_),
            Flights.dpt_date == d_,
        ).paginate(page=page, per_page=ROWS_PER_PAGE)
        serializer = FlightsSerializer(many=True)
        data = serializer.dump(flights.items)
        if not data:
            return make_response(jsonify({"error": "Data not found"}), 401)
        else:
            return jsonify(data)


def payment_amount(a, b, discount):
    total_amount = float(a) + float(b)
    if discount == False:
        return total_amount
    if discount == True:
        dis = (10 / 100) * total_amount
        dis1 = total_amount - dis
        return dis, dis1


@app.post("/book")
@jwt_required()
def book_ticket():
    # import pdb

    # pdb.set_trace()
    print(get_jwt_identity())
    data = request.get_json()
    fl_id = data.get("flight_id")
    cp_code = data.get("coupan_code")

    if fl_id == "":
        if data.get("b_class") and data.get("e_class") == "":
            return make_response(
                jsonify({"Data missing": "Ticket Information Missing"}), 400
            )
        return make_response(
            jsonify({"Data missing": "Ticket Information Missing"}), 400
        )

    try:
        if data.get("b_class") != "" or data.get("e_class") != "":
            flights = Flights.query.filter_by(flight_id=str(fl_id)).first()
            var_busc = int(flights.bus_cls_avl_seets)
            var_ecoc = int(flights.ecn_cls_avl_seets)
            var_user_busc = data.get("b_class")
            var_user_ecoc = data.get("e_class")
            if (var_busc - var_user_busc) >= 0:
                flights.bus_cls_avl_seets = var_busc - var_user_busc
            else:
                return make_response(
                    jsonify({"Not Avaliable": "Housefull BusinessClass"})
                )
            if (var_ecoc - var_user_ecoc) >= 0:
                flights.ecn_cls_avl_seets = var_ecoc - var_user_ecoc
            else:
                return make_response(
                    jsonify({"Not Avaliable": "Housefull EconomyClass"})
                )

            db.session.add(flights)
            db.session.commit()
            # payment =

    except:
        return make_response(jsonify({"Un-Success": "Something Wrong"}), 400)

    try:
        var_bcl = float(flights.business_class_price) * int(data.get("b_class"))
        var_ecl = float(flights.economy_class_price) * int(data.get("e_class"))
        coupan = CoupanCode.query.filter_by(coupan_code=cp_code).first()
        user = Users.query.filter_by(username=str(get_jwt_identity())).first()
        if not coupan:
            final_amount = payment_amount(a=var_bcl, b=var_ecl, discount=False)
            get_dicount_amount = 0
        else:
            if coupan.used_status == True:
                return make_response(
                    jsonify({"Un-Success": "You Used this coupan-code once"}), 400
                )
            payable_amount = payment_amount(a=var_bcl, b=var_ecl, discount=True)
            get_dicount_amount = int(payable_amount[0])
            final_amount = int(payable_amount[1])
            coupan.used_status = True
            db.session.add(coupan)
            db.session.commit()
        ticket = ManageTicket(
            user_id_fk=user.user_id,
            flight_id_fk=flights.flight_id,
            discount_amount_applied=get_dicount_amount,
            payment_amount=final_amount,
            ticket_valid_upto=flights.dpt_date,
            booked_business_class_seats=var_user_busc,
            booked_economy_class_seats=var_user_ecoc,
            total_seats=var_user_busc + var_user_ecoc,
        )
        if final_amount > 0:
            db.session.add(ticket)
            db.session.commit()
            user_ticket = ManageTicket.query.filter_by(
                user_id_fk=int(user.user_id)
            ).first()
            serializer = RegisterSerializer()
            data2 = serializer.dump(user)
            serializer = FlightsSerializer()
            data1 = serializer.dump(flights)
            serializer = TicketSerializer()
            data = serializer.dump(user_ticket)

            if not data:
                return make_response(jsonify({"error": "Data not found"}), 401)
            else:
                return jsonify(data, data1, data2), 200
        else:
            return make_response(jsonify({"Un-Success": "Something Wrong"}), 400)

    except:
        return make_response(jsonify({"Un-Success": "Something Wrong"}), 400)

@basic_authentication_user
@app.get("/my_tickets")
def my_tickets():
    user = Users.query.filter_by(username = request.authorization.username).first()
    user_ticket = ManageTicket.query.filter_by(user_id_fk=int(user.user_id)).all()
    serializer = TicketSerializer(many=True)
    data = serializer.dump(user_ticket)
    if not data:
        return make_response(jsonify({"error": "You have not booked any flights "}), 401)
    else:
        return jsonify(data), 200