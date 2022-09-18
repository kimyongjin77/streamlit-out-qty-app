# 물류센터 출고수량 예측 앱(streamlit web dashboard)
## 개발 목적
물류센터의 향후 출고 물동량을 예측하여 센터내의 출고처리Capa를 고려한

설비 및 인력 운영 설계를 위한 참고자료를 제공.
## 데이터
A사 물류센터 출고 정보(2021년01월04일 ~ 2022년05월 25일)

출처 : Z사

RAW데이터파일 컬럼 : 출고일자, 거래처코드, 거래처명, 제품코드, 제품명, 수량

RAW데이터행수 : 11,025,190(약 1GB)

거래처수 : 4,823

품목수 : 7,787
## 데이터 가공
RAW데이터파일 용량이 너무 커서 집계/요약한 파일로 생성하여 사용

센터 기준 집계 : 출고일자, 수량, 주간출고일자, 월간출고일자

거래처 기준 집계 : 출고일자, 거래처, 수량, 주간출고일자, 월간출고일자

제품 기준 집계 : 출고일자, 제품, 수량, 주간출고일자, 월간출고일자

데이터 헤드 : RAW데이터셋의 처음 5개

데이터 describe : RAW데이터셋의 describe

## 개발 환경
* OS : windows 10
* Anaconda
* python 3.7
* streamlit 1.9
* vscode, jupyter, 구글코랩, github

## 사용 라이브러리
* pip install streamlit
* pip install fbprophet
* pip install altair

## 소스파일구조 및 구현기능
> * common.py -> 함수 모음, 전역변수(데이터프레임)
> * app.py -> main()
>   + 그래프를 위한 한글폰트로드, 데이터로드
> > * app_eda.py
> >   + 데이터 개요
> >   + 전체출고현황 시각화
> >   + 거래처비교출고현황 시각화
> >   + 제품비교출고현황 시각화
> > > * app_ml.py
> > >   + prophet_total.pkl 로드 -> 구글코랩에서 Prophet 라이브러리를 이용하여 센터 기준 집계 데이터로 학습한 예측기
> > >   + 사용자 입력날짜 센터 출고수량 예측 -> prophet_total.pkl 예측기 사용
> > >   + 센터 출고수량 예측(모델평가 : 평균절대오차(MAE, Mean Absolute Error) -> prophet_total.pkl 예측기 사용
> > >   + 거래처별 출고수량 학습 및 예측
> > >   + 제품별 출고수량 학습 및 예측

## 출고물량 예측.ipynb [https://drive.google.com/file/d/1opTbgtyDmWstNpry8lzAW76W0pRa1YG9/view?usp=sharing]
## 앱URL [http://ec2-3-34-2-16.ap-northeast-2.compute.amazonaws.com:8504]

![img1](https://user-images.githubusercontent.com/105832520/172524356-4b030ae2-037c-47cf-9f84-50e52b68ca75.PNG)
![img2](https://user-images.githubusercontent.com/105832520/172525210-ce31dd92-e81f-4c75-b142-2e2b0d9dd832.PNG)
![img3](https://user-images.githubusercontent.com/105832520/172525217-ec49f0a1-8e22-4c33-a0f6-8762fd31ae7a.PNG)
![img4](https://user-images.githubusercontent.com/105832520/172525231-99ed0d57-d134-4b6d-b737-dfe6447d8cbd.PNG)
![img5](https://user-images.githubusercontent.com/105832520/172525238-a4d02f96-c240-438b-8cb3-dfccb736b4bf.PNG)
![img6](https://user-images.githubusercontent.com/105832520/172525248-4ce63aa5-cf3c-4da9-800a-2be8c40d7a8c.PNG)
![img7](https://user-images.githubusercontent.com/105832520/172525256-f60a5634-6ca9-4626-8e44-eb53c145b077.PNG)
![img8](https://user-images.githubusercontent.com/105832520/172525269-27332b5e-7f91-41ce-8024-0b510bbeb3b1.PNG)
![img9](https://user-images.githubusercontent.com/105832520/172525277-3e1d57e2-6cde-4d39-a17a-98ff18968236.PNG)
