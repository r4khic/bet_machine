import pymysql
import datetime
import dateparser


class GetData:
    """Connect to db and getting data"""

    def __init__(self):
        self.db = pymysql.connect(host='185.209.22.56',
                                  user='r4khic_pc',
                                  password='v0LBdb3mbhrqGNHA',
                                  db='bet_machine',
                                  charset='utf8',
                                  autocommit=True)
        self.cursor = self.db.cursor()

    def get_data(self):
        data_color = []
        data_time = []
        query = 'SELECT * FROM `wheel_results` LIMIT 5000'
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        for result in results:
            game_time_result = result[5]
            result = result[7]
            data_color.append(result)
            data_time.append(game_time_result)
        return data_color, data_time

    @staticmethod
    def generate_date():
        date_data = []
        day_delta = datetime.timedelta(days=1)
        start_date = dateparser.parse('2020-04-01').date()
        end_date = datetime.date.today()
        for i in range((end_date - start_date).days):
            date_result = (start_date + i * day_delta)
            date_data.append(date_result)
        return date_data

    def get_white_color_date(self):
        result_data = []
        sql = "select date(game_run_time), a.* From wheel_results a where game_result_color = 'white' And " \
                "game_run_time between '2020-04-01' and '2020-06-02' "
        query = "SELECT date(game_run_time) FROM `wheel_results` WHERE game_result_color = 'white' ORDER BY " \
                "game_run_time ASC "
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        for result in results:
            result_data.append(result[0])
        return result_data