import streamlit as st
import pandas as pd  
import common as cm
import app_ml as ml

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

    rows=cm.df_describe.iloc[0,0].astype(int)
    cust_cnt=cm.df_cust_sum['거래처코드'].nunique()
    item_cnt=cm.df_item_sum['제품코드'].nunique()
    col1,col2,col3 = st.columns(3)
    with col1:
        st.write(f'데이터행수 : ' + f'{rows:,}')
    with col2:
        st.write(f'거래처수 : ' + f'{cust_cnt:,}')
    with col3:
        st.write(f'품목수 : ' + f'{item_cnt:,}')
    
    st.write(f'데이터 헤드 샘플')
    st.dataframe(cm.df_head)

    st.write(f'데이터 describe')
    df_describe_pivot=cm.df_describe.reset_index()
    df_describe_pivot = df_describe_pivot.pivot_table(columns='index',values='수량' )
    st.dataframe(df_describe_pivot)

    st.markdown('---')
    
    st.subheader('전체 출고 현황')
    choice_item=['출고일자','주간출고일자','월간출고일자']
    choice=st.radio('일/주/월 기준 선택', choice_item, index=2, key='radio_1')

    df_temp=cm.df_cust_sum.groupby([choice])['수량'].sum()
    df_temp=pd.DataFrame(df_temp).reset_index()
    # Percentage difference (between 0-1) of downloads of current vs previous month
    df_temp["delta"] = df_temp['수량'].pct_change().fillna(0)

    st.altair_chart(cm.alt_chart_selection_single(df_temp, choice), use_container_width=True)

    st.markdown('---')

    st.subheader('거래처 비교 현황')
    
    instructions = """
                    Click and drag line chart to select and pan date interval\n
                    Hover over bar chart to view downloads\n
                    Click on a bar to highlight that package
                    """
    select_cust = st.multiselect(
        '비교할 거래처 선택',
        cm.df_cust_names,
        default=[
                    '11088038-아리따움 NC야탑점',
                    '11008786-아리따움 성남(구)시청점'
                ],
        help=instructions,
        key='multiselect_1'
    )

    select_cust_df = pd.DataFrame(select_cust).rename(columns={0: "거래처"})

    if len(select_cust) > 0:
        choice2=st.radio('일/주/월 기준 선택', choice_item, index=2, key='radio_2')

        df_cust_preiod=cm.df_cust_sum.loc[cm.df_cust_sum['거래처'].isin(select_cust_df['거래처'])].groupby([choice2, '거래처코드', '거래처명', '거래처'])['수량'].sum()
        df_cust_preiod=pd.DataFrame(df_cust_preiod).reset_index()
        # Percentage difference (between 0-1) of downloads of current vs previous month
        df_cust_preiod["delta"] = df_cust_preiod.groupby('거래처코드')['수량'].pct_change().fillna(0)

        st.altair_chart(cm.alt_chart_selection_multi(df_cust_preiod, choice2, '수량', '거래처'), use_container_width=True)
    else:
        #st.stop()
        pass

    st.markdown('---')

    st.subheader('제품 비교 현황')
    
    # instructions = """
    #                 Click and drag line chart to select and pan date interval\n
    #                 Hover over bar chart to view downloads\n
    #                 Click on a bar to highlight that package
    #                 """
    select_item = st.multiselect(
        '비교할 제품 선택',
        cm.df_item_names,
        default=[
                    '110000097-바이탈뷰티 슬림컷 28EA_18AD(시판)',
                    '110000108-바이탈뷰티(아) 스킨콜라겐 28입(19)'
                ],
        help=instructions,
        key='multiselect_2'
    )

    select_item_df = pd.DataFrame(select_item).rename(columns={0: "제품"})

    if len(select_item) > 0:
        choice2=st.radio('일/주/월 기준 선택', choice_item, index=2, key='radio_3')

        df_item_preiod=cm.df_item_sum.loc[cm.df_item_sum['제품'].isin(select_item_df['제품'])].groupby([choice2, '제품코드', '제품명', '제품'])['수량'].sum()
        df_item_preiod=pd.DataFrame(df_item_preiod).reset_index()
        # Percentage difference (between 0-1) of downloads of current vs previous month
        df_item_preiod["delta"] = df_item_preiod.groupby('제품코드')['수량'].pct_change().fillna(0)

        st.altair_chart(cm.alt_chart_selection_multi(df_item_preiod, choice2, '수량', '제품'), use_container_width=True)
    
    st.markdown('---')

    ml.run_ml()