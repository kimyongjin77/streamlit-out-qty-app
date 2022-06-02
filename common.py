import pandas as pd
import calendar
import datetime
import matplotlib.pyplot as plt
import platform
from matplotlib import font_manager, rc
import altair as alt

df_head = pd.DataFrame({'A' : []})
df_describe = pd.DataFrame({'A' : []})
df_cust_sum = pd.DataFrame({'A' : []})
df_cust_names = pd.DataFrame({'A' : []})
df_item_sum = pd.DataFrame({'A' : []})
df_item_names = pd.DataFrame({'A' : []})
df_sum = pd.DataFrame({'A' : []})

def DataLoad():
    # global myList
    # myList = []

    global df_head
    global df_describe
    global df_cust_sum
    global df_cust_names
    global df_item_sum
    global df_item_names
    global df_sum

    df_head = pd.read_csv('data/concat_head.csv', encoding='CP949', index_col=0)

    df_describe = pd.read_csv('data/concat_describe.csv', encoding='CP949', index_col=0)

    df_cust_sum = pd.read_csv('data/cust_sum.csv', encoding='CP949', index_col=0)
    df_cust_sum['출고일자'] = df_cust_sum['출고일자'].astype("datetime64")
    df_cust_sum['주간출고일자'] = df_cust_sum['주간출고일자'].astype("datetime64")
    df_cust_sum['월간출고일자'] = df_cust_sum['월간출고일자'].astype("datetime64")
    df_cust_sum['거래처'] = df_cust_sum['거래처코드'] + '-' + df_cust_sum['거래처명']
    df_cust_names = sorted(df_cust_sum['거래처'].unique())

    df_item_sum = pd.read_csv('data/item_sum.csv', encoding='CP949', index_col=0)
    df_item_sum['출고일자'] = df_item_sum['출고일자'].astype("datetime64")
    df_item_sum['주간출고일자'] = df_item_sum['주간출고일자'].astype("datetime64")
    df_item_sum['월간출고일자'] = df_item_sum['월간출고일자'].astype("datetime64")
    df_item_sum['제품'] = df_item_sum['제품코드'] + '-' + df_item_sum['제품명']
    df_item_names = sorted(df_item_sum['제품'].unique())

    df_sum=df_cust_sum.groupby(['출고일자'])['수량'].sum()
    df_sum=pd.DataFrame(df_sum).reset_index()

def fontLoad():
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

def alt_chart_selection_multi(source, x='출고일자', y='수량', group='거래처코드', axis_scale="linear"):
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

def alt_chart_selection_single(source, x='출고일자', y='수량'):
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