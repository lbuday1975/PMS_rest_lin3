import pyodbc, flask

lv_odbc_conn = pyodbc.connect('Driver={/opt/sdb/MaxDB/lib/libsdbodbc.so}'
                          'Server=lnwts1;'
                          'Database=PMS;'
                          'UID=BWB_ADM;'
                          'PWD=BALETT')

lv_cursor = lv_odbc_conn.cursor()
lv_cursor.execute('SELECT * FROM SYS_DEF')
for lv_item in lv_cursor:
    print('TEST:' + lv_item[2] + ' ' + lv_item[3] )

lv_cursor.close()
lv_odbc_conn.close()