import yfinance as yf
import pandas_ta as pta
import pandas as pd


def fetch_stock_data(ticker, period='1mo'):
    '''
    :param ticker: тикер акции
    :param period: период акции
    :return: DataFrame с историческими данными об акциях для указанного тикера и временного периода
    '''
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


def add_moving_average(data, window_size=5):
    '''
    Добавляет в DataFrame колонку со скользящим средним, рассчитанным на основе цен закрытия.
    :param data: DataFrame с данными
    :param window_size: количество точек данных, используемых для вычисления скользящего среднего
    :return: DataFrame с колонкой со скользящим средним
    '''
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data

def calculate_and_display_average_price(data):
    '''
    Функция для расчёта средней цены закрытия акций.
    :param data: DataFrame с данными
    :return: средняя цена закрытия акции
    '''
    average_price = round(data['Close'].mean(), 2)
    return average_price

def notify_if_strong_fluctuations(data, threshold=10):
    '''
    Анализирует данные и уведомляет пользователя, если цена акций колебалась более чем на заданный процент за период.
    :param data: DataFrame с данными
    :param threshold: Заданный порог (по умолчанию 10%)
    :return: Уведомление о колебании цены закрытия акции
    '''

    max_value = max(data['Close'])
    min_value = min(data['Close'])

    difference = max_value - min_value
    percentage_change = (difference / min_value) * 100

    if percentage_change > threshold:
        print("Сильные колебания! Изменения превышают заданный порог на {:.2f}%".format(percentage_change))
        return True
    else:
        print("Колебания в пределах нормы.")
        return False

def export_data_to_csv(data, filename):
    '''
    Сохраняет DataFrame с данными об акциях в CSV файл.
    :param data: DataFrame с данными
    :param filename: Название для csv-файла
    :return: Csv-файл с данными об акциях
    '''
    data.to_csv(filename, index=False)
    print(f'Данные загружены в csv-файл "{filename}"')


def calculate_rsi(data):
    '''
    Функции для расчёта и отображения на графике дополнительных технических индикаторов (RSI)
    :param data: DataFrame с данными
    :return: DataFrame с колонкой с RSI
    '''
    data['rsi'] = pta.rsi(data['Close'], 2)
    return data
