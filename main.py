import matplotlib.pyplot as plt
from collections import Counter
import scipy.stats as stats
import pandas as pd
import numpy as np

def read_data():
    file = 'loto.xls'
    df = pd.read_excel(file)
    df_matrix = df.as_matrix()
    df_matrix = np.int_(df_matrix)
    df_matrix = [checker(d) for d in df_matrix]
    return np.array(df_matrix)

def checker(d_arr):
    tmp = []
    for i in d_arr:
        if i < 0:
            tmp.append(i)
        else:
            tmp.append(i % 100)
    return tmp

def get_rows(data, s_row = 0, e_row = 1):
    return data[s_row:e_row]

def get_columns(data, s_col = 0, e_col = 12):
    cols = [np.array(d)[s_col:e_col] for d in data]
    cols = data_concate(cols)
    return cols

def data_concate(data):
    concate = np.concatenate(data)
    concate = np.array([num for num in concate if num >= 0])
    return concate

def plot_data(data):
    counter = Counter(data)
    labels, values = zip(*counter.items())
    indexes = np.arange(len(labels))
    width = 0.5
    plt.xlabel('Numbers')
    plt.ylabel('Frequence')
    plt.bar(indexes, values, width)
    plt.xticks(indexes + width * 0.5, labels)
    plt.show()

def get_top_loto(data, n_top = 3):
    counter = Counter(data).most_common(n_top)
    labels, values = zip(*counter)
    return np.array(labels)

def loto_lost_func(loto_arr, rs = 0, price = 0):
    total = - price * len(loto_arr)
    if rs in loto_arr:
        total = total + price * 70
    return total

def total_lost(test_data, loto_arr = None, price = 0):
    total = 0
    for rs in test_data:
        total += loto_lost_func(loto_arr, rs=rs, price=price)
    return total

def total_with_previous(test_data, price, n_days, n_top):
    if n_days >= len(test_data):
        return 0
    total_score = 0
    for i in range(0, len(test_data) - n_days):
        train_loto = data_concate([test_data[i: i+n_days]])
        top_loto = get_top_loto(train_loto, n_top=n_top)
        test_loto = np.array([test_data[i + n_days]])
        total_score += total_lost(test_data=test_loto, loto_arr=top_loto, price=price)
    return total_score

def get_data_range(s_year, e_year):
    data = read_data()
    data = get_rows(data, s_year * 31 + 1, e_year * 31 - 1)
    return data_concate(data)

if __name__ == '__main__':
    # train_all = get_data_range(s_year=0, e_year=14)
    # test_all = get_data_range(s_year=14, e_year=15)
    #
    # # plot_data(train_all)
    #
    # loto_arr = get_top_loto(train_all, n_top=5)
    #
    # lost = total_lost(test_data=test_all, loto_arr=loto_arr, price=2000)
    # print lost
    #
    # lost = total_with_previous(test_data=test_all, price=2000, n_days=200, n_top=2)
    # print lost

    data = read_data()
    data_1d = data_concate(get_rows(data, 0, 31))
    plot_data(data_1d)
    