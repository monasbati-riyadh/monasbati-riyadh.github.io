import json, os, re, sys, urllib.request, datetime as D

AR = {57:"أرسنال",58:"أستون فيلا",61:"تشيلسي",62:"إيفرتون",63:"فولهام",64:"ليفربول",
65:"مانشستر سيتي",66:"مانشستر يونايتد",67:"نيوكاسل يونايتد",71:"سندرلاند",73:"توتنهام هوتسبير",
322:"هال سيتي",341:"ليدز يونايتد",349:"إبسويتش تاون",351:"نوتنغهام فورست",354:"كريستال بالاس",
397:"برايتون",402:"برنتفورد",1044:"بورنموث",1076:"كوفنتري سيتي"}

req = urllib.request.Request(
    "https://api.football-data.org/v4/competitions/PL/matches?status=SCHEDULED",
    headers={"X-Auth-Token": os.environ["FD_KEY"]})
data = json.load(urllib.request.urlopen(req, timeout=30))
ms = data["matches"]
if len(ms) < 20:
    sys.exit("too few matches: %d" % len(ms))

out = []
for m in ms:
    t = D.datetime.fromisoformat(m["utcDate"].replace("Z", "+00:00")) + D.timedelta(hours=3)
    h, a = m["homeTeam"], m["awayTeam"]
    out.append({"d": t.strftime("%Y-%m-%d"), "t": t.strftime("%H:%M"),
                "h": AR.get(h["id"], h["shortName"]), "a": AR.get(a["id"], a["shortName"])})
out.sort(key=lambda x: (x["d"], x["t"]))
meta = {"upd": D.datetime.utcnow().strftime("%Y-%m-%d"), "first": out[0]["d"], "last": out[-1]["d"], "m": out}
line = "var PL=" + json.dumps(meta, ensure_ascii=False, separators=(",", ":")) + ";//PLDATA"
html = open("index.html", encoding="utf-8").read()
new, n = re.subn(r"var PL=.*?//PLDATA", lambda _: line, html, count=1, flags=re.S)
if n != 1:
    sys.exit("PL marker not found")
os.makedirs("_site", exist_ok=True)
open("_site/index.html", "w", encoding="utf-8").write(new)
print("matches=%d first=%s last=%s" % (len(out), out[0]["d"], out[-1]["d"]))
