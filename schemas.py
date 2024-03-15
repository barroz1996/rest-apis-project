from marshmallow import Schema,fields


class PlainItemScheme(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)
  price = fields.Float(reqired = True)

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class PlainTagSchema(Schema):
   id = fields.Int(dump_only=True)
   name = fields.Str()


class ItemUpdateSchema(Schema):
  name = fields.Str()
  price = fields.Float()
  store_id = fields.Int()


  
class ItemScheme(PlainItemScheme):
  store_id = fields.Int(required = True, load_only = True)
  store = fields.Nested(PlainStoreSchema(), dump_only = True)
  tags = fields.List(fields.Nested(PlainTagSchema()),dump_only=True)

  

class StoreSchema(PlainStoreSchema):
   items = fields.List(fields.Nested(PlainItemScheme()),dump_only = True)
   tags = fields.List(fields.Nested(PlainTagSchema()),dump_only = True)


class TagSchema(PlainTagSchema):
   store_id = fields.Int( load_only = True)
   store = fields.Nested(PlainStoreSchema(), dump_only = True)
   items = fields.List(fields.Nested(PlainItemScheme()), dump_only=True)


class TagAndItemSchema(Schema):
   message= fields.Str()
   item = fields.Nested(ItemScheme)
   tag = fields.Nested(TagSchema)
   
   

class UserSchema(Schema):
   id = fields.Int(dump_only = True)
   username = fields.Str(required=True)
   password = fields.Str(required=True)


