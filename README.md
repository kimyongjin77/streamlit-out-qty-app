# 물류센터 출고수량 예측 앱(streamlit web dashboard)
## 개발 목적
물류센터의 향후 출고 물동량을 예측하여 센터내의 출고처리Capa를 고려한

설비 및 인력 운영 설계를 위한 가이드를 제공.
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
## 사용 라이브러리
```python
import streamlit as st
import pandas as pd
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from sklearn.metrics import mean_absolute_error
import calendar
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import joblib
import math
import matplotlib.pyplot as plt
import platform
from matplotlib import font_manager, rc
import altair as alt
```
## 소스파일구조 및 기능
> * common.py -> 함수 모음
> * app.py -> main()
>   + 그래프를 위한 한글폰트로드, 데이터로드
> > * app_eda.py
> >   + 데이터 개요
> >   + 전체출고현황 시각화
> >   + 거래처비교현황 시각화
> >   + 제품비교현황 시각화
> > > * app_ml.py
> > >   + prophet_total.pkl 로드 -> 구글코랩에서 Prophet 라이브러리를 이용하여 센터 기준 집계 데이터로 학습한 예측기
> > >   + 사용자 입력날짜 센터 출고수량 예측 -> prophet_total.pkl 예측기 사용
> > >   + 센터 출고수량 예측(모델평가 : 평균절대오차(MAE, Mean Absolute Error) -> prophet_total.pkl 예측기 사용
> > >   + 거래처별 출고수량 학습 및 예측
> > >   + 제품별 출고수량 학습 및 예측
