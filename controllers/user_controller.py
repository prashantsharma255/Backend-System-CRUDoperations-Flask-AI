from crypt import methods
import imp
import flask
from flask import request, send_file
from app import app
from models.user_model import user_model
from models.auth_model import auth_model
import os
from datetime import datetime
obj = user_model()
auth = auth_model()


@app.route("/user/all", methods = ["GET"]) #Get All Users
# The endpoint for token_auth() is automatically getting calculated in the auth_model.token_auth() method
# @auth.token_auth()
def all_users(): 
    return obj.all_user_model()

@app.route("/user/add", methods = ["POST"]) # Add A Single User
def add_user():
    return obj.add_user_model(request.form)

@app.route("/user/addmultiple", methods = ["POST"]) # Add Multiple Users
def add_multiple_users():
    return obj.add_multiple_users_model(request.json)

@app.route("/user/delete/<id>", methods = ["DELETE"]) # Delete User By ID
def delete_user(id):
    return obj.delete_user_model(id)

@app.route("/user/update", methods = ["PUT"]) # Update User Data
def update_user():
    return obj.update_user_model(request.form)

@app.route("/user/patch", methods = ["PATCH"]) # Update Specific User Data
def patch_user():
    return obj.patch_user_model(request.form)

@app.route("/user/page/<pno>/limit/<limit>", methods = ["GET"]) # Limit Response by Specific Page No & No. of Results
def pagination(pno, limit):
    return obj.pagination_model(pno, limit)

@app.route("/user/<uid>/file/upload", methods = ["PATCH"])
def upload_file(uid):
    file = request.files['file']
    new_filename =  str(datetime.now().timestamp()).replace(".", "") # Generating Unique Name for the File
    split_filename = file.filename.split(".") # Spliting ORIGINAL Filename to Seperate Extenstion
    ext_pos = len(split_filename)-1 # Calculating last index of the list we got by splitting the filename
    ext = split_filename[ext_pos] # Using last index To get the file extension
    db_path = f"uploads/{new_filename}.{ext}"
    file.save(f"uploads/{new_filename}.{ext}")
    return obj.upload_file_model(uid, db_path)

@app.route("/user/file/<uid>", methods =["GET"])
def get_file(uid):
    data = obj.get_file_path_model(uid)
    root_dir = os.path.dirname(app.instance_path)
    return send_file(f"{root_dir}{data['payload'][0]['file']}")

@app.route("/uploads/<filename>", methods = ["GET"])
def get_file_controller(filename):
    return send_file(f"uploads/{filename}")

@app.route("/user/login")
def user_login():
    auth_data = request.authorization
    return obj.user_login_model(auth_data['username'], auth_data['password'])

@app.route("/home")
def home():
    return "This is a home page"