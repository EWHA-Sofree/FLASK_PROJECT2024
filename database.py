# 데이터베이스 연결하는 스크립트 
import pyrebase
import json

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f: 
            config=json.load(f )
        firebase = pyrebase.initialize_app(config) 
        self.db = firebase.database()
        
    def insert_item(self, name, data, img_path): 
        item_info ={
            "name": data['name'],
            "seller": data['seller'], 
            "price": int(data['price']),
            "info": data['info'], 
            "category": data['category'],
            "img_path": img_path, 
            "timestamp":data['timestamp'], 
            "user_id":data['user_id'], 
            "user_nickname":data['user_nickname']
        }
        # Firebase에 데이터 저장 (랜덤 키 사용)
        self.db.child("item").push(item_info)       # push()를 사용하면 고유 ID 생성
        #print(f"Data saved successfully: {item_info}")
        return True
    
    def insert_user(self, data, pw): 
        user_info = {
            "id": data['id'], 
            "pw": pw,
            "name": data.get('username', ''), 
            "nickname": data.get('nickname', ''),
            "email": data.get('email', ''),
            "phone": data.get('phone', '')
        }
        if self.user_duplicate_check(data['id']): 
            self.db.child("user").push(user_info) 
            return True
        else:
            return False

    def user_duplicate_check(self, username): 
        users = self.db.child("user").get()
        #print("Existing users:", users.val())

        # 첫 번째 사용자일 경우 또는 사용자가 없을 경우 True 반환
        if str(users.val()) == "None":
            return True
        else:  
            # 이미 존재하는 사용자 중에서 중복 체크
            for res in users.each(): 
                value = res.val()
                if value['id'] == username: 
                    return False
            return True
    
    def find_user(self, id_, pw_):
        users = self.db.child("user").get() 
        target_value=[]
        for res in users.each():
            value = res.val()

            if value['id'] == id_ and value['pw'] == pw_:
                return True 
        return False

    def get_items(self):
        items=self.db.child("item").get()
        return items
    
    def get_item_bykey(self, key):
        items = self.db.child("item").get()
        if not items.each():
            return None  # 데이터가 없을 경우 None 반환

        # key와 매칭되는 값 찾기
        for res in items.each():
            if res.key() == key:
                return res.val()  # 매칭된 값 반환

        return None  # 매칭되는 값이 없으면 None 반환

    
    def get_items_bycategory(self, cate):
        tmps = self.db.child("item").get()
        target_value=[]
        target_key=[]
        for res in tmps.each():
            value = res.val()
            key_value = res.key()
            
            if value['category'] == cate:
                target_value.append(value)
                target_key.append(key_value)
        #print("######target_value", target_value)
        items={}
        
        for k,v in zip(target_key, target_value):
            items[k]=v
        
        return items
    
    def reg_review(self, data, img_path, purchase_id):
        review_info = {
            "name": data['name'],
            "rate": int(data['reviewStar']),
            "review": data['reviewContents'],
            "img_path": img_path,
            "user_id": data['user_id'],
            "user_nickname": data['user_nickname'],
            "timestamp": data['timestamp'],
            "item_id": data['item_id'],
            "purchase_id": purchase_id
        }
        
        # 리뷰 저장
        result = self.db.child("review").push(review_info)
        
        # purchases 하위 데이터 업데이트
        self.db.child("purchases").child(data['user_id']).child(purchase_id).update({
            "review_written": True
        })

        return result['name']
    
    def get_review_byID(self, review_id):
        review = self.db.child("review").child(review_id).get()
        return review.val() if review else None
            
    def get_reviews_by_name(self, name):
        reviews = self.db.child("review").order_by_child("name").equal_to(name).get()
        if not reviews or not reviews.each():
            return []
        return [review.val() for review in reviews.each()]
    
    def get_reviews(self):
        reviews=self.db.child("review").get().val()
        return reviews if reviews else {}

    def get_heart_byname(self, uid, name):
        hearts = self.db.child("heart").child(uid).get()
        target_value=""
        if hearts.val() == None:
            return target_value

        for res in hearts.each():
            key_value = res.key()
            
            if key_value == name:
                target_value=res.val()
        return target_value
    
    def update_heart(self, user_id, isHeart, item, timestamp):
        heart_info ={
            "interested": isHeart
        }
        if timestamp is not None:
            heart_info["timestamp"] = timestamp
        else:
            heart_info["timestamp"] = None
            
        self.db.child("heart").child(user_id).child(item).set(heart_info)
        return True
    
    def get_userinfo_byid(self, user_id):
        users = self.db.child("user").get()
        #print("Fetched users:", users.val())  # Firebase에서 가져온 전체 데이터 출력

        for user in users.each():
            #print("Checking user:", user.val())  # 각 사용자 데이터를 출력
            if user.val().get("id") == user_id:
                user_data = {  # **추가된 필드 반환**
                    "id": user.val().get("id"),
                    "name": user.val().get("name", ""),
                    "nickname": user.val().get("nickname", ""),  # **닉네임 반환**
                    "email": user.val().get("email", ""),        # **이메일 반환**
                    "phone": user.val().get("phone", "")         # **전화번호 반환**
                }
                #print("Matched user data:", user_data)  # 매칭된 사용자 데이터 출력
                return user_data
        return None
    
    def get_wishlist_byid(self, user_id):
        user_data = self.db.child("heart").child(user_id).get()
                  
        if user_data.val() is None: return {}

        wishlist = []

        user_data_dict = user_data.val()  # 데이터를 딕셔너리로 변환
        if user_data_dict:  
            for key, value in user_data_dict.items():
                if value.get("interested") == "Y":
                    wishlist.append({"item": key, "timestamp": value.get("timestamp")})
        
        return wishlist

    def get_purchase_by_purchaseid(self, user_id, purchase_id):
        purchase = self.db.child("purchases").child(user_id).child(purchase_id).get()
        return purchase if purchase else None
    
    def get_purchases_byid(self, user_id):
        purchases = self.db.child("purchases").child(user_id).get()
        return purchases if purchases else None

    def add_purchase(self, user_id, item_id, timestamp):
        purchase_data = {
            "item_id": item_id,
            "timestamp": timestamp,
            "review_written": False
        }
        try:
            result = self.db.child("purchases").child(user_id).push(purchase_data)
            return result['name']
        except Exception as e:
            print("Firebase 데이터 저장 중 오류 발생:", e)
            return None