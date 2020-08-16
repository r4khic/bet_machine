import pymysql
import csv


def get_connect():
    db = pymysql.connect(host='185.209.22.56',
                         user='r4khic_pc',
                         password='v0LBdb3mbhrqGNHA',
                         db='bet_machine',
                         charset='utf8',
                         autocommit=True)
    cursor = db.cursor()
    return cursor


def calculate_data_for_colors(connection):
    colors_id = []
    query = 'SELECT correct_id FROM `wheel_results` LIMIT 10'
    connection.execute(query)
    results = connection.fetchall()
    for result in results:
        plus_result_id = result[0] + 8
        plus_result_id1 = result[0] + 9
        colors_id.append(plus_result_id)
        colors_id.append(plus_result_id1)
    return colors_id


def get_data(connection, colors_id):
    data = []
    query = 'SELECT * FROM `wheel_results` WHERE id = %s LIMIT 10'
    for color_id in colors_id:
        connection.execute(query, color_id)
        result = connection.fetchall()
        print(result)
        data.append(result)
    return data


def csv_write(data):
    with open('wheel_data.csv', 'w') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)
    print('all is ok')


def main():
    connection = get_connect()
    colors_id = calculate_data_for_colors(connection)
    data = get_data(connection, colors_id)
    csv_write(data)


if __name__ == '__main__':
    main()
