import streamlit as st
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
import common as cm
from datetime import date
from sklearn.metrics import mean_absolute_error
import pandas as pd

def run_ml():
    #pass
    st.subheader('전체/거래처별/제품별 출고수량 예측')

    with st.expander('전체 출고수량 예측', True):
        #pass
        n_months_period = st.slider('예측개월수', 1, 12, 12, disabled=True, key='slider_1')
        n_days_period = int((n_months_period / 12) * 365)

        submitted = st.button(label='예측 실행', key='button_1')

        if submitted:
            #print(select_cust)
            txt_info=st.info('학습데이터 추출 중입니다. 잠시 기다려 주세요...')
            cm.df_sum.columns = ['ds', 'y']

            df_prophet=cm.df_sum
            # df_prophet=cm.GetDatetimeColDataFrame(cm.df_sum['ds'].min(), cm.df_sum['ds'].max(), 'ds')
            # df_prophet=pd.merge(df_prophet, cm.df_sum, how="left", on=['ds'])
            # df_prophet.sort_values('ds',inplace=True)
            # df_prophet['y'].fillna(0, inplace=True)

            #txt_info.info('학습데이터 추출 완료.')
            prophet=Prophet()
            # Specifying Custom Seasonalities
            prophet.add_seasonality(name='monthly', period=30.5, fourier_order=5)
            
            txt_info.info('학습 중입니다. 잠시 기다려 주세요...')
            prophet.fit(df_prophet)
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

            # 모델평가 : 평균절대오차(MAE, Mean Absolute Error)
            st.write(f'모델평가 : 평균절대오차(MAE, Mean Absolute Error), MSE와 마찬가지로 수치가 작을수록 좋은 모델')
            st.write(f'이미 알고 있는 2022-05월 데이터를 Out-Of-Sample Forecast 하여 MAE를 구한다.')
            #마지막 2022-5월달 제외시킨 학습데이터
            train=df_prophet.loc[df_prophet['ds'].dt.date < date(2022, 5, 1),]
            #마지막 2022-5월달 실제 값
            y_true=df_prophet.loc[df_prophet['ds'].dt.date >= date(2022, 5, 1), 'y'].values
            # 모델 생성 후 학습
            model=Prophet()
            # Specifying Custom Seasonalities
            model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
            model.fit(train)
            # 2022-5월달 예측 날짜 생성
            future=df_prophet.loc[df_prophet['ds'].dt.date >= date(2022, 5, 1),]
            # 예측하고 비교하기
            forecast=model.predict(future)
            # MAE(MSE와 마찬가지로 수치가 작을수록 좋은 모델)를 살펴본다.
            y_pred = forecast['yhat'].values
            mae = mean_absolute_error(y_true, y_pred)
            st.write(f'MAE: %.3f' % mae)
            
            # 실제값과 예측값을 시각화 해 본다.
            df_temp1=future[['ds','y']]
            df_temp1['구분']='실제값'
            df_temp1.columns=['출고일자','수량','구분']
            df_temp2=forecast[['ds','yhat']]
            df_temp2['구분']='예측값'
            df_temp2.columns=['출고일자','수량','구분']

            df_temp3=pd.concat([df_temp1, df_temp2])
            df_temp3['수량']=df_temp3['수량'].astype(int)
            st.altair_chart(cm.alt_chart_selection_multi2(df_temp3, '출고일자', '수량', '구분'), use_container_width=True)
            
            # choice_date=st.date_input(f'예측결과 내 확인')
            # choice_date=cm.GetMonthLastDate(choice_date)
            # print(choice_date)
            # print(type(choice_date))
            # forecast_temp=forecast.loc[forecast['ds'].dt.date==choice_date, 'yhat']
            
    with st.expander('거래처별 출고수량 예측', True):
        #pass
        select_cust = st.selectbox(
            '거래처 선택',
            cm.df_cust_names,
            index=cm.df_cust_names.index('11087632-고창선운(방)'),
            key='selectbox_1'
        )
        
        #select_cust_df = pd.DataFrame(select_cust).rename(columns={0: "거래처"})

        n_months_period = st.slider('예측개월수', 1, 12, 12, disabled=True, key='slider_2')
        n_days_period = int(n_months_period / 12) * 365
        
        submitted = st.button(label='예측 실행', key='button_2')

        if select_cust != '' and submitted:
            #print(select_cust)
            txt_info=st.info('학습데이터 추출 중입니다. 잠시 기다려 주세요...')
            prophet_df = cm.df_cust_sum.loc[cm.df_cust_sum['거래처']==select_cust,['출고일자','수량']]
            prophet_df.columns = ['ds', 'y']

            # df_temp=cm.GetDatetimeColDataFrame(prophet_df['ds'].min(), prophet_df['ds'].max(), 'ds')
            # prophet_df=pd.merge(df_temp, prophet_df, how="left", on=['ds'])
            # prophet_df.sort_values('ds',inplace=True)
            # prophet_df['y'].fillna(0, inplace=True)
            
            #txt_info.info('학습데이터 추출 완료.')
            prophet=Prophet()
            # Specifying Custom Seasonalities
            prophet.add_seasonality(name='monthly', period=30.5, fourier_order=5)
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
            index=cm.df_item_names.index('110641096-프리메라 알파인 베리 워터리 크림 50ml (20AD'),
            key='selectbox_2'
        )
        
        #select_item_df = pd.DataFrame(select_item).rename(columns={0: "제품"})

        n_months_period = st.slider('예측개월수', 1, 12, 12, disabled=True, key='slider_3')
        n_days_period = int(n_months_period / 12) * 365
        
        submitted = st.button(label='예측 실행', key='button_3')

        if select_item != '' and submitted:
            #print(select_item)
            txt_info=st.info('학습데이터 추출 중입니다. 잠시 기다려 주세요...')
            prophet_df = cm.df_item_sum.loc[cm.df_item_sum['제품']==select_item,['출고일자','수량']]
            prophet_df.columns = ['ds', 'y']

            # df_temp=cm.GetDatetimeColDataFrame(prophet_df['ds'].min(), prophet_df['ds'].max(), 'ds')
            # prophet_df=pd.merge(df_temp, prophet_df, how="left", on=['ds'])
            # prophet_df.sort_values('ds',inplace=True)
            # prophet_df['y'].fillna(0, inplace=True)

            #txt_info.info('학습데이터 추출 완료.')
            prophet=Prophet()
            # Specifying Custom Seasonalities
            prophet.add_seasonality(name='monthly', period=30.5, fourier_order=5)
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