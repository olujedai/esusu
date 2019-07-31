from datetime import datetime
import arrow

def in_this_month(date_time_obj):
	return date_time_obj.month == datetime.today().month

def in_the_past(date_obj):
	return arrow.get(date_obj, 'Africa/Lagos').date() < arrow.now('Africa/Lagos').date()

def shift_by(arrow_date_time_obj, week_shift=4):
	return arrow_date_time_obj.shift(weeks=+week_shift)

def get_max_end_date_time(arrow_date_time_obj, maximum_capacity, week_shift=4):
	week_shift = maximum_capacity * week_shift
	return arrow_date_time_obj.shift(weeks=+week_shift)
