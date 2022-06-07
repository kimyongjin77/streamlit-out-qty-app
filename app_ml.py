import streamlit as st
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
import common as cm
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from sklearn.metrics import mean_absolute_error
import pandas as pd
import joblib
import math

def run_ml():
    #pass
    st.subheader('센터/거래처별/제품별 출고수량 예측')

    prophet_total=joblib.load('data/prophet_total.pkl')

    with st.expander('사용자 입력날짜 센터 출고수량 예측', False):
        start_date=date.today()
        year_delta = relativedelta(years=1)
        end_date=start_date + year_delta
        choice_date=st.date_input('날짜 선택', min_value=start_date, max_value=end_date, key='date_input_1')
        info1=st.info('예측 중입니다.. 잠시 기다려 주세요...')
        user_future=cm.GetDatetimeColDataFrame(choice_date, choice_date, 'ds')
        user_future['y']=0
        user_forecast=prophet_total.predict(user_future)
        user_pred=user_forecast.loc[user_forecast['ds'].dt.date==choice_date, 'yhat'][0]
        info1.info(f'{choice_date} 일자의 출고예측 수량은 {math.trunc(user_pred):,} 개 입니다')

    with st.expander('센터 출고수량 예측(모델평가 : 평균절대오차(MAE, Mean Absolute Error)', False):
        n_months_period = st.slider('예측개월수', 1, 12, 12, disabled=True, key='slider_1')
        n_days_period = int((n_months_period / 12) * 365)

        submitted = st.button(label='예측 실행', key='button_1')

        if submitted:
            txt_info=st.info('예측 중입니다. 잠시 기다려 주세요...')

            future=prophet_total.make_future_dataframe(periods=n_days_period, freq='D')
            forecast=prophet_total.predict(future)
            txt_info.info('예측 완료.')

            st.write('전체 ' + str(n_months_period) + '개월 예측 그래프')
            fig1 = plot_plotly(prophet_total, forecast, xlabel='출고일자', ylabel='수량')
            st.plotly_chart(fig1, use_container_width=True)
            
            st.write('전체 ' + str(n_months_period) + '개월 예측 components')
            fig2=prophet_total.plot_components(forecast)
            st.write(fig2)

            # 모델평가 : 평균절대오차(MAE, Mean Absolute Error)
            st.write('모델평가 : 평균절대오차(MAE, Mean Absolute Error), MSE와 마찬가지로 수치가 작을수록 좋은 모델')
            st.write('이미 알고 있는 2022-05월 데이터를 Out-Of-Sample Forecast 하여 MAE를 구한다.')
            #마지막 2022-5월달 실제 값(prophet_total을 학습 시킨 데이터)
            y_true=cm.df_sum.loc[cm.df_sum['출고일자'].dt.date >= date(2022, 5, 1),]
            y_true.columns = ['ds', 'y']
            #마지막 2022-5월달 예측 값(위에서 예측한 값)
            y_pred=y_true.merge(forecast, on='ds')[['ds', 'yhat']]
            # MAE(MSE와 마찬가지로 수치가 작을수록 좋은 모델)를 살펴본다.
            mae = mean_absolute_error(y_true['y'].values, y_pred['yhat'].values)
            st.write(f'MAE: %.3f' % mae)
            
            # 실제값과 예측값을 시각화 해 본다.
            y_true['구분']='실제값'
            y_true.columns=['출고일자','수량','구분']
            y_pred['구분']='예측값'
            y_pred.columns=['출고일자','수량','구분']

            df_temp=pd.concat([y_true, y_pred])
            df_temp['수량']=df_temp['수량'].astype(int)
            st.altair_chart(cm.alt_chart_selection_multi2(df_temp, '출고일자', '수량', '구분'), use_container_width=True)
    
    with st.expander('거래처별 출고수량 학습 및 예측', False):
        #pass
        select_cust = st.selectbox(
                                        '거래처 선택',
                                        cm.df_cust_names,
                                        index=cm.df_cust_names.index('11087632-고창선운(방)'),
                                        key='selectbox_1'
                                    )
        
        #select_cust_df = pd.DataFrame(select_cust).rename(columns={0: '거래처'})

        n_months_period = st.slider('예측개월수', 1, 12, 12, disabled=True, key='slider_2')
        n_days_period = int(n_months_period / 12) * 365
        
        submitted = st.button(label='학습 및 예측 실행', key='button_2')

        if select_cust != '' and submitted:
            #print(select_cust)
            txt_info=st.info('학습데이터 추출 중입니다. 잠시 기다려 주세요...')
            prophet_df = cm.df_cust_sum.loc[cm.df_cust_sum['거래처']==select_cust,['출고일자','수량']]
            prophet_df.columns = ['ds', 'y']
            
            #txt_info.info('학습데이터 추출 완료.')
            prophet=Prophet()
            # Specifying Custom Seasonalities
            prophet.add_seasonality(name='monthly', period=30.5, fourier_order=5)
            txt_info.info('학습 중입니다. 잠시 기다려 주세요...')
            prophet.fit(prophet_df)
            txt_info.info('학습 완료하여 예측 중입니다. 잠시 기다려 주세요...')
            #future=prophet.make_future_dataframe(periods=n_months_period, freq='M')
            future=prophet.make_future_dataframe(periods=n_days_period, freq='D')
            forecast=prophet.predict(future)
            txt_info.info('예측 완료.')

            st.write(select_cust + ' ' + str(n_months_period) + '개월 예측 그래프')
            fig1 = plot_plotly(prophet, forecast, xlabel='출고일자', ylabel='수량')
            st.plotly_chart(fig1, use_container_width=True)
            
            st.write(select_cust + ' ' + str(n_months_period) + '개월 예측 components')
            fig2=prophet.plot_components(forecast)
            st.write(fig2)

    with st.expander('제품별 출고수량 학습 및 예측', False):
        #pass
        select_item = st.selectbox(
                                        '제품 선택',
                                        cm.df_item_names,
                                        index=cm.df_item_names.index('110641096-프리메라 알파인 베리 워터리 크림 50ml (20AD'),
                                        key='selectbox_2'
                                    )
        
        #select_item_df = pd.DataFrame(select_item).rename(columns={0: '제품'})

        n_months_period = st.slider('예측개월수', 1, 12, 12, disabled=True, key='slider_3')
        n_days_period = int(n_months_period / 12) * 365
        
        submitted = st.button(label='학습 및 예측 실행', key='button_3')

        if select_item != '' and submitted:
            #print(select_item)
            txt_info=st.info('학습데이터 추출 중입니다. 잠시 기다려 주세요...')
            prophet_df = cm.df_item_sum.loc[cm.df_item_sum['제품']==select_item,['출고일자','수량']]
            prophet_df.columns = ['ds', 'y']

            #txt_info.info('학습데이터 추출 완료.')
            prophet=Prophet()
            # Specifying Custom Seasonalities
            prophet.add_seasonality(name='monthly', period=30.5, fourier_order=5)
            txt_info.info('학습 중입니다. 잠시 기다려 주세요...')
            prophet.fit(prophet_df)
            txt_info.info('학습 완료하여 예측 중입니다. 잠시 기다려 주세요...')
            #future=prophet.make_future_dataframe(periods=n_months_period, freq='M')
            future=prophet.make_future_dataframe(periods=n_days_period, freq='D')
            forecast=prophet.predict(future)
            txt_info.info('예측 완료.')

            st.write(select_item + ' ' + str(n_months_period) + '개월 예측 그래프')
            fig1 = plot_plotly(prophet, forecast, xlabel='출고일자', ylabel='수량')
            st.plotly_chart(fig1, use_container_width=True)
            
            st.write(select_item + ' ' + str(n_months_period) + '개월 예측 components')
            fig2=prophet.plot_components(forecast)
            st.write(fig2)
    
    st.markdown('---')