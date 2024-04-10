from datetime import datetime, timedelta
import mysql.connector
import json
from flask import make_response, jsonify
import jwt
from configs.config import dbconfig

class user_model():
    def __init__(self):
        self.con = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
        self.con.autocommit=True #Every future query will automatically get committed to the MySQL DB.
        self.cur = self.con.cursor(dictionary=True) #Get Data in Dictionary format
        
    def all_user_model(self):
        self.cur.execute("SELECT * FROM users")
        result = self.cur.fetchall()
        if len(result)>0:
            return {"payload":result}
            # return make_response({"payload":result},200)
        else:
            return "No Data Found"
    
    def add_user_model(self,data):
        self.cur.execute(f"INSERT INTO users(name, email, phone, password) VALUES('{data['name']}', '{data['email']}', '{data['phone']}', '{data['password']}')")
        return make_response({"message":"CREATED_SUCCESSFULLY"},201)

    def delete_user_model(self,id):
        self.cur.execute(f"DELETE FROM users WHERE id={id}")
        if self.cur.rowcount>0:
            return make_response({"message":"DELETED_SUCCESSFULLY"},202)
        else:
            return make_response({"message":"CONTACT_DEVELOPER"},500)
        
    def update_user_model(self,data):
        self.cur.execute(f"UPDATE users SET name='{data['name']}', email='{data['email']}', phone='{data['phone']}', '{data['password']}' WHERE id={data['id']}")
        if self.cur.rowcount>0:
            return make_response({"message":"UPDATED_SUCCESSFULLY"},201)
        else:
            return make_response({"message":"NOTHING_TO_UPDATE"},204)

    def patch_user_model(self, data):
        qry = "UPDATE users SET "
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
        qry = f"SELECT * FROM users LIMIT {start}, {limit}"
        self.cur.execute(qry)
        result = self.cur.fetchall()
        if len(result)>0:
            return make_response({"page":pno, "per_page":limit,"this_page":len(result), "payload":result})
        else:
            return make_response({"message":"No Data Found"}, 204)
        
    def user_login_model(self, data): #username, password):
        self.cur.execute(f"SELECT id, name, email, phone, role_id FROM users WHERE email='{data['email']}' AND password='{data['password']}'")
        result = self.cur.fetchall()
        exptime = datetime.now() + timedelta(minutes=15)
        exp_epoc_time = int(exptime.timestamp())
        payload = {
            'payload':result[0],
            'exp':exp_epoc_time
        }
        jwt_token = jwt.encode(payload, 'prash', algorithm='HS256')
        print(jwt_token)
        return make_response({'token':jwt_token}, 200)
        # else:
        #     return make_response({"message":"NO SUCH USER"}, 204)
            