from mongo_crud import get_stat

import matplotlib.pyplot as plt
import datetime
import uuid


def stat_pic(facebook_id):
    my_stat = sorted(list(get_stat(facebook_id)), key=lambda x: x["timestamp"])

    for s in my_stat:
        print(s)

    def readable(_ts):
        return datetime.datetime.fromtimestamp(
            int(_ts)
        ).strftime('%Y-%m-%d')

    ts = [readable(s["timestamp"]) for s in my_stat]
    values = [s["value"] for s in my_stat]

    filename = "plot-{}.png".format(uuid.uuid4())

    plt.plot(ts, values)
    plt.savefig(filename)

    return filename
