import os, re, json, urllib.request, datetime
KEYS = {"whole": "ICAL_WHOLE", "first": "ICAL_FIRST", "ground": "ICAL_GROUND"}
P = "data/availability.json"
d = lambda s: datetime.datetime.strptime(s[:8], "%Y%m%d").date().isoformat()
try: out = json.load(open(P))
except Exception: out = {"listings": {}}
for k, env in KEYS.items():
    url = os.environ.get(env, "").strip()
    if not url: continue
    try:
        txt = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read().decode()
        txt = re.sub(r"\r?\n[ \t]", "", txt)
        rng = []
        for ev in txt.split("BEGIN:VEVENT")[1:]:
            s = re.search(r"DTSTART[^:]*:(\d{8})", ev); e = re.search(r"DTEND[^:]*:(\d{8})", ev)
            if s and e: rng.append([d(s.group(1)), d(e.group(1))])
        out["listings"][k] = sorted(rng)
    except Exception as x:
        print("Failed", k, x)  # keep previous data
out["updated"] = datetime.datetime.utcnow().isoformat() + "Z"
json.dump(out, open(P, "w"), indent=1)
