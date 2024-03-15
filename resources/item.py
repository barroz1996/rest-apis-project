from flask import request
from flask.views  import MethodView
from flask_smorest import Blueprint, abort
from models import ItemModel
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError
from db import db


from schemas import  ItemScheme, ItemUpdateSchema

blp = Blueprint("Items", __name__, description = "Operations on items")

@blp.route("/item/<int:item_id>")
class Item(MethodView):
  @jwt_required()
  @blp.response(200, ItemScheme)
  def get(self,item_id):
      item = ItemModel.query.get_or_404(item_id)
      return item
  
  @jwt_required()    
  def delete(self,item_id):
      jwt = get_jwt()
      if not jwt.get("is admin"):
         abort(401, message = "Admin privilege required.")

      item = ItemModel.query.get_or_404(item_id)
      db.session.delete(item)
      db.session.commit()
      return {"message" : "Item deleted."}

  @blp.arguments(ItemUpdateSchema)
  @blp.response(200, ItemScheme)
  def put(self,item_data ,item_id): 
      item = ItemModel.query.get(item_id)
      if item:
         item.price = item_data["price"]
         item.name = item_data["name"]
      else:
         item = ItemModel(id= item_id,**item_data)
      db.session.add(item)
      db.session.commit()
      return item

@blp.route("/item")
class ItemList(MethodView):
  @jwt_required()
  @blp.response(200, ItemScheme(many=True))
  def get(self):
    return ItemModel.query.all()


  @jwt_required(fresh=True)
  @blp.arguments(ItemScheme)  # the itemscheme check the json and give the method argument item_data
  @blp.response(201, ItemScheme)
  def post(self, item_data):   
    item = ItemModel(**item_data)

    try:
       db.session.add(item)   #we can add multiply things , we can add money things before we every each time commit its take time to save to db everytime
       db.session.commit()  # this is saveing the date to the db
    except SQLAlchemyError:
       abort(500, message = "An error occurred while inserting the item.")

    return item      