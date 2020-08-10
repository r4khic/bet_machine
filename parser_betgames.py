import json
import requests
import pymysql
import datetime
import dateparser


def get_response(url):
    response = requests.get(url)
    return response


def parse_json(response):
    game_results = []
    games_run_id = []
    json_result = json.loads(response.text)
    for array in json_result['items'].items():
        if 'results' == array[0]:
            for elem in array[1]:
                if elem['game_id'] in '7':
                    data_array = elem['results']
                    if len(data_array) != 0:
                        data = data_array[0]
                        game_id = elem['game_id']
                        run_id = elem['id']
                        game_video_url = elem['video_url']
                        game_name = elem['game_name']
                        run_time = elem['run_time']
                        number_result = data['number']
                        color = data['color']
                        games_run_id.append(run_id)
                        game_results.append((
                            run_id,
                            game_id,
                            game_name,
                            game_video_url,
                            run_time,
                            number_result,
                            color
                        ))
    return game_results, games_run_id


def get_connect():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='',
                         db='bet_machine',
                         charset='utf8',
                         port='3306',
                         autocommit=True)
    cursor = db.cursor()
    return cursor


def insert_data(connection, game_results):
    query = 'INSERT INTO `wheel_results`(`game_run_id`, `game_id`, `game_name`, `game_video_url`,`game_run_time`, ' \
            '`game_number_result`, `game_result_color`) VALUES (%s,%s,%s,%s,%s,%s,%s) '
    connection.executemany(query, game_results)


def generate_date():
    date_data = []
    day_delta = datetime.timedelta(days=1)
    start_date = dateparser.parse('2020-04-01').date()
    end_date = datetime.date.today()
    for i in range((end_date - start_date).days):
        date_result = (start_date + i * day_delta)
        date_data.append(date_result)
    return date_data


def check_duplicate_game(connection, games_results):
    for game_run_id in games_results[1]:
        query = 'SELECT `game_run_id` FROM `wheel_results` WHERE `game_run_id` = %s'
        connection.execute(query, game_run_id)
        result = connection.fetchone()
        if result is None:
            return False
        else:
            return True


def main():
    pattern = 'https://betgames9.betgames.tv/web/v2/games/results/testpartner/en/0/{}/0/{}/'
    connection = get_connect()
    dates = generate_date()
    for date in dates:
        for i in range(225):  # max pages 224
            url = pattern.format(str(date), str(i))
            response = get_response(url)
            print(type(response))
            game_results = parse_json(response)
            check_game_run_id = check_duplicate_game(connection, game_results)
            if check_game_run_id:
               print('duplicate')
               continue
            if len(game_results) == 2:
                print('inserted')
                insert_data(connection, game_results[0])
                game_results = []
    print('script finished!')


if __name__ == '__main__':
    main()