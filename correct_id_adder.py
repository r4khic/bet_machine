import pymysql


def get_connect():
    db = pymysql.connect(host='185.209.22.56',
                         user='r4khic_pc',
                         password='v0LBdb3mbhrqGNHA',
                         db='bet_machine',
                         charset='utf8',
                         autocommit=True)
    cursor = db.cursor()
    return cursor


def get_query(connection):
    query = 'SELECT * FROM `wheel_results` ORDER BY `game_run_time` ASC'
    connection.execute(query)
    results = connection.fetchall()
    query_for_update = 'UPDATE `wheel_results` SET `correct_id` = "%s" WHERE `wheel_results`.`id` = %s'
    correct_id = 0
    for result in results:
        correct_id += 1
        id = result[0]
        connection.execute(query_for_update, (correct_id, id))
        print('update successfully !')


def main():
    connection = get_connect()
    get_query(connection)


if __name__ == '__main__':
    main()
