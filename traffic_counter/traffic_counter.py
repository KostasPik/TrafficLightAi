from datetime import datetime


def traffic_counter(present_cars_count, previous_time, previous_cars_count, first_frame):
    present_time = datetime.now()

    # get time difference in seconds
    seconds_passed = (present_time - previous_time).seconds

    # if time difference between counts is less than 3 don't jump to conclusions about traffic
    if not seconds_passed >= 3:
        return False

    # if we didn't have any vehicles in previous frame don't jump to conclusions about traffic
    if first_frame:
        return True

    if not present_cars_count > 0 or not previous_cars_count > 0:
        print("No Traffic")
        return True
    # print("Present Cars", present_cars_count)
    # print("Previous Cars", previous_cars_count)
    # print("Seconds Passed", seconds_passed)

    # difference of cars in present and past frame
    cars_diff = present_cars_count - previous_cars_count

    if cars_diff <= 0:
        print("Red Traffic")
        return True

    if cars_diff <= 2:
        print("Yellow Traffic")
        return True

    print("No Traffic")
    return True
