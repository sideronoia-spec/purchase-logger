from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["daily_expense"]
collection = db["expenses"]

@app.route("/", methods=["GET", "POST"])
def index():
    today = datetime.now().strftime("%Y-%m-%d")

    if request.method == "POST":
        date = request.form["date"]
        amount = float(request.form["amount"])

        collection.update_one(
            {"date": date},
            {"$set": {"amount": amount}},
            upsert=True
        )
        return redirect("/")

    expenses = list(collection.find().sort("date", -1))

    total = 0
    if expenses:
        total = sum(e["amount"] for e in expenses)

    return render_template("index.html",
                           today=today,
                           expenses=expenses,
                           total=total)
@app.route("/delete/<id>")
def delete(id):
    collection.delete_one({"_id": ObjectId(id)})
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
