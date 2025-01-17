from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pytz import timezone
spain_tz = timezone('Europe/Madrid')
from enum import Enum
# import pandas as pd


# cars_data = pd.read_csv('/workspaces/Watacar_v2/src/api/brands-and-models/cars-2020.csv',
#                     header = None)


#print(cars_data.head())



db = SQLAlchemy()

class IdDocument(Enum):
    DNI = 'DNI'
    CIF = 'CIF'

class User_role(Enum): #Solo se pueden usar los roles que pongamos aquí
    COMMON_USER= 'common_user'
    GARAGE = 'garage'




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email =  db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    document_type = db.Column(db.Enum(IdDocument), nullable=True, default=IdDocument.DNI)
    document_number = db.Column(db.String(10), unique=True, nullable=True)
    address = db.Column(db.String(120), nullable=True) 
    role = db.Column(db.Enum(User_role), nullable=False, default=User_role.COMMON_USER)
    phone = db.Column(db.Integer, nullable=True) 
    avatar = db.Column(db.String(200))
    #is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    products = db.relationship('Product', backref='user') # Un usuario puede tener muchos productos asociados (relación de 1 a muchos)
    favorites = db.relationship('Favorites', backref='user') # Un usuario puede tener muchos favoritos asociados (relación de 1 a muchos)
    sales = db.relationship('Sale', backref='user', foreign_keys='Sale.buyer_id') # Un usuario puede buscar buscar las ventas que hizo (1 a muchos)
    garage = db.relationship('Garage', backref='user')
    status = db.relationship('status', backref='user')



    # seller_reviews = db.relationship('Review', backref='user') # Preguntar a profes si és una relación recíproca (puedo ver las reseñas que me han puesto y las que he puesto)
    # buyer_reviews = db.relationship('Review', backref='user') # Preguntar a profes si és una relación recíproca (puedo ver las reseñas que me han puesto y las que he puesto)


    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            #"surname": self.surname,
            "email": self.email,
            "document_type": self.document_type.value,
            "document_number": self.document_number,
            "address": self.address, 
            "role": self.role.value,
            "phone": self.phone,
            "avatar": self.avatar
            
            # do not serialize the password, its a security breach
        }
    


    


class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return f'<Favorite {self.id}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id
        }
    


class ProductState(Enum):
    NUEVO = 'Nuevo'
    SEMINUEVO = 'Seminuevo'

class fuel_type(Enum):
    DIESEL = 'Diesel'
    GASOLINA = 'Gasolina'
    HIBRIDO = 'Hibrido'
    ELECTRICO = 'Electrico'

class product_type(Enum):
    MOTO = 'Moto'
    COCHE = 'Coche'
    


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.Enum(ProductState), nullable=False)
    price = db.Column(db.Float, nullable=False) #Estuve leyendo y cuando no quieres un número de decimales exactos el FLOAT es buena opción
    description = db.Column(db.String(2000))
    product_type = db.Column(db.Enum(product_type), nullable=True, default=product_type.COCHE)
    year = db.Column(db.Integer)
    km = db.Column(db.Integer)
    fuel = db.Column(db.Enum(fuel_type), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    images = db.relationship('Image', backref='product')
    brand = db.relationship('Brand', backref='products')
    model = db.relationship('Model', backref='products')

    def __repr__(self):
        return f'<Products {self.id}>'
    
    def serialize(self):
        user=User.query.get(self.user_id)
        return {
            "id": self.id,
            "name": self.name,
            "state": self.state.value,
            "price": self.price,
            "description": self.description,

            "images": [image.serialize() for image in self.images],

            "brand": self.brand.serialize(),
            "model": self.model.serialize(),
            "user": self.user.serialize(), #puede petar si creo producto desde admin

            "status": status.query.get(self.status_id).status.value,


            "year": self.year,
            "km": self.km,
            "fuel": self.fuel.value,
            "user_id": self.user_id,
            "user_full_name": user.full_name,
            "brand_id": self.brand_id,
            "model_id": self.model_id,
            "product_type": self.product_type.value
        }

class status_product(Enum):
    ONSALE = 'on sale'
    PENDING_SALE = 'pending sale'
    PENDING_BLOCKED = 'pending blocked'
    BLOCKED = 'blocked'
    SOLD = 'sold'
    SOLD_REVIEWED = 'sold reviewed'


class status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(status_product), nullable=False)
    given_review_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product = db.relationship('Product', backref='status')

class Garage (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    web = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(15), nullable=False)
    mail = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    cif = db.Column(db.String(10), nullable=False)
    avatar = db.Column(db.String(200))

    # avatar = db.Column(db.Integer, db.ForeignKey('image.id')) 
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    services = db.relationship('Service', backref='garage')

    def __repr__(self):
        return f'<Garages {self.id}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "web" : self.web,
            "phone": self.phone,
            "mail": self.mail,
            "address": self.address,
            "description": self.description,
            "cif": self.cif,
            "avatar": self.avatar,
            "product_id": self.product_id,
            "user_id": self.user_id
        }


class Image (db.Model): # Duda. No sé si debería ir también un relationship de esta tabla en users
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image = db.Column(db.String(200), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    

    def __repr__(self):
        return f'<Images {self.id}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "image": self.image,
            "product_id": self.product_id
        }
    

    
class Service (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(300), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    garage_id = db.Column(db.Integer, db.ForeignKey('garage.id'))

    def __repr__(self):
        return f'<Services {self.id}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "image_id": self.image_id,
            "garage_id": self.garage_id
        }


    
class Review(db.Model): # Cambiar la tabla para que se pueda asociar al comrpador y al vendedor
    id = db.Column(db.Integer, primary_key=True)
    given_review_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recived_review_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    comment = db.Column(db.String(250), nullable=True)

    given = db.relationship('User', foreign_keys=[given_review_id])
    recived = db.relationship('User', foreign_keys=[recived_review_id])


    

    #GPT DICE QUE AÑADA ESTO PORQUE SINÓ PUEDE CREAR CONFUSIÓN
    # buyer = db.relationship('User', foreign_keys=[buyer_id], backref='buyer_reviews')
    # seller = db.relationship('User', foreign_keys=[seller_id], backref='seller_reviews')

    def __repr__(self):
        return f'<Reviews {self.id}>'
    
    def serialize(self):
        return{
            "id": self.id,
            "buyer_id": self.buyer_id,
            "seller_id": self.seller_id,
            "product_id": self.product_id,
            "stars": self.stars.value,
            "comment": self.comment
        }
    
class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    garage_id = db.Column(db.Integer, db.ForeignKey('garage.id'))
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.now(spain_tz))
    #Posibilidad de añadir reviews en la tabla

    def __repr__(self):
        return f'<Sales {self.id}>'
    
    def serialize(self):
        return{
            "id": self.id,
            "buyer_id": self.buyer_id,
            "seller_id": self.seller_id,
            "product_id": self.product_id,
            "taller_id": self.taller_id,
            "fecha": self.fecha
        }
    

class vehicle_type(Enum):
    #SELECCIONA = 'selecciona'
    MOTO = 'moto'
    CAR = 'car'
    COCHE = 'coche'
    
class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    vehicle_type = db.Column(db.Enum(vehicle_type), nullable=True, default=vehicle_type.COCHE)

    models = db.relationship('Model', backref='brands') # Podemos acceder a modelos asociados a una marca . 1 modelo solo puede pertenecer a 1 marca, las marcas peuden tener varios modelos

    def __repr__(self):
        return f'<Brands {self.id}>'
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "vehicle_type": self.vehicle_type.value.upper()

        }
    

    
class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50), nullable=False)
    #type = db.Column(db.String(20), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    #product_type = db.Column(db.Enum(product_type), nullable=True, default=product_type.COCHE)

    # brands = db.relationship('Brand', backref='models') # Podemos acceder a una marca asociada con modelos 

    def __repr__(self):
        return f'<Models {self.id}>'
    
    def serialize(self):
        return{
            "id": self.id,
            "model": self.model,
            #"type": self.type,
            "brand_id": self.brand_id,
            #"product_type": self.product_type.value
        }
    


# class MotoBrand(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)

#     models = db.relationship('Model', backref='brands') # Podemos acceder a modelos asociados a una marca . 1 modelo solo puede pertenecer a 1 marca, las marcas peuden tener varios modelos

#     def __repr__(self):
#         return f'<Brands {self.id}>'
    
#     def serialize(self):
#         return{
#             "id": self.id,
#             "name": self.name,
#         }
    
# class MotoModel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     model = db.Column(db.String(50), nullable=False)
#     #type = db.Column(db.String(20), nullable=False)
#     brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))

#     # brands = db.relationship('Brand', backref='models') # Podemos acceder a una marca asociada con modelos 

#     def __repr__(self):
#         return f'<Models {self.id}>'
    
#     def serialize(self):
#         return{
#             "id": self.id,
#             "model": self.model,
#             #"type": self.type,
#             "brand_id": self.brand_id
#         }