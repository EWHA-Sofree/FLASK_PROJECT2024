from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from database import DBhandler 
import hashlib
import sys

application = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"

DB = DBhandler()

@application.route("/")
def hello():
    return render_template("main.html")

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
  if 'id' in session:   # 로그인 한 경우에만 마이페이지 화면으로 이동
    user_info = DB.get_userinfo_byid(session['id'])
    return render_template("mypage.html",info=user_info)
  else:
    flash("로그인이 필요한 서비스입니다!")
    return redirect(url_for('login'))

@application.route("/reg_item")
def reg_item():
    return render_template("reg_item.html")

@application.route("/reg_review/<name>/")
def reg_review(name):
    if "id" not in session:
        flash("리뷰 등록 시 로그인이 필요합니다.")
        return redirect(url_for("login"))
    return render_template("reg_review.html", name=name)
  
@application.route("/reg_review_submit", methods=['POST'])
def reg_review_submit():
    image_file=request.files["file"]
    image_file.save("static/image/{}".format(image_file.filename))
    data=request.form
    user_id = session.get('id')
    data_with_user = {
        **data,
        "user_id": user_id
    }
    review_id = DB.reg_review(data_with_user, image_file.filename)
    return redirect(url_for('view_review_detail', review_id=review_id))

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
    
if __name__ == "__main__":
    application.run(host="0.0.0.0")


@application.route("/list")
def view_list():
    
    page = request.args.get("page", 0, type=int)
    per_page = 8
    per_row = 4
    row_count=int(per_page/per_row)

    start_idx = per_page * page
    end_idx = per_page * (page + 1)

    data = DB.get_items()
    
    item_counts = len(data)
    data = list(data.items())[start_idx:end_idx]

    rows = []
    for i in range(row_count):
        start_idx = i * per_row
        end_idx = start_idx + per_row
        rows.append(dict(data[start_idx:end_idx]))

    return render_template(
        "list.html",
        datas=data,
        rows=rows,
        limit=per_page,
        page=page,
        page_count=(item_counts + per_page - 1) // per_page,
        total=item_counts,
    )
    
@application.route("/view_detail/<name>/")
def view_item_detail(name):
    print("###name:", name)
    data=DB.get_item_byname(str(name))
    print("####data:", data)
    return render_template("item_detail.html", name=name, data=data)

@application.route("/view_review_detail/<review_id>")
def view_review_detail(review_id):
    review_info = DB.get_review_byID(review_id)    
    if not review_info:
        return "리뷰를 찾을 수 없습니다.", 404
    return render_template("review_detail.html", data=review_info)

@application.route('/show_heart/<name>/', methods=['GET'])
def show_heart(name):
 my_heart = DB.get_heart_byname(session['id'],name)
 return jsonify({'my_heart': my_heart})

@application.route('/like/<name>/', methods=['POST'])
def like(name):
 my_heart = DB.update_heart(session['id'],'Y',name)
 return jsonify({'msg': '위시리스트에 추가했습니다!'})

@application.route('/unlike/<name>/', methods=['POST'])
def unlike(name):
 my_heart = DB.update_heart(session['id'],'N',name)
 return jsonify({'msg': '위시리스트에서 삭제했습니다!'})