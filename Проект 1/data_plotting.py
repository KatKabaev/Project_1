import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates


def create_and_save_plot(data, ticker, std_deviation, period=None, start_date=None, end_date=None, style=None,
                         filename=None) -> None:
    """
    Функция для создания и сохранения графика на основе данных о ценах акций.

    :param data: DataFrame с данными
    :param ticker: Тикер акции.
    :param std_deviation: Стандартное отклонение цены закрытия.
    :param period: Период акции.
    :param start_date: Начальная дата анализа.
    :param end_date: Конечная дата анализа.
    :param style: Стиль для оформления графика.
    :param filename: Имя файла для сохранения графика.
    :return: Создает и сохраняет график
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

            ax2.plot(dates, data['RSI'].values, label='RSI', color='g')
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
