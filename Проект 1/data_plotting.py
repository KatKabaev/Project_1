import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_and_save_plot(data, ticker, std_deviation, period=None, start_date: str=None, end_date=None, style=None,
                         filename=None) -> None:
    """
    Функция для создания и сохранения графика на основе данных о ценах акций.

    :param data: DataFrame с данными.
    :param ticker: Тикер акции.
    :param std_deviation: Стандартное отклонение цены закрытия.
    :param period: Период акции.
    :param start_date: Начальная дата анализа.
    :param end_date: Конечная дата анализа.
    :param style: Стиль для оформления графика.
    :param filename: Имя файла для сохранения графика.
    :return: Создает и сохраняет график.
    """

    plt.figure(figsize=(10, 8))
    if style:
        plt.style.use(style)

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()

            ax1 = plt.subplot2grid((8, 1), (0, 0), rowspan=5, colspan=1)
            ax2 = plt.subplot2grid((8, 1), (6, 0), rowspan=3, colspan=1)

            # Форматер для отображения дат
            formatter = mdates.DateFormatter('%d-%b-%y')
            ax1.xaxis.set_major_formatter(formatter)
            ax2.xaxis.set_major_formatter(formatter)

            ax1.plot(dates, data['Close'].values, label='Цена закрытия')
            ax1.plot(dates, data['Moving_Average'].values, label='Скользящее среднее')
            ax1.fill_between(dates, data['Close'].values - std_deviation, data['Close'].values + std_deviation,
                             color='lightblue', alpha=0.5, label='Стандартное отклонение')
            ax1.set_title(f"Цена акций {ticker}")
            ax1.set_ylabel("Цена")
            ax1.legend()

            # График RSI
            ax2.plot(dates, data['RSI'].values, label='RSI', color='b')
            ax2.axhline(70, color='r', linestyle='--')
            ax2.axhline(30, color='g', linestyle='--')
            ax2.set_title(f"RSI {ticker}")
            ax2.legend()

            if style is None:
                ax1.grid()
                ax2.grid()

            # plt.gcf().autofmt_xdate()
            plt.xlabel("Дата")

        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.plot(data['Date'], data['Close'], label='Close Price')
        plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')
        plt.fill_between(data['Date'], data['Close'] - std_deviation, data['Close'] + std_deviation,
                             color='lightblue', alpha=0.5, label='Стандартное отклонение')
        plt.plot(data['Date'], data['RSI'], label='RSI')

    if filename is None:
        if period is None:
            filename = f"{ticker}_{start_date}_to_{end_date}_stock_price_chart.png"
        else:
            filename = f"{ticker}_{period}_stock_price_chart.png"

    plt.savefig(filename)
    print(f"График сохранен как {filename}")

def show_interactive_plot(data, ticker, std_deviation, period=None):
    """
    Функция для создания и сохранения интерактивного графика на основе данных о ценах акций.

    :param data: DataFrame с данными.
    :param ticker: Тикер акции.
    :param std_deviation: Стандартное отклонение цены закрытия.
    :param period: Период акции.
    :return: Создает и сохраняет интерактивный график.
    """
    fig = make_subplots(rows=2, cols=1, subplot_titles=(
        f"Цена акций {ticker}",
        f"RSI {ticker}"
        ))

    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Цена закрытия'), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data['Moving_Average'], mode='lines', name='Скользящее среднее'),
                  row=1, col=1)
    fig.add_trace(
        go.Scatter(x=data.index, y=data['Close'] + std_deviation, mode='lines', name='Верхнее станд. откл.'), row=1, col=1)
    fig.add_trace(
        go.Scatter(x=data.index, y=data['Close'] - std_deviation, mode='lines', name='Нижнее станд. откл.',
                   fill='tonexty'), row=1, col=1)

    # График RSI
    fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], mode='lines', name='RSI'), row=2, col=1)
    fig.add_hline(y=70, line_dash="dot", line_color="red", row=2, col=1)
    fig.add_hline(y=30, line_dash="dot", line_color="green", row=2, col=1)

    fig.update_xaxes(title_text="Дата", row=2, col=1)

    filename = f"{ticker}_{period}_interactive_chart.html"

    # Сохранение графика в HTML и открытие его в браузере
    fig.write_html(filename)

    # Открытие графика в браузере
    fig.show()

    # Вывод сообщения об успешном создании графика
    print(f"График сохранен как {filename}")