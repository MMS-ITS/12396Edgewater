#!/usr/bin/env python3
"""Assemble the single-file due-diligence artifact from report.src.html + figures.

Handles:
  {{SVG:name}}   -> inline SVG (or embedded PNG for terrain3d)
  <!--SPLIT|id|nav|head|sub-->  -> breaks one sheet into two A4 sheets
  {{PAGENO}}     -> sequential "Page N of M" (computed after splits)
  {{CLIMATE_ROWS}}, {{DATE}}
"""
import re, json, base64, datetime, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def clean_svg(path):
    s = open(path, encoding="utf-8").read()
    s = s[s.find("<svg"):]
    s = re.sub(r'\s(width|height)="[\d.]+(pt|px)?"', "", s, count=2)
    if "preserveAspectRatio" not in s:
        s = s.replace("<svg", '<svg preserveAspectRatio="xMidYMid meet"', 1)
    return s


def embed_png(path, alt):
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    return ('<img alt="%s" style="max-width:100%%;height:auto" '
            'src="data:image/png;base64,%s">' % (alt, b64))


def apply_splits(s):
    """Turn <!--SPLIT|id|nav|head|sub--> markers into real sheet boundaries."""
    # NOTE: the character classes must exclude newlines and the final group must
    # be non-greedy. With [^|]* (which matches newlines) the last group runs to
    # the *final* "-->" in the file, eating an unrelated comment terminator and
    # leaving an unterminated comment that silently swallows the rest of the doc.
    pat = re.compile(r"<!--SPLIT\|([^|\n]*)\|([^|\n]*)\|([^|\n]*)\|([^|\n]*?)-->")

    def rep(m):
        sid, nav, head, sub = (x.strip() for x in m.groups())
        return (
            '<div class="pfoot"><span>%s</span><span>{{PAGENO}}</span></div>\n'
            "</section>\n\n"
            '<section class="sheet" id="%s" data-nav="%s">\n'
            '  <div class="phead"><span class="t">%s</span>'
            '<span class="s">%s</span></div>\n' % (nav, sid, nav, head, sub)
        )

    return pat.sub(rep, s)


SHEET_RE = re.compile(r'<section class="sheet[^"]*"')


def number_pages(s):
    """Replace each {{PAGENO}} with 'Page N of M' in document order.

    Uses a sequential re.sub so the document is never sliced or truncated.
    """
    total = len(SHEET_RE.findall(s))
    placeholders = s.count("{{PAGENO}}")
    if placeholders != total:
        print("ERROR: %d sheets but %d {{PAGENO}} placeholders — footers would "
              "be misnumbered." % (total, placeholders))
        sys.exit(1)

    counter = {"n": 0}

    def rep(_m):
        counter["n"] += 1
        return "Page %d of %d" % (counter["n"], total)

    s = re.sub(r"\{\{PAGENO\}\}", rep, s)
    return s, total


def main():
    src = open(os.path.join(ROOT, "report.src.html"), encoding="utf-8").read()

    src = apply_splits(src)

    for name in ("plan_topo", "sections"):
        p = os.path.join(ROOT, "figures", name + ".svg")
        src = src.replace("{{SVG:%s}}" % name, clean_svg(p))
    src = src.replace(
        "{{SVG:terrain3d}}",
        embed_png(os.path.join(ROOT, "figures", "terrain3d.png"),
                  "3D terrain model of the lot derived from USGS 3DEP lidar"))

    cl = json.load(open(os.path.join(ROOT, "data", "climate.json")))
    rows = ['<tr><td>{}</td><td class="n">{:.1f}</td><td class="n">{:.1f}</td>'
            '<td class="n">{:.1f}</td><td class="n">{:.0f}</td></tr>'.format(
                m["m"], m["tmax"], m["tmin"], m["tmean"], m["precip_mm"])
            for m in cl["months"]]
    rows.append('<tr class="hi"><td><b>ANNUAL</b></td><td class="n"><b>{:.1f}</b></td>'
                '<td class="n"><b>{:.1f}</b></td><td class="n"><b>{:.1f}</b></td>'
                '<td class="n"><b>{:.0f}</b></td></tr>'.format(
                    cl["annual_tmax"], cl["annual_tmin"],
                    cl["annual_tmean"], cl["annual_precip_mm"]))
    src = src.replace("{{CLIMATE_ROWS}}", "\n".join(rows))

    src = src.replace("{{DATE}}", datetime.date(2026, 10, 6).strftime("%d %B %Y"))
    src = src.replace("erosion-control permits bite. Verify before designing.</p>",
                      "erosion-control permits bite. Verify before designing.</small></p>")

    src, total = number_pages(src)

    left = re.findall(r"\{\{[^}]+\}\}", src)
    if left:
        print("ERROR unreplaced placeholders:", set(left)); sys.exit(1)

    out = os.path.join(ROOT, "index.html")
    open(out, "w", encoding="utf-8").write(src)
    print("sheets: %d   size: %.0f KB" % (total, len(src) / 1024))
    return total


if __name__ == "__main__":
    main()
