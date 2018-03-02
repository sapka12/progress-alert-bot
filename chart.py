from mongo_crud import get_stat
from mongo_crud import planned_values, registered_plan_in_mongo

import matplotlib.pyplot as plt
import datetime
import uuid
import matplotlib

matplotlib.use('Agg')


def stat_pic(facebook_id):
    my_stat = sorted(list(get_stat(facebook_id)), key=lambda x: x["timestamp"])

    def readable(_ts):
        return datetime.datetime.fromtimestamp(
            int(_ts)
        ).strftime('%Y-%m-%d')

    ts = [readable(s["timestamp"]) for s in my_stat]
    values = [s["value"] for s in my_stat]

    filename = "plot-{}.png".format(uuid.uuid4())

    plan = registered_plan_in_mongo(facebook_id)
    planned_vals = [planned_values(s["timestamp"], plan) for s in my_stat]

    plt.plot(ts, values)
    plt.plot(ts, planned_vals)
    plt.savefig(filename)

    return filename
