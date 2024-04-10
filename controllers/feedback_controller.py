from crypt import methods
import imp
import flask
from flask import request, send_file
from app import app
import os
from datetime import datetime
from app import app

from models.user_model import user_model
from models.auth_model import auth_model
from models.feedback_model import feedback_model

obj = user_model()
auth = auth_model()
fdb = feedback_model()

@app.route("/feedback/all", methods = ["GET"]) #Get All User Feedback
# The endpoint for token_auth() is automatically getting calculated in the auth_model.token_auth() method
# @auth.token_auth()
def all_feedback(): 
    return fdb.all_feedback_model()

@app.route("/feedback/add", methods=["POST"]) #Submit a New Feedback
def add_feedback():
    # feedback_text = request.json.get("feedback_text")
    # sentiment = fdb.analyze_sentiment(feedback_text)
    # feedback_id = fdb.add_feedback_model(feedback_text, sentiment)
    # return {"message": "Feedback submitted successfully", "feedback_id": feedback_id}
    return fdb.add_feedback_model(request.form)

@app.route("/feedback/update", methods=["PUT"]) #Update the feedback text & provider with a specific id
def update_feedback():
    return fdb.update_feedback_model(request.form)

@app.route("/feedback/delete/<id>", methods=["DELETE"]) #Delete Feedback With A Specific ID
def delete_feedback(id):
    return fdb.delete_feedback_model(id)

@app.route("/feedback/patch", methods = ["PATCH"]) # Update Specific User Data
def patch_feedback():
    return fdb.patch_feedback_model(request.form)

@app.route("/feedback/page/<pno>/limit/<limit>", methods = ["GET"]) # Limit Response by Specific Page No & No. of Results
def pagination(pno, limit):
    return fdb.pagination_model(pno, limit)