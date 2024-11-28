import datetime

date1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
date2 = '2023-05-15 14:30:00'

dt1 = datetime.datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
dt2 = datetime.datetime.strptime(date2, '%Y-%m-%d %H:%M:%S')

if dt1 > dt2:
    print(dt1)
    print(dt2)
    print("date1 больше date2")
elif dt1 < dt2:
    print(dt1)
    print(dt2)
    print("date1 меньше date2")
else:
    print(dt1)
    print(dt2)
    print("date1 равно date2")