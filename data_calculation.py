from getting_colors import GetData
from collections import Counter, OrderedDict


def main():
    data = GetData()
    # colors_data = data.get_data()  # contain 2 lists 0 index str,1 index datetime
    white_color_dates = data.get_white_color_date()
    compare(white_color_dates)


def compare(white_color_dates):
    s = Counter(white_color_dates)
    print(s)


def sort(colors_data):
    sorted_colors = Counter(colors_data[0])
    if sorted_colors['black'] == sorted_colors['red'] == sorted_colors['grey']:
        print('yes!!')


if __name__ == '__main__':
    main()
