# facebook_id, start_timestamp, end_timestamp, start_value, end_value
# 1514764800 => 2018-01-01 00:00
# 1546300800 => 2019-01-01 00:00
my_data = [
    ["11111111", 1514764800, 1546300800, 112.0, 100.0],
    ["22222222", 1519244967, 1526811200, 50.0, 40.0]
]


def find_by_fb_id(facebook_id, data):
    pass


# should return ["22222222", 1519244967, 1526811200, 50.0, 40.0]
print(
    find_by_fb_id("22222222", my_data)
)

#
# # TODO: calculate the actual value
# # use the find_by_fb_id function
# #
# # facebook_id is a string, can identify the facebook user
# # actual_timestamp is a linux timestamp (number of second elapsed from 1970-01-01 00:00 https://www.epochconverter.com/)
# # data is a similar structure like my_data
# def required_value(facebook_id, actual_timestamp, data):
#     pass
#
#
# # 1519862400 => 2018-03-01 00:00
# # ~110
# print(
#     required_value("11111111", 1519862400, my_data)
# )
#
#
#
# # 1527811200 => 2018-06-01 00:00
# # ~107
# print(
#     required_value("11111111", 1527811200, my_data)
# )
