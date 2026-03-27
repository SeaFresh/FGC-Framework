from datetime import timedelta, timezone


def get_na_timezone_spread(start_time):
    eastern_offset = 5
    na_timezone_list = ["EST", "CST", "MST", "PST"]

    start_time = start_time.astimezone(timezone(-timedelta(hours=eastern_offset)))
    start_time_format = start_time.strftime("%I:%M%p").lower()
    start_time_format = start_time_format.removeprefix("0")
    timezone_spread = start_time_format + " " + na_timezone_list[0] + " ("
    curr_timezone = eastern_offset + 1

    while curr_timezone != eastern_offset + len(na_timezone_list):
        time = start_time.astimezone(timezone(-timedelta(hours=curr_timezone))).strftime("%I:%M%p").lower()
        time = time.removeprefix("0")
        timezone_spread += time
        timezone_spread += " " + na_timezone_list[curr_timezone - eastern_offset]
        curr_timezone = curr_timezone + 1
        if curr_timezone != eastern_offset + len(na_timezone_list):
            timezone_spread += ", "
    
    timezone_spread += ")"
    timezone_spread = timezone_spread.replace(":00", "")
    return timezone_spread

def get_emea_timezone_spread(start_time):
    cent_euro_offset = 2

    start_time = start_time.astimezone(timezone(timedelta(hours=cent_euro_offset)))
    start_time_format = start_time.strftime("%I:%M%p").lower()
    start_time_format = start_time_format.removeprefix("0")
    timezone_spread = start_time_format + " CET ("
    time = start_time.astimezone(timezone(timedelta(hours=0))).strftime("%I:%M%p").lower()
    time = time.removeprefix("0")
    timezone_spread += time
    timezone_spread += " GMT)"
    timezone_spread = timezone_spread.replace(":00", "")
    return timezone_spread