import streamlit as st
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
import common as cm

def run_ml():
    #pass
    st.header('전체/거래처별/제품별 출고수량 예측')

    with st.expander('전체 출고수량 예측', True):
        #pass
        n_months_period = st.slider('예측개월수',1,12,12,disabled=True,key='slider_1')
        #n_months_period = 12
        n_days_period = n_months_period * 30
        n_weeks_period = n_months_period * 5
        n_year_period = 365

        submitted = st.button(label='예측 실행', key='button_1')

        if submitted:
            #print(select_cust)
            txt_info=st.info('학습데이터 추출 중입니다. 잠시 기다려 주세요...')
            cm.df_sum.columns = ['ds', 'y']
            #txt_info.info('학습데이터 추출 완료.')
            prophet=Prophet()
            txt_info.info('학습 중입니다. 잠시 기다려 주세요...')
            prophet.fit(cm.df_sum)
            txt_info.info('학습 완료하여 예측 중입니다. 잠시 기다려 주세요...')
            future=prophet.make_future_dataframe(periods=n_months_period, freq='M')
            forecast=prophet.predict(future)
            txt_info.info('예측 완료.')

            st.write(f'' + '전체' + ' ' + str(n_months_period) + '개월 예측 그래프')
            fig1 = plot_plotly(prophet, forecast, xlabel='출고일자', ylabel='수량')
            st.plotly_chart(fig1, use_container_width=True)
            
            st.write(f'' + '전체' + ' ' + str(n_months_period) + '개월 예측 components')
            fig2=prophet.plot_components(forecast)
            st.write(fig2)

    with st.expander('거래처별 출고수량 예측', True):
        #pass
        select_cust = st.selectbox(
            '거래처 선택',
            cm.df_cust_names,
            index=cm.df_cust_names.index('11088038-아리따움 NC야탑점'),
            key='selectbox_1'
        )
        
        #select_cust_df = pd.DataFrame(select_cust).rename(columns={0: "거래처"})

        n_months_period = st.slider('예측개월수',1,12,12,disabled=True, key='slider_2')
        #n_months_period = 12
        n_days_period = n_months_period * 30
        n_weeks_period = n_months_period * 5
        
        submitted = st.button(label='예측 실행', key='button_2')

        if select_cust != '' and submitted:
            #print(select_cust)
            txt_info=st.info('학습데이터 추출 중입니다. 잠시 기다려 주세요...')
            prophet_df = cm.df_cust_sum.loc[cm.df_cust_sum['거래처']==select_cust,['출고일자','수량']]
            prophet_df.columns = ['ds', 'y']
            #txt_info.info('학습데이터 추출 완료.')
            prophet=Prophet()
            txt_info.info('학습 중입니다. 잠시 기다려 주세요...')
            prophet.fit(prophet_df)
            txt_info.info('학습 완료하여 예측 중입니다. 잠시 기다려 주세요...')
            future=prophet.make_future_dataframe(periods=n_months_period, freq='M')
            forecast=prophet.predict(future)
            txt_info.info('예측 완료.')

            st.write(f'' + select_cust + ' ' + str(n_months_period) + '개월 예측 그래프')
            fig1 = plot_plotly(prophet, forecast, xlabel='출고일자', ylabel='수량')
            st.plotly_chart(fig1, use_container_width=True)
            
            st.write(f'' + select_cust + ' ' + str(n_months_period) + '개월 예측 components')
            fig2=prophet.plot_components(forecast)
            st.write(fig2)

    with st.expander('제품별 출고수량 예측', True):
        #pass
        select_item = st.selectbox(
            '제품 선택',
            cm.df_item_names,
            index=cm.df_item_names.index('110000097-바이탈뷰티 슬림컷 28EA_18AD(시판)'),
            key='selectbox_2'
        )
        
        #select_item_df = pd.DataFrame(select_item).rename(columns={0: "제품"})

        n_months_period = st.slider('예측개월수',1,12,12,disabled=True, key='slider_3')
        #n_months_period = 12
        n_days_period = n_months_period * 30
        n_weeks_period = n_months_period * 5
        
        submitted = st.button(label='예측 실행', key='button_3')

        if select_item != '' and submitted:
            #print(select_item)
            txt_info=st.info('학습데이터 추출 중입니다. 잠시 기다려 주세요...')
            prophet_df = cm.df_item_sum.loc[cm.df_item_sum['제품']==select_item,['출고일자','수량']]
            prophet_df.columns = ['ds', 'y']
            #txt_info.info('학습데이터 추출 완료.')
            prophet=Prophet()
            txt_info.info('학습 중입니다. 잠시 기다려 주세요...')
            prophet.fit(prophet_df)
            txt_info.info('학습 완료하여 예측 중입니다. 잠시 기다려 주세요...')
            future=prophet.make_future_dataframe(periods=n_months_period, freq='M')
            forecast=prophet.predict(future)
            txt_info.info('예측 완료.')

            st.write(f'' + select_item + ' ' + str(n_months_period) + '개월 예측 그래프')
            fig1 = plot_plotly(prophet, forecast, xlabel='출고일자', ylabel='수량')
            st.plotly_chart(fig1, use_container_width=True)
            
            st.write(f'' + select_item + ' ' + str(n_months_period) + '개월 예측 components')
            fig2=prophet.plot_components(forecast)
            st.write(fig2)
    
    st.markdown('---')