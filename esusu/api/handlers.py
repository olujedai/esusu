from .models.collection_schedule import CollectionSchedule
import arrow


def get_new_tentative_end_date(date):
    return arrow.get(date, 'Africa/Lagos').shift(weeks=+4).date()

def user_joined_society_handler(sender, **params):
    """signal intercept for user_joined_society"""
    user = params['user']
    newest_tenure = user.society.tenures.order_by('-start_date').first()
    if newest_tenure:
        if newest_tenure.is_active() or newest_tenure.starts_soon():
            last_collection = newest_tenure.collection_schedules.order_by('-collection_date').first()
            new_tentative_end_date = get_new_tentative_end_date(last_collection.collection_date)
            newest_tenure.tentative_end_date = new_tentative_end_date
            newest_tenure.save()
            new_schedule = CollectionSchedule(
				user=user,
				collection_date=new_tentative_end_date,
				tenure=newest_tenure,
            )
            new_schedule.save()
