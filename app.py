from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler 
import hashlib
import sys

application = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"

DB = DBhandler()

@application.route("/")
def hello():
    return render_template("main.html")  # 기존 index.html을 main.html로 변경

@application.route("/category")
def view_category_default():
    return render_template("category.html", category_name="stationery")

@application.route("/category/<category_name>")
def view_category(category_name):
    return render_template("category.html", category_name=category_name)

@application.route("/reviews_list")
def view_review_list():
  return render_template("/reviews_list.html")

@application.route("/mypage")
def view_mypage():
  return render_template("mypage.html")

@application.route("/reg_item")
def reg_item():
    return render_template("reg_item.html")
  
@application.route("/reg_review", methods=['POST'])
def reg_review():
    data=request.form
    image_file=request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))
    DB.reg_review(data, image_file.filename)
    return redirect(url_for('review_detail'))

@application.route("/reg_review_init/<name>/")
def reg_review_init(name):
    return render_template("reg_review.html", name=name)

@application.route("/login")
def login():
    return render_template("login.html")

@application.route("/login_confirm", methods=['POST']) 
def login_user():
    id_=request.form['id']
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id_,pw_hash):
        session['id']=id_
        return redirect(url_for('hello'))
    else:
        flash("로그인 실패! 올바른 아이디와 비밀번호를 입력하세요.")
        return render_template("login.html")
  
@application.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")

@application.route("/signup_post", methods=['POST']) 
def register_user():
    # 요청 메서드와 폼 데이터 확인
    print("Request method:", request.method)
    data = request.form.to_dict()
    print("Received form data:", data)  # 전체 데이터를 딕셔너리로 출력

    # 요청 메서드가 POST가 아니면 오류 반환
    if request.method != 'POST':
        print("Error: Not a POST request")
        return "Request method is not POST", 400

    # 비밀번호 필드가 있는지 확인
    try:
        pw = data['pw']
        print("Password field:", pw)
    except KeyError:
        print("Error: 'pw' field is missing")  # 'pw' 필드 누락 시 오류 메시지
        flash("비밀번호가 입력되지 않았습니다.")
        return render_template("sign_up.html")

    # 비밀번호 해시 처리
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    
    # 데이터베이스에 사용자 등록 시도
    if DB.insert_user(data, pw_hash):
        return render_template("login.html") 
    else:
        flash("User ID already exists!")
        return render_template("sign_up.html")
    
@application.route("/logout") 
def logout_user():
    session.clear()
    return redirect(url_for('hello'))

@application.route("/submit_item_post", methods=["POST"])
def reg_item_submit_post():
    image_file = request.files["file"]
    image_file.save("static/image/{}".format(image_file.filename))
    data = request.form
    DB.insert_item(data['name'], data, image_file.filename)
        
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
        "user_id": "예지",  # 작성자의 아이디
        "product_name": "[사계절 햇빛차단🌟] 시어링 팔토시 핸드워머",  # 제품 이름
        "rating": 4,  # 1~5의 별점
        "review_text": "소재가 보들보들해서 기분이 좋고 마감도 탄탄해요!\n여름에 반팔 입거나 봄가을 환절기 때 잘 착용할 것 같아요 ^ㅇ^",
        "review_image": "image/sample.jpg"  # 미리보기용 샘플 리뷰 이미지 경로 (static 경로 지정 시 url_for 사용)
    }
    
    return render_template("review_detail.html", data=review_data)

if __name__ == "__main__":
    application.run(host="0.0.0.0")


@application.route("/list")
def view_list():
    
    page=request.args.get("page", 0, type=int)
    
    per_page=8 # item count to display per page
    per_row=4 # item count to display per row
    row_count=int(per_page/per_row)
    
    start_idx=per_page*page
    end_idx=per_page*(page+1)
   
    data=DB.get_items() #read the table

    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count=len(data)
    
    for i in range(row_count): #last row
        if (i==row_count-1) and (tot_count%per_row != 0):
            locals()['data_{}'.format(i)]=dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)]=dict(list(data.items())[i*per_row:(i+1)*per_row])
    
    return render_template(
        "list.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page = page,
        page_count = int((item_counts/per_page)+1),
        total=item_counts
    )
    
    
@application.route("/view_detail/<name>/")
def view_item_detail(name):
    print("###name:", name)
    data=DB.get_item_byname(str(name))
    print("####data:", data)
    return render_template("item_detail.html", name=name, data=data)
