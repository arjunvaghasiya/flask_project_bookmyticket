from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin
from werkzeug.security import check_password_hash , generate_password_hash
from sqlalchemy import Float, ForeignKey, Integer,Table,Column,String,Boolean, DateTime,Date,Time


db = SQLAlchemy()

class Users(db.Model,UserMixin):
    
    __tablename__ = "users"
    user_id = Column(Integer,primary_key  = True,autoincrement = True)
    username = Column(String(300),nullable = False, unique = True)
    email = Column(String(300),nullable = False, unique = True)
    passport_number = Column( String(400),nullable = True)
    first_name =  Column( String(100),nullable = True)
    last_name =  Column( String(100),nullable = True)
    gender = Column(String(100),nullable =True)
    age = Column(Integer,nullable = True)
    nationality = Column( String(400),nullable = True)
    address =  Column( String(400),nullable = True)
    phone =  Column( String(400),nullable = True,unique = True)
    password_hash = Column(String(300),nullable = False,server_default= '')
    is_guest = Column(Boolean(),server_default='1')
    is_registered = Column(Boolean(),server_default='0')
    is_manager = Column(Boolean(),server_default='0')
    is_admin = Column(Boolean(),server_default='0')
    
    @property
    def password(self):
        raise AttributeError(' password is not readable')
    
    @password.setter
    def password(self,password):
        # import pdb;pdb.set_trace()
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)    
    
    def __repr__(self) -> str:
        return self.username

class Flights( db.Model,UserMixin):
    __tablename__ = "flights"
    flight_id =  Column( String(400),primary_key  = True,unique = True,nullable = False)
    flight_name = Column( String(400),nullable = True)
    flight_airline = Column( String(400),nullable = True)
    flight_from = Column( String(400),nullable = True)
    flight_to = Column( String(400),nullable = True)
    business_class_total = Column( Integer,nullable = True)
    economy_class_total = Column( Integer,nullable = True)
    bus_cls_avl_seets= Column( Integer,nullable = True)
    ecn_cls_avl_seets= Column( Integer,nullable = True)
    dpt_date = Column( Date,nullable = True)
    eta_date = Column( Date,nullable = True)
    dpt_time = Column( Time,nullable = True)
    eta_time = Column( Time,nullable = True)
    business_class_price = Column( Float,nullable = True)
    economy_class_price = Column( Float,nullable = True)
    
    def __repr__(self) -> str:
        return self.flight_id
    
class ManageTicket(db.Model,UserMixin):
    
    user_id_fk = Column(Integer,ForeignKey('users.user_id'))
    flight_id_fk = Column(String(400),ForeignKey('flights.flight_id'))
    payment_id = Column(Integer,primary_key  = True,autoincrement = True)
    discount_amount_applied = Column( Float,nullable = True)
    booked_business_class_seats = Column( Integer,nullable = True)
    booked_economy_class_seats = Column( Integer,nullable = True)
    total_seats = Column( Integer,nullable = True)
    payment_amount = Column(Float,nullable=True)
    ticket_valid_upto = Column( Date,nullable = True)

    def __repr__(self) -> str:
        return self.payment_id 
    
class CoupanCode(db.Model,UserMixin):
    
    user_id_fk = Column(Integer,ForeignKey('users.user_id'))
    coupan_code = Column(String(400),primary_key  = True,unique = True)
    coupan_code_valid_upto = Column( Date,nullable = True)
    used_status = Column(Boolean(),server_default='0')
    
    def __repr__(self) -> str:
        return self.coupan_code 