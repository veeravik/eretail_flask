from random import random
from re import template
import json
import pymongo
import datetime
from bson import json_util
from bson.json_util import dumps, loads
from flask import render_template_string, jsonify
import stripe
from flask import Flask, render_template, request, url_for, redirect
import os
from dotenv import load_dotenv



app = Flask(__name__)

load_dotenv()


stripe_api_key = os.getenv('STRIPE_API_KEY')
mongo_connection_string = os.getenv('MONGO_CONNECTION_STRING')
dep_url = os.getenv("DEPLOYMENT_URL")


stripe.api_key = stripe_api_key

client = pymongo.MongoClient(mongo_connection_string )
db = client.mydb
collection = db["eretail"]

@app.route("/",methods=["GET"])
def index():
  return "App is running. Go to /home to view."
# collection.insert_one({"product_id":"3","product_name":"Haldiram Bhujiya","product_price":"50","product_image":"https://www.bigbasket.com/media/uploads/p/l/70000835_4-haldirams-namkeen-bhujia-del.jpg?tr=w-750,q=80"})

@app.route("/signin",methods=["GET","POST"])
def signin():

  if request.method == "GET":
    return render_template("./take_input.html", dep_url = dep_url)
  elif request.method == "POST":
    data = request.form
    collection = db["customers"]
  
    collection_product=db["eretail"]
    all_products = collection_product.find()
    # user = collection.find_one({"email":data["email"],"password":data["password"]})
    if collection.find_one({"email":data["email"]}):
      # customers_name=collection.find_one({"name":data["name"]})

      if collection.find_one({"email":data["email"],"password":data["password"]}):
        return render_template("./home.html", products = all_products, user_email = data["email"])

      else:
        return "User not found or incorrect password"
    else:
      return "User not found or incorrect email"

  # print(customers_name)
    
    # user = collection.find_one({"email":data["email"],"password":data["password"]})
    # if user == None:
    #   return "User not found or incorrect email/password"
    # else:
    #   return "Email is valid. User is signed in"

@app.route("/signup",methods=["GET","POST"])
def signup():

  if request.method == "GET":
    return render_template("./new_user.html", dep_url = dep_url)
  elif request.method == "POST":
    data = request.form  
    collection = db["customers"]
 
    if collection.count_documents({"email":data["email"]}) == 0:
      stripe_customer = stripe.Customer.create(email=data["email"], name=data["name"])
      collection.insert_one({"name":data["name"],"email":data["email"],"password":data["password"], "stripe_customer_id":stripe_customer["id"]})
      # return redirect(url_for("home"))
      return" New user sucessfully resister return to <a style='color:red;' href='/signin'>Sign in</a> page."
    else:
      return "New User is already present"


@app.route("/insert_clint",methods=["GET","POST"])
def insert_clint():

  if request.method == "GET":
    return render_template("./insert_data.html", dep_url = dep_url)
  elif request.method == "POST":
    data = request.form  
    collection = db["eretail"]
 
    if collection.count_documents({"product_id":data["product_id"]}) == 0:
        collection.insert_one({"product_id":data["product_id"],"product_image":data["product_image"],"product_name":data["product_name"],"product_price":data["product_price"]})
        # return redirect(url_for("home"))
        return" New Product added sucessfully  return to <a style='color:red;' href='/insert_clint'>Add more Product</a> page."
    # else:
    #     return "New User is already present"
    else:
      return "New User is already present"


@app.route("/clint",methods=["GET","POST"])
def clint():

  if request.method == "GET":
    return render_template("./clint_take_input.html")
  elif request.method == "POST":
    data = request.form
    # print(data)
    collection = db["Clint"]
    collection_product=db["eretail"]
    all_products = collection_product.find()
    # user = collection.find_one({"email":data["email"],"password":data["password"]})
    if collection.find_one({"email":data["email"]}):
      
      if collection.find_one({"email":data["email"],"password":data["password"]}):
        return render_template("./insert_data.html", dep_url = dep_url)

      else:
        return "User not found or incorrect password"
    

    
    

    else:
      return "User not found or incorrect email"


@app.route("/logout",methods=["GET"])
def logout():
   # data = request.form
  collection_product=db["eretail"]
  all_products = collection_product.find()
  # return render_template("./home.html", products = all_products, user_email = None)
  return" Sucessfully Logout page, Return to <a style='color:red;' href='/home'>Home page</a> Or again <a style='color:red;' href='/signin'>Sign in</a> and New User can <a style='color:red;' href='/signup'>Sign Up</a> ------Thanku to visit our eretail shop.------"

@app.route("/add_to_cart",methods=["GET"])
def add_to_cart():
  
  user_email = request.args.get("email")
  if user_email == "None":
    # url_for("signin")
    return redirect(url_for("signin"))
  # user_name  =
  product_id = request.args.get("product_id")
  product_image = request.args.get("product_image")
  product_name = request.args.get("product_name")
  product_price = request.args.get("product_price")
  
  # product_id = request.form("product_id")
  # collection = db["customers"]
  # collection_product=db["eretail"]
  order=db["cart"]

  # a=collection.find_one({"email":data["email"]})
  order.insert_one({"email":user_email,"product":{"id":product_id,"name":product_name,"total_amount":product_price,"image":product_image}})
  # return redirect(url_for("home"))
  return ('', 204)
  

  # return {"email":user_email,"products":[{"product":product_id,"name":product_name,"total_amount":product_price,"image":product_image}]}

@app.route("/cart_products")
def cart_products():
  
  all_cart_product=db["cart"]
  user_email = request.args.get("email")
  # print(user_email)
  cart_data=all_cart_product.find()
  cart_data = loads(dumps(cart_data))
  cart_list=[]
  total_price=0
  # if user_email in cart_data:
  for i in range(len(cart_data)):
        if user_email in cart_data[i]["email"]:
          cart_list.append(cart_data[i]["product"])
          # print(cart_data[i]["_id"])
          # cart_list[i]["cart_ID"]=cart_data[i]["_id"]
          total_price = total_price + int(cart_data[i]["product"]["total_amount"])
  if len(cart_list)==0:
    # return f"<h1>Add Products first go to <a style='color:red;' href='/home?user_email={user_email}'>Home page </a></h1>; "
    return render_template("./Add_product.html",user_email = user_email)
    # return render_template("./home.html",first= "Add Products first go to", user_email = user_email["email"])
  # print(cart_list)
  # db. collection. deleteMany()
  
  return render_template("./cart.html", products = cart_list, user_email = user_email,total_products=len(cart_list),total_price = total_price)

@app.route("/remove_product")
def remove_product():
  all_cart_product=db["cart"]
  product_id = request.args.get("product_id").strip().lower()
  email = request.args.get("email").strip().lower()
  # email_param = request.args.get("email").strip()

  output = all_cart_product.delete_one({"email":email,"product.id":product_id})
  # print(output)
  return redirect(url_for("cart_products", email=email))

  # return str(output.acknowledged)

@app.route("/order")
def order():
  all_cart_product=db["cart"]
  cart_data=all_cart_product.find()
  cart_data = loads(dumps(cart_data))
  user_email = request.args.get("email")

  customer_collection = db["customers"]
  user_data = customer_collection.find_one({"email":user_email})
  stripe_customer_id = user_data["stripe_customer_id"]
  cart_list=[]
  total_price=0
  go_order={}
  record_data={}
  # print(user_email)
  for i in range(len(cart_data)):
        if user_email in cart_data[i]["email"]:
          cart_list.append(cart_data[i]["product"])
          total_price = total_price + int(cart_data[i]["product"]["total_amount"])
  if len(cart_list)==0:
    return "Add Products"


  stripe_data = stripe.checkout.Session.create(
      success_url=dep_url+"/success?user_email="+user_email,
      cancel_url=dep_url+"/cancel",

      line_items=[{
                'price_data': {
                  'currency': 'usd',
                  'product_data': {
                    'name': 'ecommerce product',
                  },
                  'unit_amount': total_price*100,
                },
                'quantity': 1,
              }],

      customer = stripe_customer_id,
      
      mode="payment"
    )

  checkout_url = stripe_data["url"]

  print(stripe_data)
  checkout_session_id = stripe_data["id"]
  
  
  
  # # print(cart_list)
  # print(total_price)
  go_order["user_email"] = user_email
  go_order["product"] = cart_list
  go_order["Total_price"] = total_price
  go_order["Date_Time"] =datetime.datetime.now().strftime("%I:%M%p on %d/%m/%Y")
  go_order["checkout_session_id"] = checkout_session_id
  go_order["payment_status"] = "unpaid"
  # print(go_order)
  order_ditails=db["order"]
  order_ditails.insert_one(go_order)

  auto_del = db["cart"]
  x = auto_del.delete_many({})
  print(x.deleted_count, " documents deleted.")

  # db.cart.delete_many({"email":"none"})
 
  

  # return ('', 204)
  return redirect(checkout_url)

@app.route("/success",methods=["GET","POST"])
def success():

  if request.method == "GET":
    user_email = request.args.get("user_email")

    return render_template("./success_url.html",user_email=user_email)
  else:

    endpoint_secret = "whsec_ROgetvo6RDbCkUJ4kzEgQUalJkur5fbR"
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    if event.type == 'payment_intent.succeeded':
      print("payment intent id is ", event["data"]["object"]["id"])

      stripe_checkout = stripe.checkout.Session.list(payment_intent = event["data"]["object"]["id"], limit=1)
      checkout_id = stripe_checkout["data"][0]["id"]
      order_collection = db["order"]
      order_collection.update_one({"checkout_session_id":checkout_id},{ "$set": { 'payment_status': "paid" } })

    # Handle the event
    print('Handled event type {}'.format(event['type']))

    return jsonify(success=True)

@app.route("/cancel",methods=["GET"])
def cancel():
  return render_template("./cancel_url.html")


@app.route("/order_history")
def order_history():
  all_order=db["order"]
  data = request.args.get("email")
  history=all_order.find({"user_email":data})
  history = loads(dumps(history))
  print(history)

  if history==[]:
    return render_template("./order_product.html",user_email = data)
  else:
    history_data=[]
    
    for i in history:
      list_history={}
      list_history["product"] = i["product"]
      list_history["Date_Time"] = i["Date_Time"]
      list_history["Total_price"] = i["Total_price"]
      list_history["order_id"] = str(i["_id"])
      list_history["payment_status"] = i["payment_status"]
      history_data.append(list_history)
  
  
    
    # print(list_history)
    # return history_data
    return render_template("./order_history.html",history_data=history_data,user_email = data)

  
  # return ('', 204)






@app.route("/home")
def home():
    try:
      user_email = request.args.get("user_email")
    except:
      user_email=None
    all_products = collection.find()
    # print(all_products)
    return render_template("./home.html", products = all_products, user_email = user_email)


@app.route("/insert_one")
def insert():
  data = [{"product_id":"3","product_name":"Park Avenue","product_price":"42","product_image":"https://images-static.nykaa.com/media/catalog/product/8/e/8e91d6c8901277019202.jpg?tr=w-344,h-344,cm-pad_resize"},
          {"product_id":"4","product_name":"Haldiram Sonpapri","product_price":"50","product_image":"https://www.bigbasket.com/media/uploads/p/l/70000835_4-haldirams-namkeen-bhujia-del.jpg?tr=w-750,q=80"},
          {"product_id":"5","product_name":"Haldiram Bhujiya","product_price":"50","product_image":"https://www.bigbasket.com/media/uploads/p/l/70000835_4-haldirams-namkeen-bhujia-del.jpg?tr=w-750,q=80"},
          {"product_id":"6","product_name":"Park Avenue","product_price":"42","product_image":"https://images-static.nykaa.com/media/catalog/product/8/e/8e91d6c8901277019202.jpg?tr=w-344,h-344,cm-pad_resize"},
          {"product_id":"7","product_name":"Park Avenue","product_price":"42","product_image":"https://images-static.nykaa.com/media/catalog/product/8/e/8e91d6c8901277019202.jpg?tr=w-344,h-344,cm-pad_resize"},
          {"product_id":"8","product_name":"Park Avenue","product_price":"42","product_image":"https://images-static.nykaa.com/media/catalog/product/8/e/8e91d6c8901277019202.jpg?tr=w-344,h-344,cm-pad_resize"},
          {"product_id":"9","product_name":"Park Avenue","product_price":"42","product_image":"https://images-static.nykaa.com/media/catalog/product/8/e/8e91d6c8901277019202.jpg?tr=w-344,h-344,cm-pad_resize"},
          {"product_id":"10","product_name":"Park Avenue","product_price":"42","product_image":"https://images-static.nykaa.com/media/catalog/product/8/e/8e91d6c8901277019202.jpg?tr=w-344,h-344,cm-pad_resize"}]
  
  collection.insert_many(data)

  return "Data inserted successfully"



# @app.route("/file",methods=["POST"])
# def store_data():
    

#     try:
#         data = json.loads(request.data)
#     except:
#         data = request.form
       
#     print(data)
#     path = "d:\PROGRAM\python\Project\templatesS\json_data.json"

#     with open(path,"r") as fp:
#         d = json.load(fp)
#         d.append(data)
        
#     with open(path,"w") as fp:
#         json.dump(d,fp)
#     return "json data succesfully uploaded"


# app.run("0.0.0.0",debug=True)





