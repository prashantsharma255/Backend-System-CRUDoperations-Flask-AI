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
# @auth.token_auth() # The endpoint for token_auth() is automatically getting calculated in the auth_model.token_auth() method
def all_users(): 
    return obj.all_user_model()

@app.route("/user/add", methods = ["POST"]) # Add A Single User
# @auth.token_auth()
def add_user():
    return obj.add_user_model(request.form)

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

@app.route("/user/login", methods = ["POST"])
def user_login():
    #auth_data = request.authorization
    return obj.user_login_model(request.form)#auth_data['username'], auth_data['password'])