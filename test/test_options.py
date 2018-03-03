import unittest
from tools.options import Options


class MongoCrud:
    def hello(self):
        return ""

    def register_plan_in_mongo(self, facebook_id, actual_timestamp, end_timestamp, actual_value, end_value):
        print("register_plan_in_mongo", facebook_id, actual_timestamp, end_timestamp, actual_value, end_value)

    def registered_plan_in_mongo(self, facebook_id):
        print("registered_plan_in_mongo", facebook_id)

        return 0

    def planned_values(self, fb_id, ts, plan):
        print("planned_values", fb_id, ts, plan)
        return 0

    def save_progress(self, facebook_id, _timestamp, _value):
        print("save_progress", facebook_id, _timestamp, _value)


class MyTestCase(unittest.TestCase):
    def test_random_msg(self):
        fb_id = 1234
        request = "?"

        opt = Options(MongoCrud())
        response = opt.answer_message(fb_id, request)

        expected = "version:"
        first_line = response[0].split("\n")[1].strip()[:len(expected)]

        self.assertEquals(first_line, expected)

    def test_register(self):
        fb_id = 1234
        request = "Register 100 2018-06-01 90"

        opt = Options(MongoCrud())
        response = opt.answer_message(fb_id, request)

        expected = "Your plan has been registered"
        self.assertEquals(response[0], expected)

    def test_stat(self):
        fb_id = 1234
        request = "Stat"

        opt = Options(MongoCrud())
        response = opt.answer_message(fb_id, request)

        expected = "your planned weigth for today is: 0 kg"
        self.assertEquals(response[0], expected)

    def test_new_value(self):
        fb_id = 1234
        request = "50.5"

        opt = Options(MongoCrud())
        response = opt.answer_message(fb_id, request)

        expected = "OK, you are {} kg today".format(request)
        self.assertEquals(response[0], expected)


if __name__ == '__main__':
    unittest.main()
