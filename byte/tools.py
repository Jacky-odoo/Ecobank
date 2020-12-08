from datetime import datetime


def date_to_string(date=False, datetimes=False):
    date1, date2 = False, False
    if date:
        date_dt = datetime.strptime(date, '%Y-%m-%d')
        day = date_dt.day
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]
        date1 = str(date_dt.day) + suffix + date_dt.strftime("%B") + " " + str(date_dt.year)
    if datetimes:
        datetime_dt = datetime.strptime(datetimes, '%Y-%m-%d %H:%M:%S')
        day = datetime_dt.day
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]
        date2 = datetime_dt.strftime("%A") + " "+str(datetime_dt.day)+suffix+" "+datetime_dt.strftime("%B")+", " + str(datetime_dt.year)
    return [date1, date2]
