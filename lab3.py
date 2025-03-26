import re
from collections import Counter, defaultdict
from datetime import datetime
import pandas as pd

def report(data):
    data.sort(key=lambda x: x[0])
    hourly_logs = defaultdict(Counter)

    for row in data:
        t, l, n, m, ID = row
        hour = datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f").strftime("%H:00 - %H:59")
        hourly_logs[hour][l] += 1

    for hour, counts in hourly_logs.items():
        print(f"{hour} | " + " | ".join(f"{level}: {count}" for level, count in sorted(counts.items())))
def sub_timestamps(s1, s2):
    time_format = "%Y-%m-%d %H:%M:%S.%f"
    d1 = datetime.strptime(s1, time_format)
    d2 = datetime.strptime(s2, time_format)

    return d1 - d2


csv_gen = (row for row in open('server.log', "r"))
pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) (\w+) \[(\w+)\] (.+) \(ID: (\d+)\)'

timestamp, log_level, module_name, message, id = [], [], [], [], []
data = []

for line in csv_gen:
    match = re.match(pattern, line)
    if match:
        t, l, n, m, ID = match.groups()
        data.append([t, l, n, m, ID])
    else:
        print(f"Corrupted line: {line}")
# print(data)

c_log_level = Counter(data[1])
c_module_name = Counter(data[2])

print(f"Log levels: {c_log_level}")
print(f"Top 3 most active modules: {c_module_name.most_common(3)}")
ts = [d[0] for d in data]
print(f"Time between first ts {max(ts)} and last ts {min(ts)}: {sub_timestamps(max(ts), min(ts))}")

report(data)


