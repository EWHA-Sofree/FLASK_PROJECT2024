from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from database import DBhandler 
import hashlib
import sys
import math

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
def view_reviews_list():
    page = request.args.get("page", 1, type=int)
    per_page = 8  # item count to display per page
    per_row = 4  # item count to display per row
    row_count = int(per_page / per_row)
    start_idx = per_page * (page - 1)  # 페이지 계산 수정
    end_idx = per_page * page
    
    # 데이터를 가져오고 None 체크
    data = DB.get_reviews() or {}  # None이면 빈 딕셔너리로 대체
    
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])  # 슬라이싱 안전하게 처리
    tot_count = len(data)
    
    for i in range(row_count):  # 행 별로 데이터 생성
        if (i == row_count - 1) and (tot_count % per_row != 0):
            locals()[f'data_{i}'] = dict(list(data.items())[i * per_row:])
        else:
            locals()[f'data_{i}'] = dict(list(data.items())[i * per_row:(i + 1) * per_row])
    
    return render_template(
        "reviews_list.html",
        reviews=data,
        row1=locals().get('data_0', {}).items(),
        row2=locals().get('data_1', {}).items(),
        limit=per_page,
        page=page,
        page_count=(item_counts + per_page - 1) // per_page,  # 페이지 수 계산 보정
        total=item_counts
    )

@application.route('/mypage')
def mypage():
    user_id = session.get('id')  # 세션에서 사용자 ID 가져오기

    if not user_id:
        flash("로그인이 필요한 서비스입니다.")
        return redirect(url_for('login'))  # 로그인 페이지로 리다이렉트

    # 데이터베이스에서 사용자 정보 가져오기
    user_info = DB.get_userinfo_byid(user_id)

    if not user_info:
        flash("사용자 정보를 찾을 수 없습니다.")
        return redirect(url_for('hello'))  # 메인 페이지로 리다이렉트

    wishlist = DB.get_wishlist_byid(user_id)  # 좋아요 상품 이름 리스트 가져오기

    if not wishlist:
        return render_template('mypage.html', items=[], info=user_info, total=0)

    all_items = DB.get_items()
    item_details = []

    # 위시리스트에 있는 상품 필터링
    for item_id in wishlist[:4]: 
        if item_id in all_items:
            item_details.append({"key": item_id, "value": all_items[item_id]}) 

    return render_template(
        'mypage.html',
        items=item_details,  
        total=len(wishlist),  # 전체 좋아요 상품 개수 전달
        info=user_info  # 사용자 정보
    )

@application.route("/wishlist")
def wishlist():
    page = request.args.get("page", 1, type=int)
    per_page = 8  # item count to display per page
    per_row = 4  # item count to display per row
    row_count = int(per_page / per_row)
    start_idx = per_page * (page - 1)  # 페이지 계산 수정
    end_idx = per_page * page

    user_id = session.get('id')
    all_items = DB.get_items()
    wishlist = DB.get_wishlist_byid(user_id)
    data = {}
    
    # 위시리스트에 있는 상품 필터링
    for item_id in wishlist: 
        if item_id in all_items:
                data[item_id]=all_items[item_id]
    
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])  # 슬라이싱 안전하게 처리
    tot_count = len(data)
    
    for i in range(row_count):  # 행 별로 데이터 생성
        if (i == row_count - 1) and (tot_count % per_row != 0):
            locals()[f'data_{i}'] = dict(list(data.items())[i * per_row:])
        else:
            locals()[f'data_{i}'] = dict(list(data.items())[i * per_row:(i + 1) * per_row])
    
    return render_template(
        "wishlist.html",
        wish=data,
        row1=locals().get('data_0', {}).items(),
        row2=locals().get('data_1', {}).items(),
        limit=per_page,
        page=page,
        page_count=(item_counts + per_page - 1) // per_page,  # 페이지 수 계산 보정
        total=item_counts
    )

@application.route("/purchase_history")
def purchase_history():
    return render_template("purchase_history.html")

@application.route("/sales_history")
def sales_history():
    return render_template("sales_history.html")

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

    # 필수 필드 확인
    required_fields = ['id', 'pw', 'nickname', 'email', 'phone']
    for field in required_fields:
        if field not in data or not data[field].strip():
            print(f"Error: '{field}' field is missing or empty")
            flash(f"'{field}'는 필수 입력 항목입니다.")
            return render_template("sign_up.html")

    # 비밀번호 해시 처리
    pw = data['pw']
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

    page=request.args.get("page", 1, type=int)
    category = request.args.get("category", "all")
    
    per_page=8  # item count to display per page
    per_row=4   # item count to display per row
    row_count=int(per_page/per_row)

    start_idx = page * per_page
    end_idx = (page+1) * per_page
    
    if category=="all":         #카테고리로 DB에서 데이터 받아오기
        data = DB.get_items()
    else: 
        data = DB.get_items_bycategory(category)
        
    data = dict(sorted(data.items(), key=lambda x: x[0], reverse=False))

    item_counts = len(data)
    
    if item_counts<=per_page:
        data = dict(list(data.items())[:item_counts])
    else :    
        data = dict(list(data.items())[start_idx:end_idx])
        
    tot_count = len(data)
    
    rows = []
    for i in range(row_count):
        start_idx = i * per_row
        end_idx = start_idx + per_row
        if i == row_count - 1 and tot_count % per_row != 0:
            rows.append(dict(list(data.items())[start_idx:]))
        else:
            rows.append(dict(list(data.items())[start_idx:end_idx]))

    return render_template(
        "list.html",
        datas=data.items(),
        rows=rows,
        limit=per_page,
        page=page,
        page_count=int(math.ceil(item_counts/per_page)),
        total=item_counts,
        category=category
    )
    
@application.route("/view_detail/<key>/")
def view_item_detail(key):
    data=DB.get_item_bykey(str(key))
    return render_template("item_detail.html", key=key, data=data)

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




@application.route('/dynamicurl/<varible_name>/')
def DynamicUrl(varible_name):
    return str(varible_name)

