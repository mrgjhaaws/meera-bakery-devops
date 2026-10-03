"""Lesson 1 - Why the cloud?  A tiny simulation (no AWS account needed).

A bakery website gets normal traffic most days and a big spike on Festival day.
Compare a FIXED on-premise server with an elastic cloud setup.
Run:  python scripts/lesson01_capacity_simulation.py
"""
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Festival!", "Mon"]
REQUESTS = [200, 220, 180, 210, 260, 400, 3000, 230]   # customers per hour
SERVER_CAPACITY = 500        # on-prem server handles 500 req/hour
CLOUD_UNIT = 500             # each cloud server also handles 500 req/hour
COST_PER_CLOUD_SERVER_DAY = 2.0   # illustrative numbers, NOT real AWS prices
COST_ONPREM_PER_DAY = 6.0         # hardware + power + admin, spread per day

print(f"{'Day':<10}{'Requests':>9}{'On-prem lost':>14}{'Cloud servers':>15}{'Cloud lost':>12}")
onprem_total = len(DAYS) * COST_ONPREM_PER_DAY
cloud_total = 0.0
lost_onprem = 0
for day, req in zip(DAYS, REQUESTS):
    lost = max(0, req - SERVER_CAPACITY)
    servers = -(-req // CLOUD_UNIT)          # ceiling division = auto scaling
    cloud_total += servers * COST_PER_CLOUD_SERVER_DAY
    lost_onprem += lost
    print(f"{day:<10}{req:>9}{lost:>14}{servers:>15}{0:>12}")

print()
print(f"Customers who could NOT order (on-prem): {lost_onprem}")
print(f"Illustrative cost  on-prem: {onprem_total:.1f}   cloud: {cloud_total:.1f}")
print("Takeaway: cloud scales up for the festival and back down afterwards.")
