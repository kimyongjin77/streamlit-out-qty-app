# 물류센터 출고수량 예측 앱(streamlit web dashboard)

## 개발 목적
> 물류센터의 향후 출고 물동량을 예측하여 센터내의 출고처리Capa를 고려한
> 설비 및 인력 운영 설계를 위한 가이드를 제공.
  
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

## 소스파일구조
> common.py -> 함수 모음
> 
> app.py -> main()
> > app_eda.py
> > > app_ml.py

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
------------

* 링크

[네이버](https://www.naver.com)

* 순서없는 목록 +, *, -  총 3가지의 기호

  * 1
  * 2
    * 3
    * 4
 
* 인용문구

> 악법도 법이다

* 강조

**영화** 가 좋다.

* BlockQuote

> 안녕하세요
> > 저는 
> > > may-june 입니다.

* 숫자 목록 출력하기

1. 안녕하세요
2. 오늘하루도
3. 행복하세요

* 구분선, 수평선

------------
