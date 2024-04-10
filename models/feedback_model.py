from datetime import datetime, timedelta
import mysql.connector
import json
from flask import make_response, jsonify
import jwt
from configs.config import dbconfig
from textblob import TextBlob  # Import TextBlob for sentiment analysis

from models.user_model import user_model

class feedback_model:
    def __init__(self):
        self.con = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
        self.con.autocommit=True #Every future query will automatically get committed to the MySQL DB.
        #self.user_model = user_model()
        self.cur = self.con.cursor(dictionary=True) #Get Data in Dictionary format

    def analyze_sentiment(self, text):
        analysis = TextBlob(text)
        # Get sentiment polarity (-1 to 1, where -1 is negative, 0 is neutral, and 1 is positive)
        polarity = analysis.polarity
        subjectivity = analysis.subjectivity
        
        if polarity > 0:
            return "positive"
        elif polarity == 0:
            return "neutral"
        else:
            return "negative"
        
    def all_feedback_model(self): # Get All Feedbacks
        self.cur.execute("SELECT * FROM feedback")
        result = self.cur.fetchall()
        if len(result)>0:
            return {"payload":result}
            # return make_response({"payload":result},200)
        else:
            return "No Data Found"
        
    def add_feedback_model(self, data): # Provide a single feedback with provider name & text
        self.cur.execute(f"INSERT INTO feedback(feedback_provider, feedback_text) VALUES('{data['feedback_provider']}', '{data['feedback_text']}')")
        return make_response({"message":"FEEDBACK_SUBMITTED_SUCCESSFULLY"},201)

    def update_feedback_model(self, data): #Update the feedback text & provider with a specific id
        self.cur.execute(f"UPDATE feedback SET feedback_provider='{data['feedback_provider']}', feedback_text='{data['feedback_text']}' WHERE id={data['id']}") #Update feedback provider, body with a specific id
        if self.cur.rowcount>0:
            return make_response({"message":"UPDATED_SUCCESSFULLY"},201)
        else:
            return make_response({"message":"NOTHING_TO_UPDATE"},204)

    def delete_feedback_model(self,id): # Delete feedback with a specific id
        self.cur.execute(f"DELETE FROM feedback WHERE id={id}")
        if self.cur.rowcount>0:
            return make_response({"message":"DELETED_SUCCESSFULLY"},202)
        else:
            return make_response({"message":"CONTACT_DEVELOPER"},500)
        
    def patch_feedback_model(self, data):
        qry = "UPDATE feedback SET "
        for key in data:
            if key!='id':
                qry += f"{key}='{data[key]}',"
        qry = qry[:-1] + f" WHERE id = {data['id']}"
        self.cur.execute(qry)
        if self.cur.rowcount>0:
            return make_response({"message":"UPDATED_SUCCESSFULLY"},201)
        else:
            return make_response({"message":"NOTHING_TO_UPDATE"},204)

    def pagination_model(self, pno, limit):
        pno = int(pno)
        limit = int(limit)
        start = (pno*limit)-limit
        qry = f"SELECT * FROM feedback LIMIT {start}, {limit}"
        self.cur.execute(qry)
        result = self.cur.fetchall()
        if len(result)>0:
            return make_response({"page":pno, "per_page":limit,"this_page":len(result), "payload":result})
        else:
            return make_response({"message":"No Data Found"}, 204)