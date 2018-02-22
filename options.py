import time
import datetime
from mongo_crud import register_plan_in_mongo


def help_msg(fb_id):
    return """
    examples:
    - register 100 2018-06-01 90
    """


# 2018-02-28
def parse_date(d):
    return round(time.mktime(datetime.datetime.strptime(d, "%Y-%m-%d").timetuple()))


def answer_message(fb_id, message):
    try:
        args = message.strip().split(" ")
        if args[0] == "register":
            return register(
                facebook_id=fb_id,
                actual_value=args[1],
                end_value=args[3],
                end_time=parse_date(args[2])
            )
        return help_msg(fb_id)
    except:
        help_msg(fb_id)


def register(facebook_id, actual_value, end_time, end_value):
    register_plan_in_mongo(facebook_id, round(time.time()), end_time, float(actual_value), float(end_value))
    return "Your plan has been registered"


def now(facebook_id, registered_list):
    actual_timestamp = time.time()
    fb_id, start_timestamp, end_timestamp, start_value, end_value = [d for d in registered_list if d[0] == facebook_id][
        0]
    period_length = end_timestamp - actual_timestamp
    point_in_period = actual_timestamp - start_timestamp
    required_value = ((end_value - start_value) * (point_in_period / period_length))
    pass
