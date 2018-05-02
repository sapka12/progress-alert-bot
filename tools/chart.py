import matplotlib

matplotlib.use('Agg')

from tools.mongo_crud import MongoCrud

import matplotlib.pyplot as plt
import datetime
import uuid


class Chart(MongoCrud):

    def stat_pic(self, facebook_id):
        print("Chart.stat_pic", facebook_id)

        plan = MongoCrud().registered_plan_in_mongo(facebook_id)

        plan_start = plan["actual_timestamp"]

        my_stat = [s for s in sorted(list(MongoCrud().get_stat(facebook_id)), key=lambda x: x["timestamp"])
                   if s["timestamp"] >= plan_start]

        def readable(_ts):
            return datetime.datetime.fromtimestamp(
                int(_ts)
            ).strftime('%Y-%m-%d')

        ts = [readable(s["timestamp"]) for s in my_stat]
        values = [float(s["value"]) for s in my_stat]

        filename = "plot-{}.png".format(uuid.uuid4())


        planned_vals = [float(MongoCrud().planned_values(facebook_id, s["timestamp"], plan)) for s in my_stat]

        print("ts", ts)
        print("values", values)
        print("planned_vals", planned_vals)

        plt.plot(ts, values)
        plt.plot(ts, planned_vals)
        plt.savefig(filename)

        print("saved:", filename)
        return filename
