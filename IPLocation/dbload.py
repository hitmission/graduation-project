
import os
import pymysql
import pandas as pd

# 1.连接 Mysql 数据库
try:
    conn = pymysql.connect(host='localhost', user='root', password='991208', db='ipdb', charset='utf8')
    cur = conn.cursor()
    print('数据库连接成功！')
    print(' ')
except:
    print('数据库连接失败！')

# 2.读取任意文件夹下的csv文件
# 获取程序所在路径及该路径下所有文件名称
path = os.getcwd()
files = os.listdir(path)
# files = os.listdir('C:\Users\MISS\PycharmProjects\IPLocation')
# 遍历所有文件
i = 0
for file in files:
    # 判断文件是不是csv文件
    if file.split('.')[-1] in ['csv']:
        i += 1
        # 构建一个表名称，供后期SQL语句调用
        filename = file.split('.')[0]
        filename = 'tab_' + filename

        # 使用pandas库读取csv文件的所有内容,结果f是一个数据框，保留了表格的数据存储方式，是pandas的数据存储结构。
        f = pd.read_csv(file, encoding='gbk')  # 注意：如果报错就改成 encoding='utf-8' 试试
        # print(f)

        # 3.计算创建字段名称和字段类型的 SQL语句片段

        # 3.1 获取数据框的标题行（即字段名称）,将来作为sql语句中的字段名称。
        columns = f.columns.tolist()
        # print(columns)

        # 3.2 将csv文件中的字段类型转换成mysql中的字段类型
        types = f.ftypes
        field = []  # 用来接收字段名称的列表
        table = []  # 用来接收字段名称和字段类型的列表
        for item in columns:
            if 'int' in types[item]:
                char = item + ' INT'
            elif 'float' in types[item]:
                char = item + ' FLOAT'
            elif 'object' in types[item]:
                char = item + ' VARCHAR(255)'
            elif 'datetime' in types[item]:
                char = item + ' DATETIME'
            else:
                char = item + ' VARCHAR(255)'
            table.append(char)
            field.append(item)

        # 3.3 构建SQL语句片段
        # 3.3.1 将table列表中的元素用逗号连接起来，组成table_sql语句中的字段名称和字段类型片段，用来创建表。
        tables = ','.join(table)
        # print(tables)

        # 3.3.2 将field列表中的元素用逗号连接起来，组成insert_sql语句中的字段名称片段，用来插入数据。
        fields = ','.join(field)  # 字段名
        # print(fields)

        # 4. 创建数据库表
        # 4.1 #如果数据库表已经存在，首先删除它
        cur.execute('drop table if exists {};'.format(filename))
        conn.commit()

        # 4.2 构建创建表的SQL语句
        table_sql = 'CREATE TABLE IF NOT EXISTS ' + filename + '(' + 'id0 int PRIMARY KEY NOT NULL auto_increment,' + tables + ');'
        # print('table_sql is: ' + table_sql)

        # 4.3 开始创建数据库表
        print('表:' + filename + ',开始创建…………')
        cur.execute(table_sql)
        conn.commit()
        print('表:' + filename + ',创建成功!')

        # 5.向数据库表中插入数据
        print('表:' + filename + ',开始插入数据…………')

        # 5.1 将数据框的数据读入列表。每行数据是一个列表，所有数据组成一个大列表。也就是列表中的列表，将来可以批量插入数据库表中。
        values = f.values.tolist()  # 所有的数据
        # print(values)

        # 5.2 计算数据框中总共有多少个字段，每个字段用一个 %s 替代。
        s = ','.join(['%s' for _ in range(len(f.columns))])
        # print(s)

        # 5.3 构建插入数据的SQL语句
        insert_sql = 'insert into {}({}) values({})'.format(filename, fields, s)
        # print('insert_sql is:' + insert_sql)

        # 5.4 开始插入数据
        cur.executemany(insert_sql, values)  # 使用 executemany批量插入数据
        conn.commit()
        print('表:' + filename + ',数据插入完成！')
        print(' ')
cur.close()  # 关闭游标
conn.close()  # 关闭数据库连接
print('任务完成！共导入 {} 个CSV文件。'.format(i))        




