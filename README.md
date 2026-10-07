# Lot Due-Diligence Report — 12396 Edgewater Dr (Lot 23), Hampton GA 30228

Interactive, print-ready due-diligence report answering the 61-item checklist in
`Property LOT Due diligence.docx`, for parcel **05050A A003** in **Clayton County, Georgia**.

| Deliverable | File |
|---|---|
| **Interactive HTML artifact** (open in a browser) | [`index.html`](index.html) |
| **A4 portrait PDF, 21 pages, page-numbered** | [`12396-Edgewater-Lot23-Due-Diligence.pdf`](12396-Edgewater-Lot23-Due-Diligence.pdf) |
| Source template (edit this, not `index.html`) | `report.src.html` |
| Build script | `build.py` |

`index.html` is a single self-contained file — figures are inlined, so it works offline
and can be emailed as one attachment. Each of the 21 sections is a fixed A4 sheet, verified
to fit without overflow, so browser printing reproduces the PDF page-for-page.

## Headline findings

1. **The parcel is in Clayton County, not Henry County**, despite the Hampton address. This changes
   zoning, permitting, taxes and school assignment.
2. **The lot does not touch the water.** It is marketed as lakefront; the county parcel polygon stops
   59–80 ft short of the reservoir, with Clayton County Water Authority land in between. No apparent
   riparian rights.
3. **The lake is a public drinking-water reservoir** (J.W. Smith). Permit-only access, closed
   November–February, no swimming or wading — assume no private dock is achievable.
4. **The terrain is steeper than advertised.** A 2021 listing said "gentle rolling"; lidar measures
   80.2 ft of fall and an 18.3% average grade (23.5% over the steepest 50 ft). USDA's soil mapping
   independently corroborates this at 18%.
5. **Two Clayton County moratoriums are active** through 31 Dec 2026 — one on short-term rental
   applications (Res. 2026-153), one on new residential subdivision development (Res. 2026-120).
6. **Estimated build cost likely exceeds resale value** — roughly $798k–$1.39M all-in against a
   ~$120/sq ft local market.

Genuine strengths: FEMA Zone X (no mapped flood risk), a permanently undeveloped CCWA buffer
protecting the view, well-drained low-shrink–swell soil, a fire station 0.19 mi away, Hartsfield-Jackson
at ~16 mi, and a 265-day growing season.

## Evidence discipline

Every finding is tagged, because the brief specifically asked that estimates never be mistaken for
survey-grade fact:

- **OFFICIAL** — recorded or published source (county GIS, FEMA, USDA, county resolutions)
- **GIS-DERIVED** — computed here from public lidar/GIS; an estimate, not a survey
- **NEEDS PROFESSIONAL** — requires a surveyor, engineer, soil scientist or county sign-off
- **UNVERIFIED** — document not obtained or data unavailable; an open question, not a negative finding

Known gaps are listed explicitly rather than filled with plausible-sounding numbers. The recorded
plat, HOA covenants, RS180 setbacks, utility availability, lake bathymetry, Census demographics and
Clayton County's EPA radon zone were **not** obtained — see item 58 for the prioritised list.

## Data sources

Clayton County Tax Assessor GIS · FEMA National Flood Hazard Layer · USGS 3DEP lidar · USDA-NRCS Soil
Data Access · U.S. Census geocoder · Clayton County BOC resolutions · Clayton County Water Authority ·
Waterpointe Community Association · ERA5 reanalysis via Open-Meteo · OpenStreetMap (ODbL).

Listing photographs are deliberately omitted: they are copyrighted by the brokerages and not licensed
for redistribution. All imagery here is generated from public-domain federal data.

## Rebuilding

```bash
pip install matplotlib scipy shapely pyproj pypdf
python3 build.py        # report.src.html + figures/ -> index.html
```

`data/` holds the raw API responses (parcel records, elevation grid, soil, climate, amenities) so the
findings can be audited or recomputed. `figures/` holds the generated maps and the lot-aligned
elevation grid (`Zal.npy`, `xs.npy`, `ys.npy`).

## Scope

A desk study from public data. **No site visit.** Not a survey, geotechnical report, soil evaluation,
title opinion, appraisal, or legal/engineering/investment advice. Regulatory items were researched on
6 October 2026 and must be re-confirmed with the issuing authority before acting.
