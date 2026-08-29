# VIN Report Website — Full Build Roadmap
*(Reference spec — hand this to your developer)*

## 1. What This Website Does
User enters a 17-character VIN → website fetches vehicle data from government sources → generates a formatted report (web page + downloadable PDF) showing: vehicle identity, recalls, complaints, investigations, TSBs, safety ratings, crash photos, and fuel economy.

All underlying data is free/public. No data is created or owned by us — we aggregate, format, and present it.

---

## 2. Data Sources (all free, no license needed for this scope)

| # | Data | Source | Access Method |
|---|------|--------|----------------|
| 1 | Vehicle identity (make/model/year/engine/plant) | NHTSA vPIC | REST API — `vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/{VIN}?format=json` |
| 2 | Recalls | NHTSA Recalls API | REST API — `api.nhtsa.gov/recalls/recallsByVehicle?make=&model=&modelYear=` |
| 3 | Owner complaints | NHTSA Complaints API | REST API — `api.nhtsa.gov/complaints/complaintsByVehicle?make=&model=&modelYear=` |
| 4 | Investigations | NHTSA ODI Investigations dataset | Bulk file (download + store in own DB) |
| 5 | Technical Service Bulletins (TSBs) | NHTSA Manufacturer Communications / TSBS dataset | Bulk downloadable file (data.transportation.gov) — **no live API**, must import into own DB |
| 6 | Safety ratings (stars, rollover %) | NHTSA NCAP Ratings dataset | Bulk file or their ratings API |
| 7 | Crash test photos | NHTSA NCAP media | Bulk file/image archive — download & host yourself |
| 8 | MPG / fuel economy / MSRP | fueleconomy.gov | REST API |
| 9 | *(Optional, later)* Title/odometer/ownership history | NMVTIS | **Requires becoming an Approved NMVTIS Data Provider** — paid, regulated, separate application process. Skip this for v1. |

**Key point for your developer:** items 1, 2, 3, 8 are live-callable APIs. Items 4, 5, 6, 7 are **not live APIs** — they must be downloaded once as bulk files and loaded into your own database, then refreshed on a schedule (e.g. weekly/monthly job).

---

## 3. Recommended Tech Stack

- **Frontend:** React or plain HTML/JS — simple VIN input form + report display page
- **Backend:** Node.js (Express) or Python (FastAPI/Django) — orchestrates API calls, talks to database, generates PDFs
- **Database:** PostgreSQL or MySQL — stores the bulk-imported TSB/investigation/ratings/photo data, plus cached results per VIN pattern to avoid re-querying live APIs every time
- **PDF generation:** 
  - Node: Puppeteer (renders an HTML template to PDF) — easiest for matching a designed layout
  - Python: WeasyPrint or ReportLab
- **Hosting:** Any standard VPS/cloud (DigitalOcean, AWS, Hetzner) — nothing exotic needed
- **Background jobs:** A scheduled task (cron) to periodically re-download and refresh the bulk datasets (TSBs, investigations, ratings, photos)

---

## 4. System Architecture (flow)

```
User enters VIN on website
        │
        ▼
Backend receives VIN
        │
        ├─► Call NHTSA vPIC API (live)            → vehicle identity
        ├─► Call NHTSA Recalls API (live)          → recalls
        ├─► Call NHTSA Complaints API (live)       → complaints
        ├─► Query own DB (from bulk imports)       → TSBs, investigations, ratings, crash photos
        └─► Call fueleconomy.gov API (live)        → MPG/MSRP
        │
        ▼
Backend combines everything into one data object
        │
        ├─► Render as webpage (for instant viewing)
        └─► Render as PDF (HTML template → Puppeteer/WeasyPrint) for download
        │
        ▼
Report shown/delivered to user
```

---

## 5. Step-by-Step Build Plan

### Phase 1 — MVP (basic working version)
1. Build VIN input form (frontend)
2. Backend endpoint: call vPIC API → display decoded vehicle identity
3. Backend endpoint: call Recalls API → display recalls
4. Backend endpoint: call Complaints API → display complaints
5. Basic report page layout (no PDF yet)

*This alone is roughly what the demo I built you does — extended with complaints.*

### Phase 2 — Bulk Data Integration
1. Download NHTSA TSB bulk dataset → design a DB table → write an import script
2. Download NHTSA Investigations dataset → same process
3. Download NHTSA Safety Ratings dataset → same process
4. Download/link NHTSA crash-test photo archive → store image files or URLs, matched by make/model/year
5. Set up a scheduled job (weekly/monthly) to re-download and refresh these, since NHTSA updates them over time

### Phase 3 — Report Design & PDF
1. Design the actual report layout (branding, colors, logo, page structure) — this is a design task, similar to what you uploaded
2. Build an HTML template that matches this design, populated with the combined data
3. Use Puppeteer/WeasyPrint to convert that HTML into a downloadable PDF
4. Add report metadata: report number generation, "issued on" date, etc. (this is just your own logic, not from any API)

### Phase 4 — Polish & Business Logic
1. Add VIN validation (17 characters, no I/O/Q letters, checksum validation)
2. Add caching — if the same VIN (or same make/model/year combo) was queried recently, serve cached result instead of re-hitting APIs every time
3. Add rate-limiting protection on your own backend
4. Add payment gateway if you plan to charge for reports (Stripe, PayPal, or local options for Pakistan like JazzCash/EasyPaisa if targeting local market)
5. Add basic legal pages: Terms of Service, Privacy Policy, and a disclaimer matching what NHTSA-based sites typically state (data accuracy disclaimer, "not a substitute for professional inspection," etc.)

### Phase 5 — Optional Future Expansion
- Apply to become an NMVTIS Approved Data Provider if you want to add title/odometer/theft history (separate paid/regulated process — not needed for the recall/safety-style report you showed me)
- Add license plate → VIN lookup
- Add user accounts / saved reports / subscription model

---

## 6. What Your Developer Actually Needs to Know Going In

- No API keys are required for any of the core NHTSA/EPA data (all free, no signup)
- The hardest technical parts are **not** the live APIs — they're the **TSB and crash-photo bulk data import + database design**
- PDF generation from an HTML template is the standard approach — no need to build PDFs from scratch
- Budget more time for **design and data-import/database work** than for the "API calling" part, which is comparatively simple

---

## 7. Realistic Scope Estimate (for planning with developer)

| Phase | Relative Effort |
|-------|-----------------|
| Phase 1 (MVP) | Low |
| Phase 2 (bulk data + DB) | Medium-High |
| Phase 3 (design + PDF) | Medium-High |
| Phase 4 (polish/business) | Medium |
| Phase 5 (NMVTIS/expansion) | High (separate track, optional) |

---

## 8. Legal Note
Everything in phases 1–4 uses public government data, which is legal to use and republish in formatted reports (this is exactly what EpicVIN, VinAudit, VINinspect, and similar sites do). If you want to sell reports commercially, there's no licensing blocker for this scope — competition is the main challenge, not legality. Only the NMVTIS title-history piece (Phase 5) requires formal government approval.
