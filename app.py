import streamlit as st
import common as cm
import app_eda as eda

st.set_page_config(
   page_title='물류센터 출고수량 예측',
   page_icon='data/icon.png',
   layout='centered',
   initial_sidebar_state='expanded'
)

def main():
    #pass
    st.title('물류센터 출고수량 예측 (Facebook Prophet 라이브러리)')

    cm.fontLoad()
    cm.DataLoad()

    eda.run_eda()

if __name__=='__main__':
    main()