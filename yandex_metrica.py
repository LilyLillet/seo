import datetime as dt
from tapi_yandex_metrika import YandexMetrikaStats
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

ACCESS_TOKEN = "y0_AgAAAAAcHHSnAAn5BwAAAADkLufyJuEybIf_RdWn8OL6e4aj42R5JX0"
COUNTER_ID = "88227360"

client = YandexMetrikaStats(access_token=ACCESS_TOKEN)

start_date = '2023-05-01'
# input("Начальная дата отчета в формате YYYY-mm-dd: ")
end_date = '2023-05-31'


# input("Конечная дата отчета в формате YYYY-mm-dd: ")


def get_traffic_source_report():
    params = dict(
        ids=COUNTER_ID,
        date1=start_date,
        date2=end_date,
        metrics="ym:s:visits",
        dimensions="ym:s:SearchEngineRoot",
        lang="en",
    )
    report = client.stats().get(params=params)
    result = report().to_values()
    df = pd.DataFrame(result, columns=['Поисковая система', 'Визиты'])
    df.groupby('Поисковая система').sum().plot(kind='pie', y='Визиты')
    ## Не понимаю пока как отформатировать круговую диаграмму и выгрузить ее

    total_sum = 0
    for i in result:
        total_sum = total_sum + float(i[1])
    df = pd.DataFrame(result, columns=['Поисковая система', 'Визиты'])
    df.loc[len(df.index)] = ['Итого', total_sum]
    df.drop(labels=[2, 3, 4, 5, 6, 7], axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)
    print(df)
    df.to_csv('DataFrame_without_index.csv', sep='\t', encoding='Windows-1251', index=False)


def get_visits_comparison_to_previous_periods_report():
    params = dict(
        ids=COUNTER_ID,
        date1='2023-01-01',
        date2='2023-05-31',
        metrics="ym:s:visits",
        dimensions="ym:s:SearchEngineRoot",
        lang="en",
    )
    report = client.stats().get(params=params)
    result = report().to_values()
    df = pd.DataFrame(result, columns=['Поисковая система', 'Визиты'])
    print(df)

def get_qty_visits_report():
    params = dict(
        ids=COUNTER_ID,
        date1=start_date,
        date2=end_date,
        metrics="ym:s:visits",
        dimensions="ym:s:date, ym:s:isRobot",
        sort="ym:s:date",
        lang="en",
    )
    report = client.stats().get(params=params)

    result = report().to_values()
    print(result)
    print(type(result))

    df = pd.DataFrame(result, columns=['ym:s:date', 'ym:s:isRobot', 'ym:s:visits'])
    print(df)

    sns.set(style='whitegrid', rc={'figure.figsize': (12, 4)})
    barplot = sns.barplot(x='ym:s:date', y='ym:s:visits', hue='ym:s:isRobot', data=df)
    barplot.axes.set_title("Распределение роботов и пользователей по дням", fontsize=16)
    barplot.set_xlabel("Дата", fontsize=14)
    barplot.set_ylabel("Визиты", fontsize=14)

    plt.legend(title="Тип пользователя")
    plt.xticks(
        rotation=45,
        horizontalalignment='right',
        fontweight='light',
        fontsize='12'
    )
    plt.show()
