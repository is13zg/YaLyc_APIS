import datetime

import schedule


def cuckoo():
    dt = datetime.datetime.now()
    hour = datetime.datetime.timetuple(dt)[3]
    i = hour % 12 if hour % 12 else 12
    print("Ку" * i)


schedule.every().hour.at(":00").do(cuckoo)

while True:
    schedule.run_pending()
