import pandas as pd
import random

rows = 1000

data = []

protocols = ["tcp", "udp", "icmp"]
services = ["http", "ftp", "smtp", "dns"]
flags = ["SF", "REJ", "S0"]

for _ in range(rows):
    duration = random.randint(0, 1000)
    protocol = random.choice(protocols)
    service = random.choice(services)
    src_bytes = random.randint(0, 10000)
    dst_bytes = random.randint(0, 10000)
    flag = random.choice(flags)

    # 🔥 Logic to simulate attacks
    if src_bytes > 5000 or dst_bytes > 5000:
        label = 1   # attack
    else:
        label = 0   # normal

    data.append([
        duration, protocol, service,
        src_bytes, dst_bytes, flag, label
    ])

columns = [
    "duration", "protocol_type", "service",
    "src_bytes", "dst_bytes", "flag", "label"
]

df = pd.DataFrame(data, columns=columns)

df.to_csv("data/dataset.csv", index=False)

print("✅ Dataset created successfully with 1000 rows!")