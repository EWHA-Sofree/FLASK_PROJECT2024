from flask import Flask, render_template, request
import sys

application = Flask(__name__)


@application.route("/")
def hello():
    return render_template("main.html")  # 기존 index.html을 main.html로 변경

@application.route("/category")
def view_category_default():
    return render_template("category.html", category_name="stationery")

@application.route("/category/<category_name>")
def view_category(category_name):
    return render_template("category.html", category_name=category_name)
  
@application.route("/item_detail")
def view_item_detail():
    return render_template("item_detail.html")

@application.route("/reviews_list")
def view_review_list():
  return render_template("/reviews_list.html")

@application.route("/mypage")
def view_mypage():
  return render_template("mypage.html")

@application.route("/reg_item") #판매하기
def reg_item():
    return render_template("reg_item.html")
  
@application.route("/reg_review")
def reg_review():
    return render_template("reg_review.html")

@application.route("/login")
def log_in():
    return render_template("login.html")
  
@application.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")

@application.route("/submit_item_post", methods=["POST"])
def reg_item_submit_post():
    image_file = request.files["file"]
    image_file.save("static/image/{}".format(image_file.filename))
    data = request.form
    
    print(f"Form data: {data}")
    
    return render_template(
        "item_detail.html",
        data=data,
        img_path="static/image/{}".format(image_file.filename),
    )
    
#상품 상세, 리뷰 상세 페이지 주소로 접근 가능하게 만든 미리보기 함수
@application.route("/item_preview")
def item_preview():
    # 임시 미리보기 상품상세 데이터
    data = {
        "name": "샘플 상품",
        "seller": "미리보기 판매자",
        "category": "샘플 카테고리",
        "price": "5000",
        "info": "이 상품은 미리보기를 위해 표시된 샘플 데이터입니다."
    }
    img_path = "static/image/sample.jpg"  # 미리보기용 샘플 이미지 경로
    
    return render_template("item_detail.html", data=data, img_path=img_path)
  
@application.route("/review_preview")
def review_preview():
    # 임시 미리보기 리뷰 데이터
    review_data = {
        "product_name": "샘플 상품",
        "rating": 4,  # 1~5의 별점
        "review_text": "이 상품은 정말 훌륭합니다! 품질도 좋고 배송도 빨랐습니다.",
        "review_image": "static/image/sample.jpg"  # 미리보기용 샘플 리뷰 이미지 경로
    }
    
    return render_template("review_detail.html", data=review_data)


if __name__ == "__main__":
    application.run(host="0.0.0.0")
