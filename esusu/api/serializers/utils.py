from datetime import datetime

def in_this_month(date_time_obj):
    return date_time_obj.month == datetime.today().month
