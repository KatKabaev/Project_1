import yfinance as yf
import pandas_ta as pta


def fetch_stock_data(ticker, period, start_date=None, end_date=None):
    """
    Функция для получения исторических данных о ценах акций.

    :param ticker: Тикер акции.
    :param start_date: Начальная дата анализа.
    :param end_date: Конечная дата анализа.
    :param period: Период акции.
    :return: DataFrame с историческими данными об акциях для указанного тикера и временного периода.
    """

    stock = yf.Ticker(ticker)

    if start_date is not None:
        data = stock.history(start=start_date, end=end_date)
    else:
        data = stock.history(period=period)
    return data


def add_moving_average(data, window_size=5):
    """
    Добавляет в DataFrame колонку со скользящим средним, рассчитанным на основе цен закрытия.

    :param data: DataFrame с данными
    :param window_size: количество точек данных, используемых для вычисления скользящего среднего
    :return: DataFrame с колонкой со скользящим средним
    """
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data

def calculate_average_price(data):
    """
    Функция для расчёта средней цены закрытия акций.

    :param data: DataFrame с данными.
    :return: Средняя цена закрытия акции.
    """
    average_price = round(data['Close'].mean(), 2)
    print(f'Средняя цена закрытия акций за заданный период: {average_price}')
    return average_price

def notify_if_strong_fluctuations(data, threshold=10):
    """
    Функция уведомляет пользователя, если цена акций колебалась более чем на заданный процент за период.

    :param data: DataFrame с данными.
    :param threshold: Заданный порог (по умолчанию 10%).
    :return: Уведомление о колебании цены закрытия акции.
    """

    max_value = data['Close'].max()
    min_value = data['Close'].min()

    difference = max_value - min_value
    percentage_change = (difference / min_value) * 100

    if percentage_change > threshold:
        print("Сильные колебания! Изменения превышают заданный порог на {:.2f}%".format(percentage_change))
        return True
    else:
        print("Колебания в пределах нормы.")
        return False

def export_data_to_csv(data, filename):
    """
    Сохраняет DataFrame с данными об акциях в CSV-файл.

    :param data: DataFrame с данными.
    :param filename: Название для csv-файла.
    :return: Csv-файл с данными об акциях.
    """

    data.to_csv(filename, index=False)
    print(f'Данные загружены в csv-файл "{filename}"')


def calculate_rsi(data):
    """
    Функции для расчёта и отображения на графике дополнительных технических индикаторов (RSI).

    :param data: DataFrame с данными.
    :return: DataFrame с колонкой с RSI.
    """

    data['RSI'] = pta.rsi(data['Close'], 2)
    return data

def calculate_standard_deviation(data):
    """
    Функция для расчета стандартного отклонения цены закрытия акции.

    :param data: DataFrame с данными.
    :return: Стандартное отклонение цены закрытия акции.
    """
    std_deviation = data['Close'].std(ddof=1)
    print(f'Стандартное отклонение цены закрытия: {round(std_deviation, 2)}')
    return std_deviation
