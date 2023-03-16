from datetime import datetime

def average_calculator(traffic_average_counts):
    total_items = 0
    nominator = 0
    for key in traffic_average_counts.keys():
        nominator += int(key)*traffic_average_counts[key]
        total_items += traffic_average_counts[key]
    return round(nominator/total_items, )


def traffic_counter(present_cars_count, previous_time, previous_cars_count):

    if not present_cars_count > 0 or not previous_cars_count > 0:
        print("No Traffic")
        return True, 0
    # print("Present Cars", present_cars_count)
    # print("Previous Cars", previous_cars_count)
    # print("Seconds Passed", seconds_passed)

    # difference of cars in present and past frame
    cars_diff = present_cars_count - previous_cars_count

    if cars_diff <= 0:
        print("Red Traffic")
        return True, 2

    if cars_diff <= 2:
        print("Yellow Traffic")
        return True, 1

    print("No Traffic")
    return True, 0