
# Calculate average traffic number
# 0:    Green
# 1:    Yellow
# 2:    Red

def average_calculator(traffic_average_counts):
    total_items = 0
    nominator = 0
    for key in traffic_average_counts.keys():
        nominator += int(key)*traffic_average_counts[key]
        total_items += traffic_average_counts[key]
    return round(nominator/total_items, )

