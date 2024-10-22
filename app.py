from flask import Flask, render_template, request
import sys

application = Flask(__name__)


@application.route("/")
def hello():
<<<<<<< HEAD
    return render_template("index_ewhamarket.html") # 여기 바꿈


@application.route("/category")
def view_category():
  return render_template("category.html")

@application.route("/best_review")
def view_review():
  return render_template("best_review.html")

@application.route("/mypage")
def view_mypage():
  return render_template("mypage.html")

@application.route("/reg_items") #판매하기
def reg_item():
    return render_template("reg_items.html")

@application.route("/login")
def reg_review():
    return render_template("login.html")

@application.route("/submit_item_post", methods=["POST"])
def reg_item_submit_post():
    image_file = request.files["file"]
    image_file.save("static/image/{}".format(image_file.filename))
    data = request.form
    
    print(f"Form data: {data}")
    
    return render_template(
        "submit_item_result.html",
        data=data,
        img_path="static/image/{}".format(image_file.filename),
    )


if __name__ == "__main__":
    application.run(host="0.0.0.0")
=======
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

@application.route("/reg_items")
def reg_item():
  return render_template("reg_items.html")

@application.route("/submit_item")
def reg_item_submit():
    name=request.args.get("name")
    seller=request.args.get("seller")
    price=request.args.get("price")
    category=request.args.get("category")
    print(name,seller,price,category)
    #return render_template("reg_item.html")
>>>>>>> 516e640e9cd898f8feb54c431bebde6363fe91b3
