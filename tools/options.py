import time
import datetime


def register(facebook_id, actual_value, end_time, end_value, registered_list):
    actual_timestamp = time.time()
    end_timestamp = time.mktime(datetime.datetime.strptime(end_time, "%Y-%m-%d").timetuple())

    registered_list.append(
        (facebook_id, actual_timestamp, end_timestamp, actual_value, end_value)
    )
    return registered_list


def now(facebook_id, registered_list):
    actual_timestamp = time.time()
    fb_id, start_timestamp, end_timestamp, start_value, end_value = [d for d in registered_list if d[0] == facebook_id][0]
    period_length = end_timestamp - actual_timestamp
    point_in_period = actual_timestamp - start_timestamp
    required_value = ((end_value - start_value) * (point_in_period / period_length)) +
