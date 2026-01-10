import re
from collections import OrderedDict

parts = []

with open("server.log", "r") as f:
    for line in f:
        match = re.search(r"FLAGPART:\s*(.*)", line)
        if match:
            parts.append(match.group(1))

unique_parts = list(OrderedDict.fromkeys(parts))
flag = "".join(unique_parts)

print(flag)
