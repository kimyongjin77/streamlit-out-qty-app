import streamlit as st
import pandas as pd  
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import platform
from matplotlib import font_manager, rc
import altair as alt
import plotly.express as px

from app_ml import run_ml

#from app_ml import run_ml

#print('This System=' + platform.system())
#print('This System=' + platform.platform())

plt.rcParams['axes.unicode_minus'] = False
if platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':
    path = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
elif platform.system() == 'Linux':
    #matplotlib의 폰트를 Nanum 폰트로 지정합니다.
    path = '/usr/share/fonts/nanum/NanumGothic.ttf'
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print('This System=' + platform.system() + ' Unknown system... sorry~~~~')

import calendar
import datetime

#해당 일자의 월의 마지막 날짜
def GetMonthLastDate(sourDate):
    #date = datetime(year=year, month=month, day=1).date()
    monthrange = calendar.monthrange(sourDate.year, sourDate.month)
    first_day = calendar.monthrange(sourDate.year, sourDate.month)[0]
    last_day = calendar.monthrange(sourDate.year, sourDate.month)[1]
    last_date = sourDate.replace(day=last_day)
    return last_date

#해당 일자의 주차의 일요일 날짜 기준
def GetWeekLastDate(sourceDate):
    #temporaryDate = datetime.datetime(sourceDate.year, sourceDate.month, sourceDate.day)
    #weekDayCount = temporaryDate.weekday()
    weekDayCount = sourceDate.weekday()
    targetDate = sourceDate + datetime.timedelta(days =  -weekDayCount + 6)
    #targetDate = AddDays(sourceDate, -weekDayCount + 6);
    return targetDate

def compare(source, x='출고일자', y='수량', group='거래처코드', axis_scale="linear"):
    # if st.checkbox("View logarithmic scale", key=group):
    #     axis_scale = "log"

    brush = alt.selection_interval(encodings=["x"], empty="all")
    click = alt.selection_multi(encodings=["color"])

    lines = (
                (
                    alt.Chart(source)
                    .mark_line(point=True)
                    .encode(
                                x=x,
                                y=alt.Y(y, scale=alt.Scale(type=f"{axis_scale}")),
                                color=group,
                                tooltip=[
                                            x,
                                            group,
                                            y,
                                            alt.Tooltip("delta", format=".2%"),
                                        ],
                            )
                )
                .add_selection(brush)
                .properties(width=550)
                .transform_filter(click)
            )

    bars = (
                alt.Chart(source)
                .mark_bar()
                .encode(
                            y=group,
                            color=group,
                            x=alt.X("수량:Q", scale=alt.Scale(type=f"{axis_scale}")),
                            tooltip=[x, y, alt.Tooltip("delta", format=".2%")],
                        )
                .transform_filter(brush)
                .properties(width=550)
                .add_selection(click)
            )

    return lines & bars

def all_out(source, x='출고일자', y='수량'):
    # Create a selection that chooses the nearest point & selects based on x-value
    hover = alt.selection_single(
                                    fields=[x],
                                    nearest=True,
                                    on="mouseover",
                                    empty="none",
                                )

    lines = (
                alt.Chart(source)
                .mark_line(point="transparent")
                .encode(x=x, y=y)
                .transform_calculate(color='datum.delta < 0 ? "red" : "green"')
            )

    # Draw points on the line, highlight based on selection, color based on 수량
    points = (
                lines.transform_filter(hover)
                .mark_circle(size=65)
                .encode(color=alt.Color("color:N", scale=None))
            )

    # Draw an invisible rule at the location of the selection
    tooltips = (
                    alt.Chart(source)
                    .mark_rule(opacity=0)
                    .encode(
                                x=x,
                                y=y,
                                tooltip=[x, y, alt.Tooltip("delta", format=".2%")],
                            )
                    .add_selection(hover)
                )

    return (lines + points + tooltips).interactive()

def run_eda():
    #pass
    
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: left;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)

    st.header('A사 물류센터 출고 정보')
    
    #link='[공공데이터포털](https://www.data.go.kr/data/15071816/fileData.do?recommendDataYn=Y)'
    #st.markdown(link, unsafe_allow_html=True)
    #st.write(f'데이터 출처 : ' + link)
    st.write(f'데이터 출처 : Z사')

    st.markdown('---')

    st.subheader('2021년01월04일 ~ 2022년05월 25일 데이터')

    #info1=st.info('데이터 로딩중.....잠시 기다려 주세요.')

    #df_head = pd.read_csv('data/concat_head.csv', encoding='ansi', index_col=0)
    df_head = pd.read_csv('data/concat_head.csv', encoding='CP949', index_col=0)

    #df_describe = pd.read_csv('data/concat_describe.csv', encoding='ansi', index_col=0)
    df_describe = pd.read_csv('data/concat_describe.csv', encoding='CP949', index_col=0)

    #df_cust_sum = pd.read_csv('data/cust_sum.csv', encoding='ansi', index_col=0)
    df_cust_sum = pd.read_csv('data/cust_sum.csv', encoding='CP949', index_col=0)

    df_cust_sum['출고일자'] = df_cust_sum['출고일자'].astype("datetime64")
    df_cust_sum['주간출고일자'] = df_cust_sum['주간출고일자'].astype("datetime64")
    df_cust_sum['월간출고일자'] = df_cust_sum['월간출고일자'].astype("datetime64")
    df_cust_sum['거래처'] = df_cust_sum['거래처코드'] + '-' + df_cust_sum['거래처명']

    #df_item_sum = pd.read_csv('data/item_sum.csv', encoding='ansi', index_col=0)
    df_item_sum = pd.read_csv('data/item_sum.csv', encoding='CP949', index_col=0)

    df_item_sum['출고일자'] = df_item_sum['출고일자'].astype("datetime64")
    df_item_sum['주간출고일자'] = df_item_sum['주간출고일자'].astype("datetime64")
    df_item_sum['월간출고일자'] = df_item_sum['월간출고일자'].astype("datetime64")
    df_item_sum['제품'] = df_item_sum['제품코드'] + '-' + df_item_sum['제품명']

    rows=df_describe.iloc[0,0].astype(int)
    cust_cnt=df_cust_sum['거래처코드'].nunique()
    item_cnt=df_item_sum['제품코드'].nunique()
    col1,col2,col3 = st.columns(3)
    with col1:
        st.write(f'데이터행수 : ' + f'{rows:,}')
    with col2:
        st.write(f'거래처수 : ' + f'{cust_cnt:,}')
    with col3:
        st.write(f'품목수 : ' + f'{item_cnt:,}')
    
    st.write(f'데이터 헤드 샘플')
    st.dataframe(df_head)

    st.write(f'데이터 describe')
    df_describe_pivot=df_describe.reset_index()
    df_describe_pivot = df_describe_pivot.pivot_table(columns='index',values='수량' )
    st.dataframe(df_describe_pivot)
    
    #info1.info('데이터 로딩 완료')

    st.markdown('---')
    
    st.subheader('전체 출고 현황')
    choice_item=['출고일자','주간출고일자','월간출고일자']
    choice=st.radio('일/주/월 기준 선택', choice_item, index=2)

    df_temp=df_cust_sum.groupby([choice])['수량'].sum()
    df_temp=pd.DataFrame(df_temp).reset_index()
    # Percentage difference (between 0-1) of downloads of current vs previous month
    df_temp["delta"] = df_temp['수량'].pct_change().fillna(0)
    # BigQuery returns the date column as type dbdate, which is not supported by Altair/Vegalite
    #df_temp[choice] = df_temp[choice].astype("datetime64")

    st.altair_chart(all_out(df_temp, choice), use_container_width=True)

    st.markdown('---')

    st.subheader('거래처 비교 현황')
    cust_names = sorted(df_cust_sum['거래처'].unique())
    
    instructions = """
                    Click and drag line chart to select and pan date interval\n
                    Hover over bar chart to view downloads\n
                    Click on a bar to highlight that package
                    """
    select_cust = st.multiselect(
        '비교할 거래처 선택',
        cust_names,
        default=[
                    '11088038-아리따움 NC야탑점',
                    '11008786-아리따움 성남(구)시청점'
                ],
        help=instructions,
    )

    select_cust_df = pd.DataFrame(select_cust).rename(columns={0: "거래처"})

    if len(select_cust) > 0:
        choice2=st.radio('일/주/월 기준 선택', choice_item, key='1', index=2)

        df_cust_preiod=df_cust_sum.loc[df_cust_sum['거래처'].isin(select_cust_df['거래처'])].groupby([choice2, '거래처코드', '거래처명', '거래처'])['수량'].sum()
        df_cust_preiod=pd.DataFrame(df_cust_preiod).reset_index()
        # Percentage difference (between 0-1) of downloads of current vs previous month
        df_cust_preiod["delta"] = df_cust_preiod.groupby('거래처코드')['수량'].pct_change().fillna(0)

        st.altair_chart(compare(df_cust_preiod, choice2, '수량', '거래처'), use_container_width=True)
    else:
        #st.stop()
        pass

    st.markdown('---')

    st.subheader('제품 비교 현황')
    item_names = sorted(df_item_sum['제품'].unique())
    
    # instructions = """
    #                 Click and drag line chart to select and pan date interval\n
    #                 Hover over bar chart to view downloads\n
    #                 Click on a bar to highlight that package
    #                 """
    select_item = st.multiselect(
        '비교할 제품 선택',
        item_names,
        default=[
                    '110000097-바이탈뷰티 슬림컷 28EA_18AD(시판)',
                    '110000108-바이탈뷰티(아) 스킨콜라겐 28입(19)'
                ],
        help=instructions,
    )

    select_item_df = pd.DataFrame(select_item).rename(columns={0: "제품"})

    if len(select_item) > 0:
        choice2=st.radio('일/주/월 기준 선택', choice_item, key='2', index=2)

        df_item_preiod=df_item_sum.loc[df_item_sum['제품'].isin(select_item_df['제품'])].groupby([choice2, '제품코드', '제품명', '제품'])['수량'].sum()
        df_item_preiod=pd.DataFrame(df_item_preiod).reset_index()
        # Percentage difference (between 0-1) of downloads of current vs previous month
        df_item_preiod["delta"] = df_item_preiod.groupby('제품코드')['수량'].pct_change().fillna(0)

        st.altair_chart(compare(df_item_preiod, choice2, '수량', '제품'), use_container_width=True)
    
    st.markdown('---')

    run_ml()