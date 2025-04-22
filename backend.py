from flask_pymongo import PyMongo
import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/medication_stock_db"
mongo = PyMongo(app)
db = mongo.db



def get_salesdaily():
    try:
        sales_daily = list(db.salesdaily.find({}, {'_id': 0}))
        if not sales_daily:
            return {"message": "No data found"}, 404
        return sales_daily
    except Exception as e:
        return {"error": str(e)}, 500



def get_salesweekly():
    try:
        sales_weekly = list(db.salesweekly.find({}, {'_id': 0}))
        if not sales_weekly:
            return {"message": "No data found"}, 404
        return sales_weekly
    except Exception as e:
        return {"error": str(e)}, 500
    
def get_salesmonthly():
    try:
        sales_monthly = list(db.salesmonthly.find({}, {'_id': 0}))
        if not sales_monthly:
            return {"message": "No data found"}, 404
        return sales_monthly
    except Exception as e:
        return {"error": str(e)}, 500
    

def get_salesdaily_by_state():
    try:
        sales_daily_by_state = list(db.salesdaily_by_state.find({}, {'_id': 0}))
        if not sales_daily_by_state:
            return {"message": "No data found"}, 404
        return sales_daily_by_state
    except Exception as e:
        return {"error": str(e)}, 500

def get_salesweekly_by_state():
    try:
        sales_weekly_by_state = list(db.salesweekly_by_state.find({}, {'_id': 0}))
        if not sales_weekly_by_state:
            return {"message": "No data found"}, 404
        return sales_weekly_by_state
    except Exception as e:
        return {"error": str(e)}, 500
    

def get_salesmonthly_by_state():
    try:
        sales_monthly_by_state = list(db.salesmonthly_by_state.find({}, {'_id': 0}))
        if not sales_monthly_by_state:
            return {"message": "No data found"}, 404
        return sales_monthly_by_state
    except Exception as e:
        return {"error": str(e)}, 500
    

    

