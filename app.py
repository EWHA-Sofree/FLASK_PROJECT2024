from flask import Flask, render_template, request
import sys
application = Flask(__name__)

@application.route("/")
def hello():
  return render_template("index.html")

@application.route("/category")
def view_category():
  return render_template("category.html")

@application.route("/best_review")
def view_review():
  return render_template("best_review.html")

@application.route("/mypage")
def view_mypage():
  return render_template("mypage.html")

@application.route("/submit_item")
def reg_item_submit():
    return render_template("reg_items.html")

@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
  data=request.form
  return render_template("submit_item_result.html", data=data)
