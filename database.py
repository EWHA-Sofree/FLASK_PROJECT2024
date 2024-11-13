import pyrebase
import json

class DBhandler:
    def __init__(self):
        try:
            # Firebase 인증 파일 로드
            with open('./authentication/firebase_auth.json') as f:
                config = json.load(f)
                print("Firebase config loaded successfully.")  # 디버깅용 메시지
            
            # Firebase 초기화
            firebase = pyrebase.initialize_app(config)
            self.db = firebase.database()
        
        except FileNotFoundError:
            print("Error: firebase_auth.json 파일이 없습니다. 경로를 확인하세요.")
        
        except json.JSONDecodeError:
            print("Error: firebase_auth.json 파일이 올바른 형식이 아닙니다.")

    def insert_user(self, data, pw): 
        user_info = {
            "id": data['username'],  # "username"으로 수정
            "pw": pw,
            "nickname": data.get('nickname', '')  # nickname 필드가 없을 경우 기본값으로 빈 문자열 설정
        }
        if self.user_duplicate_check(data['username']):  # 여기서도 "username"으로 수정
            self.db.child("user").push(user_info) 
            print("User data inserted:", data)
            return True
        else:
            return False

    def user_duplicate_check(self, username): 
        users = self.db.child("user").get()
        print("Existing users:", users.val())

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
