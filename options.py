import time
import datetime
from mongo_crud import register_plan_in_mongo, save_progress

date_format = "%Y-%m-%d"


def help_msg():
    return """
    version: 0.1.1
    
    examples:
    - register 100 2018-06-01 90
      (register <actual weight> <plan end date> <planned weight>)
    - 89.9
      (a float input, represents the actual weight)
    """


# 2018-02-28
def parse_date(d):
    return round(time.mktime(datetime.datetime.strptime(d, date_format).timetuple()))


def is_float(f):
    try:
        float(f)
        return True
    except:
        return False


def save_actual_weight(fb_id, weight):
    save_progress(fb_id, actual_timestamp(), weight)
    return "OK, you are {} kg today".format(weight)


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
        if is_float(args[0]):
            return save_actual_weight(fb_id, float(args[0]))

        return help_msg()
    except:
        help_msg()


def actual_timestamp():
    return round(time.time())


def register(facebook_id, actual_value, end_time, end_value):
    register_plan_in_mongo(facebook_id, actual_timestamp(), end_time, float(actual_value), float(end_value))
    return "Your plan has been registered"
