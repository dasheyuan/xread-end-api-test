import datetime
import io
import sys

import pymysql.cursors
import xlwt


def setup_io():
    sys.stdout = sys.__stdout__ = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', line_buffering=True)
    sys.stderr = sys.__stderr__ = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8', line_buffering=True)


setup_io()


def test_mysql():
    # Connect to the database
    connection = pymysql.connect(host='120.79.33.170',
                                 port=33061,
                                 user='root',
                                 password='x123read456',
                                 db='dc_admin',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    count = 0
    except_count = 0
    except_log = []
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `mac` FROM `device`"
            cursor.execute(sql)
            result = cursor.fetchall()
            for mac in result:
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                before = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")
                sql = "SELECT * FROM `device_record` where (mac='{0}') and (login_time between '{1}' and '{2}' )". \
                    format(mac["mac"], before, now)
                cursor.execute(sql)
                result1 = cursor.fetchall()
                count += len(result1)
                city_list = []
                for record in result1:
                    city_list.append(record["city"])

                if len(set(city_list)) <= 1:
                    pass
                else:
                    except_count += 1
                    except_log.append(result1)
    finally:
        print("今天共有{0}条设备登录记录.".format(count))
        print("其中有{0}个设备登录异常:".format(except_count))

        if except_count > 0:
            i = 1
            for log in except_log:
                print("第{}个:".format(i))
                i += 1
                for x in log:
                    print(x)

            workbook = xlwt.Workbook(encoding='utf-8')
            # 创建一个worksheet
            worksheet = workbook.add_sheet('Sheet1')

            # 写入excel
            # 参数对应 行, 列, 值

            worksheet.write(0, 0, label="id")
            worksheet.write(0, 1, label="mac")
            worksheet.write(0, 2, label="city")
            worksheet.write(0, 3, label="app_key")
            worksheet.write(0, 4, label="login_time")
            worksheet.write(0, 5, label="update_time")
            worksheet.write(0, 6, label="create_time")

            i = 1
            x = 1
            for log in except_log:
                worksheet.write(x, 0, label="第{}个:".format(i))
                i += 1
                x += 1
                for item in log:
                    y = 0
                    for k in item:
                        if k == 'login_time' or k == 'update_time' or k == 'create_time':
                            style = xlwt.XFStyle()
                            style.num_format_str = 'YYYY-MM-D h:mm:ss'  # Other options: D-MMM-YY, D-MMM, MMM-YY, h:mm, h:mm:ss, h:mm, h:mm:ss, M/D/YY h:mm, mm:ss, [h]:mm:ss, mm:ss.0
                            worksheet.write(x, y, item[k], style)
                        else:
                            worksheet.write(x, y, item[k])
                        y += 1
                    x += 1

            # 保存
            filename = datetime.datetime.now().strftime("%Y-%m-%d")
            worksheet.col(1).width = 6000
            worksheet.col(2).width = 6000
            worksheet.col(3).width = 9000
            worksheet.col(4).width = 6000
            worksheet.col(5).width = 6000
            worksheet.col(6).width = 6000

            # workbook.save('/data/device_record/'+filename+'.xls')
            workbook.save('./' + filename + '.xls')
            connection.close()


test_mysql()