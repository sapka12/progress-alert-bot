import time
import datetime
from mongo_crud import register_plan_in_mongo, save_progress, registered_plan_in_mongo, planned_values
from chart import stat_pic

IMAGE_PREFIX = "img:"

date_format = "%Y-%m-%d"


def actual_timestamp():
    return round(time.time())


def help_msg():
    return """
    version: 0.1.5.test.3
    
    examples:
    - Register 100 2018-06-01 90
      (register <actual weight> <plan end date> <planned weight>)
    - 89.9
      (a float input, represents the actual weight)
    - Stat
      (tell you the actual expected value for the progress)
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


def stat(fb_id):
    ts_now = actual_timestamp()
    val_actual = planned_values(fb_id, ts_now)
    return "your planned weigth for today is: {} kg".format(val_actual)


def register(facebook_id, actual_value, end_time, end_value):
    register_plan_in_mongo(facebook_id, actual_timestamp(), end_time, float(actual_value), float(end_value))
    return "Your plan has been registered"


def answer_message(fb_id, message):
    try:
        args = message.strip().split(" ")
        if args[0].lower() == "register":
            return [
                register(
                    facebook_id=fb_id,
                    actual_value=args[1],
                    end_value=args[3],
                    end_time=parse_date(args[2])
                )
            ]
        if args[0].lower() == "stat":
            return [
                stat(fb_id)
            ]
        if is_float(args[0].replace(",", ".")):
            return [
                save_actual_weight(fb_id, float(args[0])),
                stat(fb_id),
                IMAGE_PREFIX + stat_pic(fb_id)
            ]

        return [help_msg()]
    except:
        return [help_msg()]
