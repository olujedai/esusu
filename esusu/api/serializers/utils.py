from datetime import datetime
import arrow

def this_month():
	return datetime.today().month

def in_the_past(date_obj):
	return arrow.get(date_obj, 'Africa/Lagos').date() < arrow.now('Africa/Lagos').date()

def shift_by(arrow_date_time_obj, week_shift=4):
	return arrow_date_time_obj.shift(weeks=+week_shift)

def get_max_end_date_time(arrow_date_time_obj, maximum_capacity, week_shift=4):
	week_shift = maximum_capacity * week_shift
	return arrow_date_time_obj.shift(weeks=+week_shift)

def tenure_deadline_passed(inviter, date):
    if inviter.society.tenures.count():
        current_tenure = inviter.society.active_tenure
        if current_tenure:
            return date > current_tenure.tentative_end_date and date < current_tenure.maximum_end_date
    return False

def todays_date():
    return arrow.now('Africa/Lagos').date()
