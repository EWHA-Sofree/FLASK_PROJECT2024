from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from database import DBhandler 
import hashlib
import sys
import math
from datetime import datetime, timezone

application = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"

DB = DBhandler()

if __name__ == "__main__":
    application.run(host="0.0.0.0")

@application.route("/")
def hello():
    return render_template("main.html")

@application.route("/reviews_list")
def view_reviews_list():
    page = request.args.get("page", 0, type=int)
    per_page = 8  # item count to display per page
    per_row = 4  # item count to display per row
    row_count = int(per_page / per_row)
    start_idx = per_page * (page)
    end_idx = per_page * (page+1)
    
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
    user_id = session.get('id')

    if not user_id:
        flash("로그인이 필요한 서비스입니다.")
        return redirect(url_for('login'))

    # 사용자 정보 가져오기
    user_info = DB.get_userinfo_byid(user_id)

    if not user_info:
        flash("사용자 정보를 찾을 수 없습니다.")
        return redirect(url_for('hello'))

    # 데이터 가져오기
    purchases, total_purchase = get_purchased_items(user_id, limit=4)
    wishlist, total_wish = get_wishlist_items(user_id, limit=4)
    
    return render_template(
        'mypage.html',
        wishes=wishlist,
        purchases=purchases,
        total_wish=total_wish,
        total_purchase=total_purchase,
        info=user_info
    )

@application.route('/wishlist')
def wishlist():
    user_id = session.get('id')
    page = request.args.get("page", 0, type=int)
    per_page = 8
    per_row = 4  # item count to display per row
    row_count = int(per_page / per_row)
    start_idx = per_page * (page)
    end_idx = per_page * (page+1)

    # 위시리스트 데이터 가져오기
    data, total = get_wishlist_items(user_id)

    data = dict(list(data.items())[start_idx:end_idx])  # 슬라이싱 안전하게 처리
    tot_count = len(data)
    
    for i in range(row_count):  # 행 별로 데이터 생성
        if (i == row_count - 1) and (tot_count % per_row != 0):
            locals()[f'data_{i}'] = dict(list(data.items())[i * per_row:])
        else:
            locals()[f'data_{i}'] = dict(list(data.items())[i * per_row:(i + 1) * per_row])
            
    return render_template(
        'wishlist.html',
        wish=data,
        row1=locals().get('data_0', {}).items(),
        row2=locals().get('data_1', {}).items(),
        limit=per_page,
        page=page,
        page_count=(total + per_page - 1) // per_page,  # 페이지 수 계산 보정
        total=total
    )

@application.route("/purchase_history")
def purchase_history():
    user_id = session.get('id')
    page = request.args.get("page", 0, type=int)
    per_page = 8
    per_row = 4  # item count to display per row
    row_count = int(per_page / per_row)
    start_idx = per_page * (page)  # 페이지 계산 수정
    end_idx = per_page * (page+1)

    # 위시리스트 데이터 가져오기
    data, total = get_purchased_items(user_id)

    data = dict(list(data.items())[start_idx:end_idx])  # 슬라이싱 안전하게 처리
    tot_count = len(data)
    
    for i in range(row_count):  # 행 별로 데이터 생성
        if (i == row_count - 1) and (tot_count % per_row != 0):
            locals()[f'data_{i}'] = dict(list(data.items())[i * per_row:])
        else:
            locals()[f'data_{i}'] = dict(list(data.items())[i * per_row:(i + 1) * per_row])
            
    return render_template(
        'purchase_history.html',
        purchases=data,
        row1=locals().get('data_0', {}).items(),
        row2=locals().get('data_1', {}).items(),
        limit=per_page,
        page=page,
        page_count=(total + per_page - 1) // per_page,  # 페이지 수 계산 보정
        total=total
    )
    
@application.route('/sales_history')
def sales_history():
    user_id = session.get('id')  # 현재 로그인한 사용자 ID 가져오기

    return render_template('sales_history.html')
    
@application.route('/reg_item')
def reg_item():
    # 현재 로그인한 사용자 ID 가져오기
    user_id = session.get('id')  # 세션에서 사용자 ID 가져오기

    if not user_id:
        flash("로그인이 필요한 서비스입니다.")
        return redirect(url_for('login'))  # 로그인 페이지로 리다이렉트

    # 데이터베이스에서 사용자 정보 가져오기
    user_info = DBhandler().get_userinfo_byid(user_id)
    print("User info passed to template:", user_info)  # 전달 데이터 디버깅
    if not user_info:
        flash("사용자 정보를 찾을 수 없습니다.")
        return redirect(url_for('index'))  # 메인 페이지로 리다이렉트

    print("User info:", user_info)

    return render_template('reg_item.html', info=user_info)
  

@application.route("/reg_review/<purchase_id>/")
def reg_review(purchase_id):
    if "id" not in session:
        flash("리뷰 등록 시 로그인이 필요합니다.")
        return redirect(url_for("login"))

    user_id = session.get('id')
    
    # 구매 정보 가져오기
    purchase = DB.get_purchase_by_purchaseid(user_id, purchase_id).val()
    if not purchase:
        flash("유효하지 않은 구매내역입니다.")
        return redirect(url_for("purchase_history"))

    # item_id 가져오기
    item_id = purchase.get("item_id")
    if not item_id:
        flash("구매내역에 아이템 정보가 없습니다.")
        return redirect(url_for("purchase_history"))

    # 아이템 정보 가져오기
    item = DB.get_item_bykey(item_id)
    if not item:
        flash("상품 정보를 찾을 수 없습니다.")
        return redirect(url_for("purchase_history"))
    
    print(f"Purchase: {purchase}")
    print(f"Item: {item}")

    return render_template("reg_review.html", purchase=purchase, item=item)
  
@application.route("/reg_review_submit", methods=['POST'])
def reg_review_submit():
    image_file=request.files["file"]
    image_file.save("static/image/{}".format(image_file.filename))
    
    user_id = session.get('id')
    user = DB.get_userinfo_byid(user_id)
    data = request.form
    purchase_id = data.get('purchase_id')
    
    timestamp = datetime.now(timezone.utc).isoformat()
    
    data_with_user = {
        **data,
        "user_id": user_id,
        "user_nickname": user.get('nickname'), 
        "timestamp": timestamp
    }
    review_id = DB.reg_review(data_with_user, image_file.filename, purchase_id)
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
    print("Form data received:", request.form.to_dict())
    data = request.form.to_dict()
    
    required_fields = ['id', 'pw', 'username', 'nickname', 'email', 'phone1', 'phone2', 'phone3']
    for field in required_fields:
        if field not in data or not data[field].strip():
            print(f"Error: '{field}' field is missing or empty")
            flash(f"'{field}'는 필수 입력 항목입니다.")
            return render_template("sign_up.html")

    # 전화번호 병합
    phone = f"{data['phone1']}-{data['phone2']}-{data['phone3']}"

    # 비밀번호 해시 처리
    pw = data['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    # 데이터베이스에 사용자 등록 정보 생성
    user_info = {
        "id": data['id'],
        "pw": pw_hash,
        "username": data['username'],
        "nickname": data['nickname'],
        "email": data['email'],
        "phone": phone  # 병합된 전화번호 추가
    }
    
    # 데이터베이스에 사용자 등록 시도
    if DB.insert_user(user_info, pw_hash):
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
    data_prev = request.form.to_dict()  # ImmutableMultiDict를 딕셔너리로 변환
    
    user_id = session.get('id')
    user = DB.get_userinfo_byid(user_id)
    timestamp = datetime.now(timezone.utc).isoformat()
    
    data = {
        **data_prev,
        "img_path": image_file.filename, 
        "user_id": user_id,
        "user_nickname": user.get('nickname'), 
        "timestamp": timestamp
    }
    
    DB.insert_item(data['name'], data, image_file.filename)
        
    #print(f"Form data: {data}")
    
    return render_template(
        "item_detail.html", data=data)
    
    
@application.route("/list")
def view_list():

    page=request.args.get("page", 0, type=int)
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
 my_heart = DB.get_heart_byname(session['id'], name)
 return jsonify({'my_heart': my_heart})

@application.route('/like/<name>/', methods=['POST'])
def like(name):
    timestamp = datetime.now(timezone.utc).isoformat()
    my_heart = DB.update_heart(session['id'],'Y', name, timestamp=timestamp)
    return jsonify({'msg': '위시리스트에 추가했습니다!'})

@application.route('/unlike/<name>/', methods=['POST'])
def unlike(name):
 my_heart = DB.update_heart(session['id'],'N', name, timestamp=None)
 return jsonify({'msg': '위시리스트에서 삭제했습니다!'})

@application.route('/buy/<item_id>/', methods=['POST'])
def buy_item(item_id):
    user_id = session.get('id')
    if not user_id:
        return jsonify({'msg': '로그인이 필요합니다.'}), 403

    timestamp = datetime.now(timezone.utc).isoformat()

    purchase_id = DB.add_purchase(user_id, item_id, timestamp)
    if not purchase_id:
        return jsonify({'msg': '구매내역 저장에 실패했습니다.'}), 500

    return jsonify({
        'msg': '구매가 완료되었습니다.',
        'purchase_id': purchase_id
    }), 200

def get_purchased_items(user_id, limit=None):
    # Firebase에서 사용자 구매내역 가져오기
    raw_data = DB.get_purchases_byid(user_id).val()  # {purchase_id: {item_id: ..., review_written: ..., timestamp: ...}}
    if not raw_data:
        return {}, 0

    # Firebase에서 모든 아이템 데이터 가져오기
    all_items = DB.get_items().val()  # {item_id: {name: ..., img_path: ...}}
    if not all_items:
        return {}, 0

    filtered_data = {}

    # raw_data를 순회하여 item_id 기준으로 필터링
    for purchase_id, purchase_info in raw_data.items():
        item_id = purchase_info.get("item_id")  # value에서 item_id 추출
        if item_id in all_items:  # item_id가 all_items에 존재할 경우만 처리
            filtered_data[purchase_id] = {
                "item_id": item_id,
                "item_name": all_items[item_id].get("name", "Unknown"),
                "item_image": all_items[item_id].get("img_path", "default.png"),
                "review_written": purchase_info.get("review_written", False),
                "timestamp": purchase_info.get("timestamp", "Unknown")
            }

    # 최신순 정렬
    sorted_data = dict(sorted(filtered_data.items(), key=lambda x: x[1]["timestamp"], reverse=True))

    # 제한된 개수 반환
    if limit:
        sorted_data = dict(list(sorted_data.items())[:limit])

    return sorted_data, len(filtered_data)

def get_wishlist_items(user_id, limit=None):
    """
    사용자 ID를 기반으로 위시리스트 데이터를 필터링하여 반환
    :param user_id: 사용자 ID
    :return: 위시리스트 데이터 딕셔너리와 총 개수
    """
    raw_data = DB.get_wishlist_byid(user_id)
    if not raw_data:
        return {}, 0

    all_items = DB.get_items().val()
    filtered_data = {}

    # 위시리스트 필터링
    for entry in raw_data:
        item_id = entry.get("item")
        if item_id in all_items:
            filtered_data[item_id] = {
                "item_name": all_items[item_id].get("name", "Unknown"),
                "item_seller": all_items[item_id].get("seller", "Unknown"),
                "item_image": all_items[item_id].get("img_path", "default.png"),
                "timestamp": entry.get("timestamp")
            }

    # 최신순 정렬
    sorted_data = dict(sorted(filtered_data.items(), key=lambda x: x[1]["timestamp"], reverse=True))

    # 제한된 개수 반환
    if limit:
        sorted_data = dict(list(sorted_data.items())[:limit])

    return sorted_data, len(filtered_data)

@application.route("/check_duplicate", methods=["POST"])
def check_duplicate():
    data = request.json  # 프론트엔드에서 JSON 형식으로 데이터 받음
    username = data.get("id")  # 입력된 아이디 가져오기

    if not username:
        return jsonify({"message": "아이디를 입력하세요.", "status": "error"}), 400

    # 데이터베이스에서 중복 확인
    if DB.user_duplicate_check(username):  # True이면 중복되지 않음
        return jsonify({"message": "사용할 수 있는 아이디입니다.", "status": "success"})
    else:
        return jsonify({"message": "사용할 수 없는 아이디입니다.", "status": "error"}), 400

