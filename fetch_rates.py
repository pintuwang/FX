import os
import json
import urllib.request
from datetime import datetime, timezone, timedelta

SGT     = timezone(timedelta(hours=8))
API_KEY = os.environ.get("EXCHANGERATE_API_KEY", "").strip()

if not API_KEY:
    raise SystemExit("ERROR: EXCHANGERATE_API_KEY environment variable is not set.")

url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"

with urllib.request.urlopen(url, timeout=15) as r:
    data = json.loads(r.read().decode())

if data.get("result") != "success":
    raise SystemExit(f"API error: {data}")

rates = data["conversion_rates"]
payload = {
    "last_update": datetime.now(SGT).strftime("%Y-%m-%d %H:%M SGT"),
    "base": "USD",
    "rates": {k: rates[k] for k in ["EUR", "CNY", "INR", "SGD"] if k in rates}
}

os.makedirs("data", exist_ok=True)
with open("data/rates.json", "w") as f:
    json.dump(payload, f)

print(f"✓ Rates saved: {payload['rates']}")
