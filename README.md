# FLASK_PROJECT2024

**Team 소프리🕊️**  
*Open SW Platform 24-2, Ewha Womans University*

---

## 📌 프로젝트 소개

<p align="center">
    <img src="static/image/Readme.png" alt="리드미 대문" width="300">
</p>

**Ewha Market**은 다음과 같은 마켓 웹 어플리케이션입니다:

- 기존 교내의 온/오프라인에서 진행되던 학생들의 수제 아이템 거래를 더욱 안전하고 편리하게 이용할 수 있도록 개발되었습니다.
- 단순화하고 최적화된 거래 환경을 제공하여 기존의 건전한 거래 문화에 기여하기 위해 기획되었습니다.

---

## 📽️ 시연 영상

- [시연 영상 보기](https://www.youtube.com/)

---

## 🚀 주요 기능

- **사용자 인증**: 로그인 및 회원가입 기능.
- **상품 관리**:
  - 상품 등록 기능.
- **리뷰 및 위시리스트**:
  - 구매한 상품에 대한 리뷰 작성 및 확인.
  - 관심 상품 위시리스트에 추가 기능.
- **플랫폼 내 통합된 거래**:
  - 구매, 판매 이력을 쉽게 조회.
  - 상품별 리뷰와 상태를 쉽게 확인 가능.

---

## 🛠 기술 스택

- **백엔드**: Flask
- **프론트엔드**: HTML, CSS, JavaScript
- **데이터베이스**: Firebase
- **기타**: Conda 가상환경, Pyrebase

---

## ⚙️ 설치 및 실행 방법

1. **리포지토리 클론**

   ```bash
   git clone https://github.com/EWHA-Sofree/FLASK_PROJECT2024.git
   cd FLASK_PROJECT2024
   ```

2. **가상환경 생성**  
  Anaconda에서 Python 가상환경을 생성:

   ```bash
   conda create --name <your-environment-name>
   ```

3. **가상환경 활성화**  
  생성한 가상환경을 활성화:

   ```bash
   conda activate <your-environment-name>
   ```

4. **패키지 설치**  

   ```bash
   conda install flask
   pip install pyrebase4
   ```

5. **애플리케이션 실행**

   ```bash
   flask run
   ```

6. **브라우저에서 접속**

   브라우저에서 `http://127.0.0.1:5000`으로 접속하여 어플리케이션 확인.

---

## 📂 프로젝트 폴더 구조

```text

📂 FLASK_PROJECT2024/
├── 📂 authentication/       # Firebase 인증 정보
│   └── firebase_auth.json   # Firebase 인증 JSON 파일
├── 📂 static/               # 정적 파일
│   ├── css/                 # 화면별 CSS 파일
│   ├── image/               # 이미지 파일
│   └── main.js              # 메인 페이지 JS 파일
├── 📂 templates/            # HTML 템플릿
├── .gitignore               # Git에서 무시할 파일 목록
├── LICENSE                  # 프로젝트 라이선스
├── README.md                # 프로젝트 설명
├── app.py                   # Flask 애플리케이션 엔트리포인트, 주요 로직
└── database.py              # 데이터베이스 핸들러
```

---

## 📦 주요 의존성

- **flask**: 백엔드 프레임워크
- **pyrebase**: Firebase 연결 및 데이터 처리
- **[jQuery](https://code.jquery.com/jquery-latest.min.js)**: DOM 조작 및 이벤트 처리를 간소화하기 위한 JavaScript 라이브러리

---

## 📜 기능 설명

1. **템플릿 구조**

    ```text
    📂 templates/
        ├── index.html            # 공통 레이아웃 (헤더, 네비게이션바, 푸터)
        ├── main.html             # 메인 화면 레이아웃
        ├── item_detail.html      # 상품 상세 페이지
        ├── list.html             # 상품 리스트 페이지
        ├── mypage.html           # 마이 페이지
        ├── reg_item.html         # 상품 등록 페이지
        ├── reviews_list.html     # 리뷰 목록 페이지
        ├── login.html            # 로그인 페이지
        └── sign_up.html          # 회원가입 페이지
    ```

2. **Firebase 데이터베이스 역할**
   - **user**: 사용자 정보 관리
   - **review**: 상품 리뷰 저장
   - **purchases**: 구매 내역 관리
   - **item**: 상품 정보 관리
   - **heart**: 찜한 상품 관리  

**등록한 상품/리뷰 이미지는 로컬 경로에 저장됩니다.*

---

## 📝 프로젝트 기여 방법

1. **Fork**: 이 리포지토리를 포크합니다.
2. **브랜치 생성**: 새로운 기능을 추가하기 위해 브랜치를 만드세요:

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **커밋**: 변경 사항을 커밋합니다:

   ```bash
   git commit -m "Add your feature description"
   ```

4. **푸시**: 브랜치를 리모트 리포지토리에 푸시합니다:

   ```bash
   git push origin feature/your-feature-name
   ```

5. **PR 생성**: Pull Request를 생성합니다.

---

## 📖 기술 블로그

더 자세한 개발 과정은 기술 블로그에서 확인할 수 있습니다.

[기술 블로그](https://lying-chiller-8c1.notion.site/15103656e23f8088b328d055905c3b14)
- [📕 개념](https://lying-chiller-8c1.notion.site/15103656e23f80c08c7ef69b75f2188b) / [⛓️ 가이드](https://lying-chiller-8c1.notion.site/15103656e23f80da8e21e698428d91d8) / [🔗 팁/디버깅](https://flannel-interest-6ec.notion.site/1522b77b3a26805ebcd2caa3b5d4f72b) / [1️⃣ 해설1](https://lying-chiller-8c1.notion.site/1-15103656e23f80b389ffd8fcf8371a29) / [2️⃣ 해설2](https://lying-chiller-8c1.notion.site/2-12103656e23f8089a91ae090b017fee0)

---

## 📜 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)를 따릅니다.
