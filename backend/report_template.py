import html
from datetime import datetime
from typing import Any

CSS = """
@font-face { font-family: 'Roboto'; src: url('assets/fonts/Roboto-Regular.ttf'); font-weight: 400; font-style: normal; }
@font-face { font-family: 'Roboto'; src: url('assets/fonts/Roboto-Light.ttf'); font-weight: 300; font-style: normal; }
@font-face { font-family: 'Roboto'; src: url('assets/fonts/Roboto-Medium.ttf'); font-weight: 500; font-style: normal; }
@font-face { font-family: 'Roboto'; src: url('assets/fonts/Roboto-Bold.ttf'); font-weight: 700; font-style: normal; }

@page {
  size: Letter;
  margin: 10mm 12mm 14mm 12mm;
  @bottom-center {
    content: "Car Inspection Pro · Vehicle History Report · Page " counter(page) " of " counter(pages);
    font-family: 'Roboto', sans-serif;
    font-size: 8pt;
    color: #8A8A8A;
  }
}
* { box-sizing: border-box; }
body { font-family: 'Roboto', sans-serif; color: #212121; font-size: 10.5pt; margin: 0; }

/* ---- header bar ---- */
.header-bar {
  border: none;
  padding: 0;
  margin: 0;
  background: #FFFFFF;
}
.header-accent {
  height: 5px;
  background: linear-gradient(90deg, #1a56db 0%, #2563eb 40%, #3b82f6 100%);
}
.header-inner {
  display: flex;
  align-items: center;
  padding: 14px 20px 12px 20px;
  border-bottom: 2px solid #1a56db;
}
.header-left {
  width: 30%;
  flex: 0 0 30%;
  display: flex;
  align-items: center;
}
.logo {
  width: 160px;
  height: auto;
}
.header-center {
  width: 44%;
  flex: 0 0 44%;
  display: flex;
  flex-direction: column;
  padding-left: 20px;
}
.header-title {
  font-size: 18pt;
  font-weight: 800;
  color: #1a56db;
  line-height: 1.1;
  letter-spacing: -0.3px;
}
.header-subtitle {
  font-size: 8.5pt;
  font-weight: 400;
  color: #64748b;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  margin-top: 2px;
}
.header-right {
  width: 26%;
  flex: 0 0 26%;
  text-align: right;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}
.header-price {
  font-size: 13pt;
  font-weight: 700;
  color: #1a56db;
  line-height: 1;
}
.header-price-label {
  font-size: 7pt;
  font-weight: 400;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-top: 1px;
}

/* ---- online listings banner ---- */
.listing-banner {
  border: none;
  border-radius: 0;
  padding: 8px 0 10px 0;
  margin-bottom: 0;
  background: transparent;
}

.listing-banner .lb-title {
  font-weight: 500;
  color: #212121;
  font-size: 9pt;
  margin-bottom: 0;
}
.listing-banner .lb-row { display: flex; align-items: center; gap: 10px; }
.lb-row-icon { width: 26px; height: 26px; flex-shrink: 0; }
.lb-row-icon img { width: 26px; height: 26px; object-fit: contain; }
.lb-row-text { font-size: 9pt; font-weight: 600; color: #1F2937; }

/* ---- summary (vehicle identity + highlights) ---- */
.summary {
    display: flex;
    min-height: 295px;
    border: 1px solid #BDBDBD;
    overflow: hidden;
}
.summary-left {
    flex: 0 0 30%;
    padding: 12px 16px;
    border-right: 1px solid #BDBDBD;
}

.summary-right {
    width: 69%;
    flex: 0 0 69%;
    position: relative;
    padding: 0;

    display: block;
}
.hl-col { flex: 1; display: flex; flex-direction: column; }
.vehicle-title { font-size: 16pt; font-weight: 700; color: #212121; line-height: 1.15; margin-bottom: 3px; }
.vin-line { font-size: 9pt; color: #616161; margin-bottom: 6px; }
.vin-line b { letter-spacing: 0.5px; color: #212121; font-weight: 600; }
.summary-specs .spec { padding: 3px 0; font-size: 9pt; color: #212121; text-transform: uppercase; }

.highlights {
    width: 100%;
    height: 100%;
    display: grid;
    grid-template-rows: repeat(5, 1fr);
}

.hl-tile {
    width: 100%;
    min-height: 0;
    display: grid;
    grid-template-columns: 52px 1fr;
    border-bottom: 1px solid #BDBDBD;
    box-sizing: border-box;
}

.hl-tile:last-child {
    border-bottom: none;
}

/* Left icon column */
.hl-icon {
    width: 100%;
    height: 100%;
    min-height: 49px;

    display: flex;
    align-items: center;
    justify-content: center;

    /* No vertical line beside icons */
    border-right: none;

    box-sizing: border-box;
}

.hl-icon img {
    width: 30px;
    height: 30px;
    object-fit: contain;
}

/* Right text column */
.hl-content {
    min-width: 0;

    display: flex;
    flex-direction: column;
    justify-content: center;

    padding: 6px 12px;
    box-sizing: border-box;
}

.hl-label {
    font-size: 8pt;
    color: #777;
    margin-bottom: 2px;
}

.hl-value {
    font-size: 10.5pt;
    font-weight: 700;
    color: #3A3A3A;
    line-height: 1.2;
}
.severity-mini { display: flex; gap: 3px; margin-top: 4px; }
.severity-mini .seg { flex: 1; text-align: center; padding: 2px 0; font-size: 6.5pt; font-weight: 700; text-transform: uppercase; }
.seg-mini-minor { background: #D1FAE5; color: #047857; }
.seg-mini-moderate { background: #FEF3C7; color: #B45309; }
.seg-mini-severe { background: #FEE2E2; color: #B91C1C; }
.seg-active { outline: 2px solid #1F2937; }

.vehicle-mascot {
    position: absolute;
    right: 8px;
    bottom: 0;
    width: 135px;
    z-index: 2;
}

.vehicle-mascot img {
    width: 100%;
    height: auto;
    display: block;
}

/* vehicle photo */
.photo-col { width: 42%; display: flex; align-items: flex-end; }
.photo-box {
  border: 1px solid #BDBDBD;
  background: #F9FAFB;
  min-height: 90px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #C0C4CC;
  font-size: 8.5pt;
  overflow: hidden;
}
.photo-box img { width: 100%; height: auto; }

/* ---- top disclaimer ---- */
.top-note { font-size: 8pt; color: #616161; line-height: 1.4; margin-bottom: 4px; }

/* ---- NMVTIS unavailable banner ---- */
.nmvtis-banner { display: flex; align-items: flex-start; gap: 10px; background: #FFF3E0; border: 1px solid #E65100; padding: 10px 14px; margin: 6px 0 10px 0; border-radius: 0; }
.nmvtis-banner-icon { font-size: 18pt; color: #E65100; flex-shrink: 0; line-height: 1; }
.nmvtis-banner-text { font-size: 8pt; color: #BF360C; line-height: 1.5; }
.nmvtis-banner-text b { color: #BF360C; }

/* ---- section headers (plain, no icon) ---- */
.section { margin-bottom: 8px; }
.section-box { border: 1px solid #BDBDBD; overflow: hidden; margin-bottom: 10px; background: #FFFFFF; }
.section-box .section-header { border-bottom: 2px solid #1A73E8; padding: 6px 12px 4px 12px; margin-bottom: 0; background: #FFFFFF; }
.section-header { border-bottom: 2px solid #1A73E8; padding-bottom: 4px; margin-bottom: 6px; }
.section-title { font-size: 12pt; font-weight: 700; color: #1A73E8; padding-left: 8px; border-left: 3px solid #1A73E8; }
.section-subtitle { font-size: 7.5pt; color: #8A8A8A; margin-top: 1px; }

/* ---- accident / damage ---- */
.info-banner { background: #EFF6FF; border: 1px solid #BDBDBD; padding: 8px 12px; margin-top: 8px; font-size: 9pt; font-weight: 700; color: #1E40AF; text-align: center; text-transform: uppercase; letter-spacing: 0.3px; }
.accident-card { border: 1px solid #BDBDBD; padding: 8px 10px; margin-bottom: 8px; break-inside: avoid; }
.accident-card .event-top { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 4px; }
.accident-card .event-top .ev-icon { width: 40px; height: 40px; flex-shrink: 0; background: #FEE4E4; display: flex; align-items: center; justify-content: center; }
.accident-card .event-top .ev-icon img { width: 26px; height: 26px; object-fit: contain; }
.accident-card .event-top .ev-body { flex: 1; }
.event-badge {
  display: inline-block;
  background: #FEE4E4;
  color: #B91C1C;
  font-size: 7.5pt;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  padding: 2px 8px;
  margin-bottom: 5px;
}
.ev-date { font-size: 8.5pt; color: #8A8A8A; margin-bottom: 2px; }
.ev-title { font-size: 11pt; font-weight: bold; color: #212121; margin-bottom: 2px; }
.ev-desc { font-size: 9pt; color: #616161; line-height: 1.4; }
.accident-card .severity-side { display: flex; justify-content: flex-end; border-top: 1px dashed #BDBDBD; padding-top: 4px; }
.accident-card .severity-side .severity-scale { width: 55%; }

/* severity scale */
.severity-scale { border: 1px solid #BDBDBD; }
.severity-scale .sc-label { font-size: 7.5pt; font-weight: 700; text-transform: uppercase; color: #8A8A8A; letter-spacing: 0.3px; padding: 4px 10px 2px 10px; }
.severity-segs { display: flex; }
.severity-seg { flex: 1; text-align: center; padding: 5px 0; font-size: 8.5pt; font-weight: 700; text-transform: uppercase; }
.seg-minor { background: #D1FAE5; color: #047857; }
.seg-moderate { background: #FEF3C7; color: #B45309; }
.seg-severe { background: #FEE2E2; color: #B91C1C; }

/* damage location diagram */
.damage-loc .dl-title { font-size: 7.5pt; font-weight: 700; text-transform: uppercase; color: #8A8A8A; letter-spacing: 0.3px; margin-bottom: 5px; }
.car-diagram { border: 1px solid #BDBDBD; padding: 6px; }
.dl-front, .dl-rear { text-align: center; font-size: 8pt; font-weight: 700; color: #8A8A8A; padding: 4px; border: 1px solid #BDBDBD; background: #F9FAFB; }
.dl-mid { display: flex; align-items: stretch; }
.dl-side { width: 16%; font-size: 8pt; font-weight: 700; color: #8A8A8A; display: flex; align-items: center; justify-content: center; border: 1px solid #BDBDBD; background: #F9FAFB; margin: 5px 0; }
.dl-body { flex: 1; height: 52px; border: 1px dashed #BDBDBD; margin: 5px; position: relative; }
.dl-body .hit { position: absolute; width: 16px; height: 16px; background: #DC2626; border-radius: 50%; top: 50%; left: 50%; transform: translate(-50%, -50%); }
.dl-body .hit-lbl { position: absolute; top: calc(50% + 12px); left: 50%; transform: translateX(-50%); font-size: 6pt; font-weight: 700; color: #DC2626; white-space: nowrap; }

/* ---- recent service ---- */
.service-table { width: 100%; border-collapse: collapse; border: 1px solid #BDBDBD; }
.service-table th { text-align: left; padding: 4px 10px; font-size: 8pt; color: #8A8A8A; border-bottom: 1px solid #BDBDBD; border-right: 1px solid #BDBDBD; background: #F9FAFB; font-weight: 600; }
.service-table th:last-child { border-right: none; }
.service-table td { padding: 4px 10px; border-bottom: 1px solid #F3F4F6; border-right: 1px solid #BDBDBD; font-size: 9pt; vertical-align: middle; }
.service-table td:last-child { border-right: none; }
.service-table tr:last-child td { border-bottom: none; }
.service-cell { display: flex; align-items: center; gap: 7px; }
.service-cell img { width: 14px; height: 14px; vertical-align: middle; }
.good-note { display: flex; align-items: center; gap: 8px; background: #F2F8F3; border: 1px solid #BDBDBD; padding: 5px 10px; margin-top: 4px; font-size: 9pt; font-weight: 600; color: #2E7D32; break-inside: avoid; }
.good-note img { width: 16px; height: 16px; }

/* ---- additional / title history tables ---- */
.history-table { width: 100%; border-collapse: collapse; border: 1px solid #BDBDBD; }
.history-table th { text-align: left; padding: 4px 10px; font-size: 8pt; color: #8A8A8A; border-bottom: 1px solid #BDBDBD; border-right: 1px solid #BDBDBD; background: #F9FAFB; font-weight: 600; }
.history-table th:last-child { border-right: none; }
.history-table td { padding: 4px 10px; border-bottom: 1px solid #F3F4F6; border-right: 1px solid #BDBDBD; font-size: 9pt; vertical-align: middle; }
.history-table td:last-child { border-right: none; }
.history-table tr:last-child td { border-bottom: none; }
.check-title { font-weight: 700; color: #212121; font-size: 9pt; }
.check-desc { font-size: 8pt; color: #8A8A8A; margin-top: 2px; line-height: 1.4; }
.tick { width: 10px; height: 10px; vertical-align: middle; margin-right: 4px; }
.status-label { color: #8A8A8A; font-weight: 600; font-size: 9pt; }
.status-label.ok { color: #2E7D32; }
.status-label.warn { color: #B26A00; }

/* guarantee box */
.guarantee-box { background: #F9FAFB; border: 1px solid #BDBDBD; padding: 10px 12px; margin: 12px 0; font-size: 8.5pt; line-height: 1.5; color: #8A8A8A; }
.guarantee-box .guarantee-label { font-weight: 700; color: #2E7D32; font-size: 9pt; margin-bottom: 4px; }
.guarantee-box .guarantee-label img { width: 14px; height: 14px; vertical-align: middle; margin-right: 4px; }
.guarantee-box p { margin: 0; }
.terms-links { font-size: 8.5pt; font-weight: 600; color: #2E7D32; margin-top: 6px; }

/* ---- ownership table ---- */
.ownership-table { width: 100%; border-collapse: collapse; border: 1px solid #BDBDBD; }
.ownership-table th { text-align: left; padding: 4px 10px; font-size: 8pt; color: #8A8A8A; border-bottom: 1px solid #BDBDBD; border-right: 1px solid #BDBDBD; background: #F9FAFB; font-weight: 600; }
.ownership-table th:last-child { border-right: none; }
.ownership-table td { padding: 4px 10px; border-bottom: 1px solid #F3F4F6; border-right: 1px solid #BDBDBD; font-size: 9pt; vertical-align: middle; }
.ownership-table td:last-child { border-right: none; }
.ownership-table tr:last-child td { border-bottom: none; }

/* ---- detailed history ---- */
.detail-owner { margin-bottom: 18px; }
.detail-owner-card { border: 1px solid #BDBDBD; padding: 10px 12px; margin-bottom: 8px; display: flex; align-items: center; gap: 14px; }
.detail-owner-card .own-id { font-size: 13pt; font-weight: 700; color: #212121; }
.detail-owner-card .own-purchased { font-size: 8.5pt; color: #8A8A8A; }
.detail-owner-card .own-note { flex: 1; font-size: 8.5pt; color: #616161; font-style: italic; line-height: 1.4; }
.detail-owner-card .own-right { text-align: right; }
.detail-owner-card .own-type { font-size: 9pt; font-weight: 700; color: #212121; }
.detail-owner-card .own-mpy { font-size: 8.5pt; color: #8A8A8A; }
.detail-table { width: 100%; border-collapse: collapse; border: 1px solid #BDBDBD; }
.detail-table th { text-align: left; padding: 4px 10px; font-size: 8pt; color: #8A8A8A; border-bottom: 1px solid #BDBDBD; border-right: 1px solid #BDBDBD; background: #F9FAFB; font-weight: 600; }
.detail-table th:last-child { border-right: none; }
.detail-table td { padding: 4px 10px; border-bottom: 1px solid #F3F4F6; border-right: 1px solid #BDBDBD; font-size: 9pt; vertical-align: middle; }
.detail-table td:last-child { border-right: none; }
.detail-table tr:last-child td { border-bottom: none; }
.detail-table .td-date { white-space: nowrap; width: 13%; }
.detail-table .td-miles { width: 9%; color: #212121; font-weight: 600; }
.detail-table .td-source { width: 30%; color: #616161; }
.detail-table .td-source .src-name { font-weight: 700; color: #212121; font-size: 9pt; }
.detail-table .td-source .src-sub { font-size: 8pt; }
.detail-table .td-comments { width: 48%; }
.detail-table .td-comments .evt-line img { width: 13px; height: 13px; vertical-align: middle; margin-right: 5px; }
.detail-table .td-comments .evt-line { display: block; font-size: 9pt; }
.detail-table .td-comments .evt-line.main { font-weight: 700; color: #212121; }
.detail-table .td-comments .evt-note { font-size: 8.5pt; color: #2E7D32; font-weight: 600; display: block; margin-top: 3px; }
.detail-table .td-comments .good-flag { font-size: 8.5pt; color: #2E7D32; font-weight: 600; }
.detail-damage { border: 1px solid #BDBDBD; background: #FFF7F7; padding: 8px 10px; margin-top: 4px; }
.detail-damage .severity-side { display: flex; gap: 14px; margin-top: 8px; }
.detail-damage .severity-side > div { flex: 1; }
.rating-line { font-size: 8.5pt; color: #B26A00; font-weight: 700; }
.reviews-line { font-size: 8pt; color: #8A8A8A; }

/* ---- glossary & footer ---- */
.glossary dt { font-weight: bold; font-size: 9pt; margin-top: 6px; }
.glossary dd { font-size: 8.5pt; color: #424242; margin: 2px 0 0 0; line-height: 1.4; }
.have-questions { font-size: 9pt; color: #424242; line-height: 1.5; margin: 14px 0; padding: 8px 10px; background: #F9FAFB; border: 1px solid #BDBDBD; }
.have-questions b { color: #212121; }
.footer { margin-top: 14px; border-top: 1px solid #BDBDBD; padding-top: 8px; font-size: 8pt; color: #8A8A8A; line-height: 1.5; }
.footer b { color: #1F2937; }
.review-stmt { font-size: 8pt; color: #424242; line-height: 1.5; margin-top: 12px; }
.copyright { text-align: center; font-size: 7.5pt; color: #8A8A8A; margin-top: 10px; }
.signatures { display: flex; gap: 24px; margin-top: 14px; }
.sig { flex: 1 1 50%; }
.sig .line { border-bottom: 1px solid #B0B0B0; height: 30px; }
.sig .cap { font-size: 8pt; color: #616161; margin-top: 4px; }
.page-break { page-break-after: always; }
"""

LOGO = '<img class="logo" src="assets/carinspectionlogo.JPG" alt="Car Inspection Pro"/>'
FOX_MASCOT = '<img class="mascot-img" src="assets/icons/fox.png" alt=""/>'
ICON_ACCIDENT = '<img src="assets/icons/carsearch.png" alt=""/>'
ICON_SERVICE = '<img src="assets/icons/tools.png" alt=""/>'
ICON_WELL_MAINTAINED = '<img src="assets/icons/protected.png" alt=""/>'
ICON_OWNERS = '<img src="assets/icons/threepeople.png" alt=""/>'
ICON_OWNER_TYPE = '<img src="assets/icons/house.png" alt=""/>'
ICON_ODOMETER = '<img src="assets/icons/fox.png" alt=""/>'
ICON_GOOD = '<img src="assets/icons/reading.png" alt=""/>'
ICON_GUARANTEED = '<img src="assets/icons/protected.png" alt=""/>'
TICK = '<img class="tick" src="assets/icons/tickicon.png" alt=""/>'

PRICE_USD = "45.00"

SAMPLE_HIGHLIGHTS = {
    "accident": True,
    "accident_severity": "minor damage",
    "oil_changes": True,
    "owners": 3,
    "owner_type": "Personal lease, Personal",
    "odometer": 128595,
}

SAMPLE_ACCIDENTS = [
    {
        "type": "minor damage",
        "description": "Involving front or side impact with another motor vehicle",
        "severity": "minor",
        "date": "2023-08-06",
        "airbags": "Airbags did not deploy",
        "location": "front",
    }
]

SAMPLE_SERVICES = [
    {"type": "oil", "service": "Oil", "notes": "Oil and filter changed", "date": "2025-05-21"},
    {"type": "tires", "service": "Tires", "notes": "Four tires replaced", "date": "2025-05-21"},
]

SAMPLE_OWNERS_CHECKS = {
    "owner_1": {"total_loss": "No Issues Reported", "structural_damage": "No Issues Reported", "airbag_deployment": "No Issues Reported", "odometer_check": "No Issues Indicated", "accident_damage": "No Issues Reported", "manufacturer_recall": "No Recalls Reported", "basic_warranty": "Warranty Expired"},
    "owner_2": {"total_loss": "No Issues Reported", "structural_damage": "No Issues Reported", "airbag_deployment": "No Issues Reported", "odometer_check": "No Issues Indicated", "accident_damage": "No Issues Reported", "manufacturer_recall": "No Recalls Reported", "basic_warranty": "Warranty Expired"},
    "owner_3": {"total_loss": "No Issues Reported", "structural_damage": "No Issues Reported", "airbag_deployment": "No Issues Reported", "odometer_check": "No Issues Indicated", "accident_damage": "Minor Damage", "manufacturer_recall": "No Recalls Reported", "basic_warranty": "Warranty Expired"},
}

SAMPLE_OWNERS_OWNERSHIP = [
    {"number": "1", "year_purchased": "2015", "type": "Personal lease", "length_of_ownership": "3 yrs. 3 mo.", "state": "Ohio", "miles_per_year": "7,514/yr", "odometer": "25,707"},
    {"number": "2", "year_purchased": "2018", "type": "Personal", "length_of_ownership": "2 yrs. 10 mo.", "state": "Ohio", "miles_per_year": "---", "odometer": "64,602"},
    {"number": "3", "year_purchased": "2021", "type": "Personal", "length_of_ownership": "3 yrs. 10 mo.", "state": "Ohio", "miles_per_year": "19,591/yr", "odometer": "128,595"},
]

SAMPLE_DETAILED_HISTORY = [
    {
        "owner": 1,
        "purchased": "2015",
        "note": "Low mileage! This owner drove less than the industry average of 15,000 miles per year.",
        "type": "Personal Lease Vehicle",
        "miles_per_year": "7,514 mi/yr",
        "events": [
            {"date": "10/14/2014", "mileage": "1", "kind": "service", "source_name": "Valley Chevrolet Inc", "source_loc": "Wellington, OH", "source_phone": "440-647-5381", "source_url": "valleychevy1.com", "source_rating": "4.3 / 5.0", "source_reviews": "60 Verified Reviews", "source_favorites": "940 Customer Favorites", "comments": ["Vehicle serviced", "Pre-delivery inspection completed"]},
            {"date": "10/18/2014", "mileage": "", "kind": "inventory", "source_name": "Dealer Inventory", "comments": ["Vehicle offered for sale"]},
            {"date": "04/17/2015", "mileage": "19", "kind": "purchase", "source_name": "Ohio Motor Vehicle Dept.", "comments": ["Vehicle purchase reported"]},
            {"date": "04/28/2015", "mileage": "", "kind": "title", "source_name": "Ohio Motor Vehicle Dept.", "source_loc": "Arlington, TX", "title_no": "4702999261", "comments": ["Title issued or updated", "First owner reported", "Titled or registered as personal lease vehicle", "Loan or lien reported"]},
            {"date": "04/30/2015", "mileage": "", "kind": "registration", "source_name": "Ohio Motor Vehicle Dept.", "source_loc": "Wellington, OH", "title_no": "4702999261", "comments": ["Registration issued or renewed", "Titled or registered as personal lease vehicle"]},
            {"date": "08/14/2015", "mileage": "3,611", "kind": "service", "source_name": "Valley Chevrolet Inc", "source_loc": "Wellington, OH", "source_phone": "440-647-5381", "source_url": "valleychevy1.com", "source_rating": "4.3 / 5.0", "source_reviews": "60 Verified Reviews", "source_favorites": "940 Customer Favorites", "comments": ["Vehicle serviced", "Maintenance inspection completed", "Oil and filter changed"]},
            {"date": "01/15/2016", "mileage": "", "kind": "registration", "source_name": "Ohio Motor Vehicle Dept.", "source_loc": "Wellington, OH", "title_no": "4702999261", "comments": ["Registration issued or renewed", "Titled or registered as personal lease vehicle"]},
            {"date": "04/28/2016", "mileage": "9,012", "kind": "service", "source_name": "Valley Chevrolet Inc", "source_loc": "Wellington, OH", "source_phone": "440-647-5381", "source_url": "valleychevy1.com", "source_rating": "4.3 / 5.0", "source_reviews": "60 Verified Reviews", "source_favorites": "940 Customer Favorites", "comments": ["Vehicle serviced", "Maintenance inspection completed", "Oil and filter changed"]},
            {"date": "12/01/2016", "mileage": "13,525", "kind": "service", "source_name": "Valley Chevrolet Inc", "source_loc": "Wellington, OH", "source_phone": "440-647-5381", "source_url": "valleychevy1.com", "source_rating": "4.3 / 5.0", "source_reviews": "60 Verified Reviews", "source_favorites": "940 Customer Favorites", "comments": ["Vehicle serviced", "Maintenance inspection completed", "Fluids checked", "Light bulb(s) replaced", "Oil and filter changed", "Tire condition and pressure checked"]},
            {"date": "01/17/2017", "mileage": "", "kind": "registration", "source_name": "Ohio Motor Vehicle Dept.", "source_loc": "Wellington, OH", "title_no": "4702999261", "comments": ["Registration issued or renewed", "Titled or registered as personal lease vehicle"]},
            {"date": "06/01/2017", "mileage": "17,043", "kind": "service", "source_name": "Valley Chevrolet Inc", "source_loc": "Wellington, OH", "source_phone": "440-647-5381", "source_url": "valleychevy1.com", "source_rating": "4.3 / 5.0", "source_reviews": "60 Verified Reviews", "source_favorites": "940 Customer Favorites", "comments": ["Vehicle serviced", "Maintenance inspection completed", "Fluids checked", "Oil and filter changed", "Tire condition and pressure checked", "Tires rotated"]},
            {"date": "01/19/2018", "mileage": "", "kind": "registration", "source_name": "Ohio Motor Vehicle Dept.", "source_loc": "Wellington, OH", "title_no": "4702999261", "comments": ["Registration issued or renewed", "Titled or registered as personal lease vehicle"]},
            {"date": "05/02/2018", "mileage": "23,292", "kind": "service", "source_name": "Valley Chevrolet Inc", "source_loc": "Wellington, OH", "source_phone": "440-647-5381", "source_url": "valleychevy1.com", "source_rating": "4.3 / 5.0", "source_reviews": "60 Verified Reviews", "source_favorites": "940 Customer Favorites", "comments": ["Vehicle serviced", "Maintenance inspection completed", "Oil and filter changed", "Tires rotated"]},
            {"date": "07/19/2018", "mileage": "24,498", "kind": "purchase", "source_name": "Ohio Motor Vehicle Dept.", "comments": ["Vehicle purchase reported"]},
            {"date": "07/20/2018", "mileage": "", "kind": "inventory", "source_name": "Sarchione Chevrolet Garrettsville", "source_loc": "Garrettsville, OH", "source_phone": "330-527-2101", "source_url": "sarchionechevrolet2.com", "source_rating": "4.9 / 5.0", "source_reviews": "14 Verified Reviews", "source_favorites": "87 Customer Favorites", "comments": ["Vehicle offered for sale"]},
            {"date": "07/24/2018", "mileage": "", "kind": "service", "source_name": "Sarchione Chevrolet Garrettsville", "source_loc": "Garrettsville, OH", "source_phone": "330-527-2101", "source_url": "sarchionechevrolet2.com", "source_rating": "4.9 / 5.0", "source_reviews": "14 Verified Reviews", "source_favorites": "87 Customer Favorites", "comments": ["Vehicle serviced", "Pre-delivery inspection completed", "Maintenance inspection completed", "Vehicle washed/detailed"], "good": True},
            {"date": "07/25/2018", "mileage": "", "kind": "title", "source_name": "Ohio Motor Vehicle Dept.", "source_loc": "Garrettsville, OH", "title_no": "6702129511", "comments": ["Title issued or updated", "Dealer took title of this vehicle while it was in inventory"]},
            {"date": "08/09/2018", "mileage": "", "kind": "cpo", "source_name": "Certified Pre-Owned Dealer", "source_loc": "Garrettsville, OH", "comments": ["Offered for sale as a Chevrolet Certified Pre-Owned Vehicle"], "vehicle_color": "Red exterior", "vehicle_interior": "Black interior"},
            {"date": "08/13/2018", "mileage": "", "kind": "service", "source_name": "Sarchione Chevrolet Garrettsville", "source_loc": "Garrettsville, OH", "source_phone": "330-527-2101", "source_url": "sarchionechevrolet2.com", "source_rating": "4.9 / 5.0", "source_reviews": "14 Verified Reviews", "source_favorites": "87 Customer Favorites", "comments": ["Vehicle serviced", "Maintenance inspection completed", "Body lubricated", "Oil and filter changed"]},
            {"date": "11/24/2018", "mileage": "25,707", "kind": "cpo", "source_name": "Certified Pre-Owned Dealer", "source_loc": "Garrettsville, OH", "comments": ["Sold as a Chevrolet Certified Pre-Owned Vehicle"]},
        ],
    },
    {
        "owner": 2,
        "purchased": "2018",
        "note": "Personal Vehicle",
        "type": "Personal Vehicle",
        "miles_per_year": "---",
        "events": [
            {"date": "11/24/2018", "mileage": "", "kind": "purchase", "source_name": "Ohio Motor Vehicle Dept.", "comments": ["Vehicle purchase reported"]},
            {"date": "11/27/2018", "mileage": "", "kind": "title", "source_name": "Ohio Motor Vehicle Dept.", "source_loc": "Hartville, OH", "title_no": "6702176009", "comments": ["Title issued or updated", "New owner reported", "Loan or lien reported"]},
            {"date": "12/29/2018", "mileage": "", "kind": "registration", "source_name": "Ohio Motor Vehicle Dept.", "source_loc": "Hartville, OH", "title_no": "6702176009", "comments": ["Registration issued or renewed"]},
            {"date": "04/24/2019", "mileage": "", "kind": "service", "source_name": "Stratton Chevrolet Co", "source_loc": "Beloit, OH", "source_phone": "330-537-3151", "source_url": "strattonchevrolet.com", "source_rating": "5.0 / 5.0", "source_reviews": "134 Verified Reviews", "source_favorites": "200 Customer Favorites", "comments": ["Vehicle serviced", "Oil and filter changed"]},
            {"date": "04/30/2019", "mileage": "", "kind": "title", "source_name": "Ohio Motor Vehicle Dept.", "source_loc": "Hartville, OH", "title_no": "7605003346", "comments": ["Title issued or updated", "Loan or lien reported"]},
            {"date": "05/18/2019", "mileage": "", "kind": "registration", "source_name": "Ohio Motor Vehicle Dept.", "source_loc": "Hartville, OH", "title_no": "6702176009", "comments": ["Registration issued or renewed"]},
            {"date": "08/13/2019", "mileage": "", "kind": "title", "source_name": "Ohio Motor Vehicle Dept.", "source_loc": "Hartville, OH", "title_no": "7605058369", "comments": ["Title issued or updated", "Loan or lien reported"]},
            {"date": "09/23/2019", "mileage": "", "kind": "service", "source_name": "Stratton Chevrolet Co", "source_loc": "Beloit, OH", "source_phone": "330-537-3151", "source_url": "strattonchevrolet.com", "source_rating": "5.0 / 5.0", "source_reviews": "134 Verified Reviews", "source_favorites": "200 Customer Favorites", "comments": ["Vehicle serviced", "Engine/powertrain computer/module checked", "Oil and filter changed"]},
            {"date": "11/06/2019", "mileage": "", "kind": "service", "source_name": "Stratton Chevrolet Co", "source_loc": "Beloit, OH", "source_phone": "330-537-3151", "source_url": "strattonchevrolet.com", "source_rating": "5.0 / 5.0", "source_reviews": "134 Verified Reviews", "source_favorites": "200 Customer Favorites", "comments": ["Vehicle serviced", "Oil and filter changed", "Tires rotated"]},
            {"date": "05/04/2020", "mileage": "", "kind": "service", "source_name": "Stratton Chevrolet Co", "source_loc": "Beloit, OH", "source_phone": "330-537-3151", "source_url": "strattonchevrolet.com", "source_rating": "5.0 / 5.0", "source_reviews": "134 Verified Reviews", "source_favorites": "200 Customer Favorites", "comments": ["Vehicle serviced", "Oil and filter changed"]},
            {"date": "08/07/2020", "mileage": "", "kind": "service", "source_name": "Stratton Chevrolet Co", "source_loc": "Beloit, OH", "source_phone": "330-537-3151", "source_url": "strattonchevrolet.com", "source_rating": "5.0 / 5.0", "source_reviews": "134 Verified Reviews", "source_favorites": "200 Customer Favorites", "comments": ["Vehicle serviced", "Maintenance inspection completed", "Tire condition and pressure checked"]},
            {"date": "09/10/2020", "mileage": "", "kind": "service", "source_name": "Stratton Chevrolet Co", "source_loc": "Beloit, OH", "source_phone": "330-537-3151", "source_url": "strattonchevrolet.com", "source_rating": "5.0 / 5.0", "source_reviews": "134 Verified Reviews", "source_favorites": "200 Customer Favorites", "comments": ["Vehicle serviced", "Oil and filter changed"]},
            {"date": "02/22/2021", "mileage": "55,489", "kind": "service", "source_name": "Stratton Chevrolet Co", "source_loc": "Beloit, OH", "source_phone": "330-537-3151", "source_url": "strattonchevrolet.com", "source_rating": "5.0 / 5.0", "source_reviews": "134 Verified Reviews", "source_favorites": "200 Customer Favorites", "comments": ["Vehicle serviced", "Oil and filter changed"]},
            {"date": "08/19/2021", "mileage": "64,602", "kind": "service", "source_name": "Jim's Auto Care", "source_loc": "Hartville, OH", "source_phone": "330-877-6303", "source_url": "jimsautocarellc.com", "source_rating": "5.0 / 5.0", "source_reviews": "53 Verified Reviews", "source_favorites": "3 Customer Favorites", "comments": ["Vehicle serviced", "Oil and filter changed", "Tires rotated"]},
        ],
    },
    {
        "owner": 3,
        "purchased": "2021",
        "note": "Personal Vehicle",
        "type": "Personal Vehicle",
        "miles_per_year": "19,591 mi/yr",
        "events": [
            {"date": "09/27/2021", "mileage": "", "kind": "title", "source_name": "Ohio Motor Vehicle Dept.", "source_loc": "Hartville, OH", "title_no": "7605426816", "comments": ["Vehicle purchase reported", "Title issued or updated", "Registration issued or renewed", "New owner reported"]},
            {"date": "07/26/2022", "mileage": "73,310", "kind": "service", "source_name": "Stratton Chevrolet Co", "source_loc": "Beloit, OH", "source_phone": "330-537-3151", "source_url": "strattonchevrolet.com", "source_rating": "5.0 / 5.0", "source_reviews": "134 Verified Reviews", "source_favorites": "200 Customer Favorites", "comments": ["Vehicle serviced", "Oil and filter changed", "Tires rotated"]},
            {"date": "07/30/2022", "mileage": "75,513", "kind": "service", "source_name": "Walmart Auto Care Center", "source_loc": "Alliance, OH", "source_phone": "330-821-0595", "source_url": "walmart.com", "source_rating": "4.5 / 5.0", "source_reviews": "31 Verified Reviews", "comments": ["Vehicle serviced", "Tire(s) balanced", "Tire(s) replaced"]},
            {"date": "09/25/2022", "mileage": "77,387", "kind": "service", "source_name": "Mr. Tire Auto Service Centers", "source_loc": "Alliance, OH", "source_phone": "330-821-9491", "source_url": "mrtire.com", "source_rating": "4.7 / 5.0", "source_reviews": "51 Verified Reviews", "source_favorites": "1 Customer Favorite", "comments": ["Vehicle serviced", "Maintenance inspection completed", "Recommended maintenance performed", "Tire repaired", "Tire(s) balanced"]},
            {"date": "11/18/2022", "mileage": "78,889", "kind": "service", "source_name": "Stratton Chevrolet Co", "source_loc": "Beloit, OH", "source_phone": "330-537-3151", "source_url": "strattonchevrolet.com", "source_rating": "5.0 / 5.0", "source_reviews": "134 Verified Reviews", "source_favorites": "200 Customer Favorites", "comments": ["Vehicle serviced", "Maintenance inspection completed", "Recommended maintenance performed", "Body electrical system checked", "Body electrical wiring repaired", "Cooling system checked", "Oil and filter changed"]},
            {"date": "01/31/2023", "mileage": "", "kind": "registration", "source_name": "Ohio Motor Vehicle Dept.", "source_loc": "Hartville, OH", "title_no": "7605426816", "comments": ["Registration issued or renewed"]},
            {"date": "04/24/2023", "mileage": "", "kind": "service", "source_name": "Mr. Tire Auto Service Centers", "source_loc": "Hartville, OH", "source_phone": "330-877-0913", "source_url": "mrtire.com", "source_rating": "4.9 / 5.0", "source_reviews": "35 Verified Reviews", "comments": ["Vehicle serviced", "Maintenance inspection completed", "Recommended maintenance performed", "Tire repaired", "Tire(s) balanced"]},
            {"date": "04/25/2023", "mileage": "", "kind": "registration", "source_name": "Ohio Motor Vehicle Dept.", "source_loc": "Hartville, OH", "title_no": "7605426816", "comments": ["Registration issued or renewed"]},
            {"date": "05/25/2023", "mileage": "", "kind": "service", "source_name": "Stratton Chevrolet Co", "source_loc": "Beloit, OH", "source_phone": "330-537-3151", "source_url": "strattonchevrolet.com", "source_rating": "5.0 / 5.0", "source_reviews": "134 Verified Reviews", "source_favorites": "200 Customer Favorites", "comments": ["Vehicle serviced", "Oil and filter changed"]},
            {"date": "08/06/2023", "mileage": "", "kind": "damage", "severity": "minor", "location": "front", "comments": ["Accident reported: minor damage", "Involving front or side impact with another motor vehicle", "Damage to front", "Damage to right front", "Damage to left front", "Airbags did not deploy"]},
            {"date": "08/18/2023", "mileage": "", "kind": "service", "source_name": "Stratton Chevrolet Co", "source_loc": "Beloit, OH", "source_phone": "330-537-3151", "source_url": "strattonchevrolet.com", "source_rating": "5.0 / 5.0", "source_reviews": "134 Verified Reviews", "source_favorites": "200 Customer Favorites", "comments": ["Vehicle serviced", "Cooling system checked"]},
            {"date": "11/10/2023", "mileage": "94,999", "kind": "service", "source_name": "Stratton Chevrolet Co", "source_loc": "Beloit, OH", "source_phone": "330-537-3151", "source_url": "strattonchevrolet.com", "source_rating": "5.0 / 5.0", "source_reviews": "134 Verified Reviews", "source_favorites": "200 Customer Favorites", "comments": ["Vehicle serviced", "Oil and filter changed"]},
            {"date": "03/05/2024", "mileage": "", "kind": "registration", "source_name": "Ohio Motor Vehicle Dept.", "source_loc": "Hartville, OH", "title_no": "7605426816", "comments": ["Registration issued or renewed"]},
            {"date": "03/22/2024", "mileage": "102,323", "kind": "service", "source_name": "Stratton Chevrolet Co", "source_loc": "Beloit, OH", "source_phone": "330-537-3151", "source_url": "strattonchevrolet.com", "source_rating": "5.0 / 5.0", "source_reviews": "134 Verified Reviews", "source_favorites": "200 Customer Favorites", "comments": ["Vehicle serviced", "Oil and filter changed"]},
            {"date": "07/27/2024", "mileage": "109,819", "kind": "service", "source_name": "Mr. Tire Auto Service Centers", "source_loc": "Hartville, OH", "source_phone": "330-877-0913", "source_url": "mrtire.com", "source_rating": "4.9 / 5.0", "source_reviews": "35 Verified Reviews", "comments": ["Vehicle serviced", "Maintenance inspection completed", "Recommended maintenance performed", "Battery/charging system checked", "Brakes checked", "Brakes serviced", "Oil and filter changed", "Tires rotated"]},
            {"date": "11/19/2024", "mileage": "117,509", "kind": "service", "source_name": "Stratton Chevrolet Co", "source_loc": "Beloit, OH", "source_phone": "330-537-3151", "source_url": "strattonchevrolet.com", "source_rating": "5.0 / 5.0", "source_reviews": "134 Verified Reviews", "source_favorites": "200 Customer Favorites", "comments": ["Vehicle serviced", "Oil and filter changed"]},
            {"date": "01/23/2025", "mileage": "", "kind": "service", "source_name": "Mr. Tire Auto Service Centers", "source_loc": "Hartville, OH", "source_phone": "330-877-0913", "source_url": "mrtire.com", "source_rating": "4.9 / 5.0", "source_reviews": "35 Verified Reviews", "comments": ["Vehicle serviced", "Maintenance inspection completed", "Recommended maintenance performed", "Battery/charging system checked", "Brakes checked", "Brakes serviced", "Fluids checked", "Oil and filter changed", "Tires rotated"]},
            {"date": "03/13/2025", "mileage": "", "kind": "registration", "source_name": "Ohio Motor Vehicle Dept.", "source_loc": "Hartville, OH", "title_no": "7605426816", "comments": ["Registration issued or renewed"]},
            {"date": "03/21/2025", "mileage": "123,347", "kind": "service", "source_name": "Stratton Chevrolet Co", "source_loc": "Beloit, OH", "source_phone": "330-537-3151", "source_url": "strattonchevrolet.com", "source_rating": "5.0 / 5.0", "source_reviews": "134 Verified Reviews", "source_favorites": "200 Customer Favorites", "comments": ["Vehicle serviced", "Maintenance reminder reset", "Oil and filter changed"]},
            {"date": "05/21/2025", "mileage": "128,595", "kind": "service", "source_name": "Stratton Chevrolet Co", "source_loc": "Beloit, OH", "source_phone": "330-537-3151", "source_url": "strattonchevrolet.com", "source_rating": "5.0 / 5.0", "source_reviews": "134 Verified Reviews", "source_favorites": "200 Customer Favorites", "comments": ["Vehicle serviced", "Four tires replaced", "Maintenance reminder reset", "Oil and filter changed"], "oil_note": True},
        ],
    },
]


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value))


def fmt_date(value: Any) -> str:
    if not value:
        return "—"
    s = str(value).strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%d/%m/%Y", "%Y%m%d"):
        try:
            return datetime.strptime(s, fmt).strftime("%m/%d/%Y")
        except ValueError:
            continue
    return s


def _section(title: str, subtitle: str) -> str:
    return (f'<div class="section-header"><div class="section-title">{esc(title)}</div>'
            f'<div class="section-subtitle">{esc(subtitle)}</div></div>')


def _severity_scale(active: str = "minor", mini: bool = False) -> str:
    if mini:
        segs = []
        for key, cls in [("minor", "seg-mini-minor"), ("moderate", "seg-mini-moderate"), ("severe", "seg-mini-severe")]:
            active_cls = " seg-active" if key == active else ""
            segs.append(f'<div class="seg {cls}{active_cls}">{key.capitalize()}</div>')
        return f'<div class="severity-mini">{"".join(segs)}</div>'
    segs = []
    for key, cls in [("minor", "seg-minor"), ("moderate", "seg-moderate"), ("severe", "seg-severe")]:
        active_cls = " seg-active" if key == active else ""
        segs.append(f'<div class="severity-seg {cls}{active_cls}">{key.capitalize()}</div>')
    return (f'<div class="severity-scale"><div class="sc-label">Damage Severity Scale</div>'
            f'<div class="severity-segs">{"".join(segs)}</div></div>')


def _damage_location(location: str = "front") -> str:
    hit_html = ""
    if location in ("front", "left", "right", "rear"):
        hit_html = '<div class="hit"></div><div class="hit-lbl">IMPACT</div>'
    return f'''<div class="damage-loc">
      <div class="dl-title">Damage Location</div>
      <div class="car-diagram">
        <div class="dl-front">FRONT</div>
        <div class="dl-mid">
          <div class="dl-side">LEFT</div>
          <div class="dl-body">{hit_html}</div>
          <div class="dl-side">RIGHT</div>
        </div>
        <div class="dl-rear">REAR</div>
      </div>
    </div>'''


def build_listing_banner(highlights: dict[str, Any] | None) -> str:
    return f'''<div class="listing-banner">
      <div class="lb-title">Display Car Inspection Pro in online listings:</div>
    </div>'''


def build_highlights(highlights: dict[str, Any] | None) -> str:
    highlights = highlights or SAMPLE_HIGHLIGHTS

    # Always prepare all 5 rows
    severity = str(highlights.get("accident_severity") or "minor damage")
    severity_key = severity.lower().split()[0]

    owners = highlights.get("owners")
    owners_text = f"{owners} Previous owners" if owners else "Previous owners"

    owner_type = str(
        highlights.get("owner_type") or "Personal lease, Personal"
    )

    odometer = highlights.get("odometer")
    if odometer not in (None, ""):
        try:
            odometer_text = f"{int(odometer):,}"
        except (TypeError, ValueError):
            odometer_text = str(odometer)
    else:
        odometer_text = "Not reported"

    return f'''
    <div class="highlights">

        <!-- ROW 1: Accident -->
        <div class="hl-tile">
            <div class="hl-icon">
                {ICON_ACCIDENT}
            </div>

            <div class="hl-content">
                <div class="hl-value">
                    Accident reported: {esc(severity)}
                </div>
                {_severity_scale(severity_key, mini=True)}
            </div>
        </div>

        <!-- ROW 2: Oil changes -->
        <div class="hl-tile">
            <div class="hl-icon">
                {ICON_WELL_MAINTAINED}
            </div>

            <div class="hl-content">
                <div class="hl-value">
                    Regular oil changes
                </div>
            </div>
        </div>

        <!-- ROW 3: Previous owners -->
        <div class="hl-tile">
            <div class="hl-icon">
                {ICON_OWNERS}
            </div>

            <div class="hl-content">
                <div class="hl-value">
                    {esc(owners_text)}
                </div>
            </div>
        </div>

        <!-- ROW 4: Types of owners -->
        <div class="hl-tile">
            <div class="hl-icon">
                {ICON_OWNER_TYPE}
            </div>

            <div class="hl-content">
                <div class="hl-value">
                    Types of owners: {esc(owner_type)}
                </div>
            </div>
        </div>

        <!-- ROW 5: Odometer -->
        <div class="hl-tile">
            <div class="hl-icon hl-icon-sm">
                {ICON_GOOD}
            </div>

            <div class="hl-content">
                <div class="hl-value">
                    {esc(odometer_text)} Last reported odometer reading
                </div>
            </div>
        </div>

    </div>
    '''


def build_summary(report: dict[str, Any], highlights: dict[str, Any] | None) -> str:
    v = report.get("vehicle") or {}
    make = v.get("Make", "")
    model = v.get("Model", "")
    year = v.get("ModelYear", "")
    trim = v.get("Trim", "")
    vin = report.get("vin", "")

    cyl = str(v.get("EngineCylinders", "") or "")
    roman = {"4": "I4", "6": "V6", "8": "V8", "3": "I3", "5": "I5", "10": "V10", "12": "V12"}
    cyl = roman.get(cyl, f"{cyl}-cyl") if cyl else "—"
    engine = f"{v.get('DisplacementL', '—')}L {cyl}".replace("L —", "—")
    body = v.get("BodyClass", "—")
    fuel = v.get("FuelTypePrimary", "—")
    drive = v.get("DriveType", "—")

    specs = [
        body,
        engine,
        fuel,
        drive,
    ]
    spec_html = "".join(f'<div class="spec">{esc(val)}</div>' for val in specs)

    photo = v.get("photo_url") or v.get("Photo")
    if photo:
        photo_html = f'<div class="vehicle-mascot"><img src="{esc(photo)}" alt=""/></div>'
    else:
        photo_html = ""

    line1 = f"{year} {make}"
    line2 = f"{model} {trim}".strip()

    return f'''<div class="summary">
      <div class="summary-left">
        <div style="position: relative; margin-bottom: 8px;">
          <div class="vehicle-title">{esc(line1)}<br/>{esc(line2)}</div>
          <div class="vin-line">VIN: <b>{esc(vin)}</b></div>
        </div>
        <div class="summary-specs">{spec_html}</div>
      </div>
      <div class="summary-right">
          {build_highlights(highlights)}
          <div class="vehicle-mascot">
              {FOX_MASCOT}
          </div>
      </div>
    </div>'''


def build_accident_section(accidents: list[dict[str, Any]]) -> str:
    accidents = accidents or []
    if not accidents:
        return ""
    blocks = []
    for i, a in enumerate(accidents[:3], start=1):
        severity = (a.get("severity") or "minor").lower()
        airbags = a.get("airbags", "")
        date = fmt_date(a.get("date"))
        blocks.append(f'''
        <div class="accident-card">
          <div class="event-top">
            <div class="ev-icon">{ICON_ACCIDENT}</div>
            <div class="ev-body">
              <div class="event-badge">Event {i}</div>
              <div class="ev-date">{esc(date)}</div>
              <div class="ev-title">Accident reported: {esc(a.get('type', 'minor damage'))}</div>
              <div class="ev-desc">{esc(a.get('description', 'Involving front or side impact with another motor vehicle'))}</div>
              {f'<div class="ev-desc">{esc(airbags)}</div>' if airbags else ""}
            </div>
          </div>
          <div class="severity-side">
            {_severity_scale(severity)}
          </div>
        </div>''')
    return (f'<div class="section">{_section("Accident / Damage History", "Not all accidents / issues are reported to Car Inspection Pro")}'
            f'{"".join(blocks)}'
            f'<div class="info-banner">Car Inspection Pro has the most accident &amp; damage information</div></div>')


def build_service_section(services: list[dict[str, Any]]) -> str:
    services = services or []
    if not services:
        return ""
    rows = "".join(
        f'<tr>'
        f'<td><div class="service-cell">{ICON_SERVICE}<strong>{esc(s.get("service", "Service"))}</strong></div></td>'
        f'<td>{esc(s.get("notes", ""))}</td>'
        f'<td>{esc(fmt_date(s.get("date")))}</td>'
        f'<td></td>'
        f'</tr>'
        for s in services[:6]
    )
    return f'''<div class="section">{_section("Recent Service Highlights", "Key services performed in the last 12 months")}
      <table class="service-table">
        <thead><tr><th style="width: 24%;">Service</th><th style="width: 38%;">Comments</th><th style="width: 22%;">Date</th><th style="width: 16%;"></th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
      <div class="good-note">{ICON_GOOD} This car has been recently serviced. That's a good thing!</div>
    </div>'''


def build_additional_history(owners_data: dict[str, dict[str, str]] | None = None) -> str:
    if not owners_data:
        owners_data = SAMPLE_OWNERS_CHECKS
    owner_keys = list(owners_data.keys())
    owner_th = "".join(f"<th>Owner {i+1}</th>" for i in range(len(owner_keys)))

    checks = [
        ("Total Loss", "No total loss reported to Car Inspection Pro.", "total_loss"),
        ("Structural Damage", "Car Inspection Pro recommends that you have this vehicle inspected by a collision repair specialist.", "structural_damage"),
        ("Airbag Deployment", "No airbag deployment reported to Car Inspection Pro.", "airbag_deployment"),
        ("Odometer Check", "No indication of an odometer rollback.", "odometer_check"),
        ("Accident / Damage", "Accident reported based on NHTSA complaint data.", "accident_damage"),
        ("Fire", "No fire incidents reported to NHTSA.", "fire"),
        ("Manufacturer Recall", "No open recalls reported to Car Inspection Pro.", "manufacturer_recall"),
        ("Basic Warranty", "Original warranty estimated to have expired.", "basic_warranty"),
    ]

    rows = ""
    for title_, desc, key in checks:
        rows += f'''<tr>
          <td><div class="check-title">{esc(title_)}</div><div class="check-desc">{esc(desc)}</div></td>'''
        for owner_key in owner_keys:
            status = owners_data.get(owner_key, {}).get(key, "No Issues Reported")
            has_issue = ("complaint" in status.lower() or "recall" in status.lower()
                         or "crash" in status.lower() or "fire" in status.lower()
                         or "Minor Damage" in status or "Warranty Expired" in status)
            no_issue = status.startswith("No ") or status == "No Issues Indicated"
            if has_issue:
                rows += f'<td><span class="status-label warn">{TICK}{esc(status)}</span></td>'
            elif no_issue:
                rows += f'<td><span class="status-label ok">{TICK}{esc(status)}</span></td>'
            else:
                rows += f'<td><span class="status-label">{TICK}{esc(status)}</span></td>'
        rows += '</tr>'

    return f'''<div class="section">
      <div class="section-box">
      {_section("Additional History", "Not all accidents / issues are reported to Car Inspection Pro")}
      <table class="history-table">
        <thead><tr><th></th>{owner_th}</tr></thead>
        <tbody>{rows}</tbody>
      </table>
      </div>
    </div>'''


def build_theft_records(theft_records: list[dict[str, Any]] | None = None) -> str:
    """Build Theft Records section."""
    if not theft_records:
        # No theft records - show clean status
        return f'''<div class="section">
      <div class="section-box">
      {_section("Theft Records", "Checked against NMVTIS and insurance databases")}
      <table class="history-table">
        <thead><tr><th></th><th>Status</th></tr></thead>
        <tbody>
          <tr>
            <td>
              <div class="check-title">Theft / Stolen Vehicle</div>
              <div class="check-desc">Reported stolen status from NMVTIS and participating insurance databases</div>
            </td>
            <td><span class="status-label ok">{TICK}No Issues Reported</span></td>
          </tr>
        </tbody>
      </table>
      </div>
    </div>'''

    # Build rows for each theft record
    rows = ""
    for rec in theft_records:
        date = esc(rec.get("date", "—"))
        status = esc(rec.get("status", "Reported"))
        desc = esc(rec.get("description", ""))
        rows += f'''<tr>
            <td>
              <div class="check-title">Theft / Stolen Vehicle</div>
              <div class="check-desc">{desc}</div>
            </td>
            <td>
              <div><b>Date:</b> {date}</div>
              <div><b>Status:</b> {status}</div>
            </td>
          </tr>'''

    return f'''<div class="section">
      <div class="section-box">
      {_section("Theft Records", "Checked against NMVTIS and insurance databases")}
      <table class="history-table">
        <thead><tr><th></th><th>Details</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
      </div>
    </div>'''


def build_title_history(title_data: dict[str, Any] | None = None) -> str:
    td = title_data or {}
    damage_clean = td.get("damage_brands_clean", True)
    odometer_clean = td.get("odometer_brands_clean", True)
    damage_brands = td.get("damage_brands") or []
    odometer_brands = td.get("odometer_brands") or []

    if damage_clean:
        damage_status = f'{TICK}Not Reported'
        damage_cls = ""
    else:
        brands_str = ", ".join(damage_brands) if damage_brands else "Reported"
        damage_status = f"{brands_str}"
        damage_cls = " warn"

    if odometer_clean:
        odo_status = f'{TICK}Not Reported'
        odo_cls = ""
    else:
        odo_str = ", ".join(odometer_brands) if odometer_brands else "Reported"
        odo_status = f"{odo_str}"
        odo_cls = " warn"

    # Build owner columns
    owner_count = max(1, len(td.get("owners") or []))
    owner_cols = "".join(f"<th>Owner {i+1}</th>" for i in range(owner_count))

    damage_rows = "".join(
        f'<td><span class="status-label{damage_cls}">{esc(damage_status)}</span></td>'
        for _ in range(owner_count)
    )
    odo_rows = "".join(
        f'<td><span class="status-label{odo_cls}">{esc(odo_status)}</span></td>'
        for _ in range(owner_count)
    )

    return f'''<div class="section">
      <div class="section-box">
      {_section("Title History", "Car Inspection Pro guarantees the information in this section")}
      <table class="history-table">
        <thead><tr><th></th>{owner_cols}</tr></thead>
        <tbody>
          <tr>
            <td>
              <div class="check-title">Damage Brands</div>
              <div class="check-desc">Salvage | Junk | Rebuilt | Fire | Flood | Hail | Lemon</div>
            </td>
            {damage_rows}
          </tr>
          <tr>
            <td>
              <div class="check-title">Odometer Brands</div>
              <div class="check-desc">Not Actual Mileage | Exceeds Mechanical Limits</div>
            </td>
            {odo_rows}
          </tr>
        </tbody>
      </table>
      </div>
      <div class="guarantee-box">
        <div class="guarantee-label">{ICON_GUARANTEED}GUARANTEED</div>
        <p>Title brand information is based on NMVTIS data supplied to Car Inspection Pro. For complete title history, additional data providers may be consulted.</p>
        <div class="terms-links">View Terms | View Certificate</div>
      </div>
    </div>'''


def build_ownership_history(owners_data: list[dict[str, str]] | None = None) -> str:
    if not owners_data:
        owners_data = SAMPLE_OWNERS_OWNERSHIP
    if not owners_data:
        return ""
    owner_cols = "".join(
        f"<th>Owner {o.get('number', i+1)}</th>" for i, o in enumerate(owners_data)
    )
    rows = ""
    for key_label, key in [
        ("Year purchased", "year_purchased"),
        ("Type of owner", "type"),
        ("Estimated length of ownership", "length_of_ownership"),
        ("Owned in the following states/provinces", "state"),
        ("Estimated miles driven per year", "miles_per_year"),
        ("Last reported odometer reading", "odometer"),
    ]:
        rows += f"<tr><td>{esc(key_label)}</td>"
        for owner in owners_data:
            val = owner.get(key, "—")
            rows += f"<td>{esc(val)}</td>"
        rows += "</tr>"

    return f'''<div class="section">
      <div class="section-box">
      {_section("Ownership History", "The number of owners is estimated")}
      <table class="ownership-table">
        <thead><tr><th></th>{owner_cols}</tr></thead>
        <tbody>{rows}</tbody>
      </table>
      </div>
    </div>'''


def _detail_source(ev: dict[str, Any]) -> str:
    parts = []
    if ev.get("source_name"):
        parts.append(f'<span class="src-name">{esc(ev["source_name"])}</span>')
    if ev.get("source_loc"):
        parts.append(f'<span>{esc(ev["source_loc"])}</span>')
    if ev.get("source_phone"):
        parts.append(f'<span>{esc(ev["source_phone"])}</span>')
    if ev.get("source_url"):
        parts.append(f'<span>{esc(ev["source_url"])}</span>')
    if ev.get("title_no"):
        parts.append(f'<span>Title #{esc(ev["title_no"])}</span>')
    sub = ""
    if ev.get("source_rating"):
        sub = f'<div class="rating-line">{esc(ev["source_rating"])}</div>'
    if ev.get("source_reviews"):
        sub += f'<div class="reviews-line">{esc(ev["source_reviews"])}</div>'
    if ev.get("source_favorites"):
        sub += f'<div class="reviews-line">{esc(ev["source_favorites"])}</div>'
    if ev.get("vehicle_color"):
        sub += f'<div class="reviews-line">{esc(ev["vehicle_color"])}</div>'
    if ev.get("vehicle_interior"):
        sub += f'<div class="reviews-line">{esc(ev["vehicle_interior"])}</div>'
    return f'<div class="src-sub">{"<br/>".join(parts)}</div>{sub}'


def _detail_comments(ev: dict[str, Any]) -> str:
    comments = ev.get("comments") or []
    if not comments:
        return ""
    kind = ev.get("kind") or ""
    icon_map = {
        "service": ICON_SERVICE,
        "recall": ICON_SERVICE,
        "damage": ICON_SERVICE,
        "fire": ICON_SERVICE,
        "complaint": ICON_SERVICE,
        "tsb": ICON_SERVICE,
        "investigation": ICON_SERVICE,
        "inventory": ICON_SERVICE,
        "purchase": ICON_SERVICE,
        "title": ICON_SERVICE,
        "registration": ICON_SERVICE,
        "cpo": ICON_SERVICE,
    }
    icon = icon_map.get(kind, "")
    lines = []
    first = True
    for c in comments:
        if first:
            lines.append(f'<span class="evt-line main">{icon}{esc(c)}</span>')
            first = False
        else:
            lines.append(f'<span class="evt-line">{esc(c)}</span>')
    out = "".join(lines)
    if ev.get("good"):
        out += '<span class="evt-note">That&rsquo;s a good thing!</span>'
    if ev.get("oil_note"):
        out += ('<span class="evt-note">This vehicle uses an indicator light to alert users when it\'s time to change the oil. '
                'Oil changes have been reported at least every 7,500 miles, which is in line with manufacturer guidelines.</span>')
    return out


def _detail_damage_box(ev: dict[str, Any]) -> str:
    severity = (ev.get("severity") or "minor").lower()
    return f'''<div class="detail-damage">
      {_detail_comments(ev)}
      <div class="severity-side">
        {_severity_scale(severity)}
        {_damage_location(ev.get("location", "front"))}
      </div>
    </div>'''


def build_detailed_history(history: list[dict[str, Any]] | None = None) -> str:
    if not history:
        history = SAMPLE_DETAILED_HISTORY
    if not history:
        return ""
    first = True
    owners = ""
    for o in history:
        rows = ""
        for ev in o.get("events", []):
            kind = ev.get("kind") or ""
            if kind in ("damage", "fire"):
                comments_td = _detail_damage_box(ev)
            else:
                comments_td = _detail_comments(ev)
            rows += f'''<tr>
              <td class="td-date">{esc(fmt_date(ev.get("date")))}</td>
              <td class="td-miles">{esc(ev.get("mileage", ""))}</td>
              <td class="td-source">{_detail_source(ev)}</td>
              <td class="td-comments">{comments_td}</td>
            </tr>'''
        heading = _section("Detailed History", "") if first else ""
        first = False
        owners += f'''<div class="detail-owner">
          {heading}
          <div class="detail-owner-card">
            <div>
              <div class="own-id">Owner {esc(o.get("owner"))}</div>
              <div class="own-purchased">Purchased: {esc(o.get("purchased"))}</div>
            </div>
            <div class="own-note">{esc(o.get("note", ""))}</div>
            <div class="own-right">
              <div class="own-type">{esc(o.get("type", ""))}</div>
              <div class="own-mpy">{esc(o.get("miles_per_year", ""))}</div>
            </div>
          </div>
          <table class="detail-table">
            <thead><tr><th>Date</th><th>Mileage</th><th>Source</th><th>Comments</th></tr></thead>
            <tbody>{rows}</tbody>
          </table>
        </div>'''
    return f'''<div class="section" style="page-break-inside: avoid;">
      {owners}
    </div>'''


def build_glossary() -> str:
    return f'''<div class="section">
      <div class="section-box">
      {_section("Glossary", "")}
      <dl class="glossary">
        <dt>Accident Indicator</dt>
        <dd>Car Inspection Pro receives information about accidents in all 50 states, the District of Columbia and Canada. Not every accident is reported to Car Inspection Pro. As details about the accident become available, those additional details are added to the Vehicle History Report. Car Inspection Pro recommends that you have this vehicle inspected by a qualified mechanic.</dd>
        <dt>Well Maintained - Regular Oil Changes</dt>
        <dd>Car Inspection Pro identifies a "Well Maintained - Regular Oil Changes" vehicle as having a regular oil change history when all its recommended oil changes, based on the vehicle's maintenance schedule, have been reported to Car Inspection Pro. Car Inspection Pro uses the manufacturer's schedule and assumes normal driving conditions. When an oil change schedule is not available, Car Inspection Pro may analyze reported service events to determine what is typical for the same make and model vehicle. Dealers and service shops may publish different recommended service schedules.</dd>
        <dt>Damage Severity</dt>
        <dd>Damage events result in one of the following severity levels: Minor - generally cosmetic damage including dents or scratches; Moderate - more extensive damage that may impair the operation of the vehicle; Severe - significant damage that may make the vehicle unsafe to drive.</dd>
        <dt>First Owner</dt>
        <dd>When the first owner(s) obtains a title from a Department of Motor Vehicles as proof of ownership.</dd>
        <dt>New Owner Reported</dt>
        <dd>When a vehicle is sold to a new owner, the title must be transferred to the new owner(s) at a Department of Motor Vehicles.</dd>
        <dt>Ownership History</dt>
        <dd>Car Inspection Pro defines an owner as an individual or business that possesses and uses a vehicle. Not all title transactions represent changes in ownership. To provide an estimated number of owners, Car Inspection Pro's proprietary technology analyzes all the events in a vehicle history. Estimated ownership is available for vehicles manufactured after 1991 and titled solely in the US including Puerto Rico.</dd>
        <dt>Title Issued</dt>
        <dd>A state issues a title to provide a vehicle owner with proof of ownership. Each title has a unique number. Each title or registration record on a report does not necessarily indicate a change in ownership.</dd>
        <dt>VIN</dt>
        <dd>Vehicle Identification Number — a 17-character code that uniquely identifies a vehicle.</dd>
        <dt>Manufacturer Recall</dt>
        <dd>A safety defect or non-compliance with Federal Motor Vehicle Safety Standards that a manufacturer must remedy free of charge.</dd>
        <dt>Owner Complaint</dt>
        <dd>An issue a vehicle owner reported to NHTSA's complaints database for the same model.</dd>
        <dt>Technical Service Bulletin (TSB)</dt>
        <dd>A manufacturer's recommended repair procedure for a known condition, typically not a safety recall.</dd>
        <dt>NHTSA Investigation</dt>
        <dd>An inquiry opened by NHTSA when complaints or field reports suggest a possible safety defect.</dd>
      </dl>
      </div>
    </div>'''


def build_report_html(
    report: dict[str, Any],
    report_no: str,
    issued_on: str,
    highlights: dict[str, Any] | None = None,
    accidents: list[dict[str, Any]] | None = None,
    services: list[dict[str, Any]] | None = None,
    owners_history_checks: dict[str, dict[str, str]] | None = None,
    owners_ownership: list[dict[str, str]] | None = None,
    detailed_history: list[dict[str, Any]] | None = None,
    theft_records: list[dict[str, Any]] | None = None,
    title_history: dict[str, Any] | None = None,
    nmvtis_available: bool = True,
    plan_id: str = "gold",
) -> str:
    v = report.get("vehicle") or {}
    make = v.get("Make", "")
    model = v.get("Model", "")
    year = v.get("ModelYear", "")
    trim = v.get("Trim", "")
    vin = report.get("vin", "")
    title = f"{year} {make} {model} {trim}".strip()
    vehicle_label = title or "this vehicle"

    plan_id = (plan_id or "gold").lower()

    # All plans (basic, gold, premium) include the full report.
    # Plans differ only in the number of reports purchased, not the data depth.
    include_nmvtis = True

    highlights = highlights if highlights is not None else SAMPLE_HIGHLIGHTS
    accident_html = build_accident_section(accidents if (accidents is not None and include_nmvtis) else None)
    service_html = build_service_section(services if (services is not None and include_nmvtis) else None)
    page2_additional = build_additional_history(owners_history_checks if (owners_history_checks is not None and include_nmvtis) else None)
    theft_html = build_theft_records(theft_records if include_nmvtis else None)
    title_history = build_title_history(title_history if include_nmvtis else None)
    ownership_history = build_ownership_history(owners_ownership if (owners_ownership is not None and include_nmvtis) else None)
    detailed_history = build_detailed_history(detailed_history if (detailed_history is not None and include_nmvtis) else None)

    header = f'''<div class="header-bar">
      <div class="header-accent"></div>
      <div class="header-inner">
        <div class="header-left">
          {LOGO}
        </div>
        <div class="header-center">
          <div class="header-title">Vehicle History Report</div>
          <div class="header-subtitle">Car Inspection Pro &mdash; Powered by NMVTIS &amp; NHTSA</div>
        </div>
        <div class="header-right">
          <div class="header-price">US ${esc(PRICE_USD)}</div>
          <div class="header-price-label">Per Report</div>
        </div>
      </div>
    </div>'''

    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><style>{CSS}</style></head>
<body>
  {build_listing_banner(highlights)}

  {header}

  {build_summary(report, highlights)}

  <div class="top-note">
    This Car Inspection Pro Vehicle History Report is based only on information supplied to Car Inspection Pro and available as of
    {esc(issued_on)}. Other information about this vehicle, including problems, may not have been reported to Car Inspection Pro.
    Use this report as one important tool, along with a vehicle inspection and test drive, to make a better decision
    about your next used car.
  </div>

  {"<div class='nmvtis-banner'><div class='nmvtis-banner-icon'>&#9888;</div><div class='nmvtis-banner-text'><b>NMVTIS Data Unavailable</b><br>National Motor Vehicle Title Information System data could not be retrieved at this time. The sections below (Title History, Ownership History, Theft Records, Service History, and Accident/Damage History from NMVTIS) reflect NHTSA data only. For a complete report with NMVTIS data included, please ensure account credits are available and regenerate this report.</div></div>" if not nmvtis_available else ""}

  {accident_html}

  {service_html}

  {page2_additional}

  {theft_html}

  {title_history}

  {ownership_history}

  {detailed_history}

  <div class="have-questions">
    <b>Have Questions?</b> Consumers, please visit our Help Center at www.carinspectionpro.com. Dealers or Subscribers, please visit our Help Center at www.carinspectionpro.com.
  </div>

  {build_glossary()}

  <div class="footer">
    Car Inspection Pro Vehicle History Report for this {esc(vehicle_label)}: {esc(vin)}
    &nbsp;·&nbsp; Report No. {esc(report_no)} &nbsp;·&nbsp; Issued {esc(issued_on)}
    <br>
    <b>Disclaimer:</b> This report is based only on information supplied to Car Inspection Pro and available as of {esc(issued_on)}.
    Other information about this vehicle, including problems, may not have been reported to Car Inspection Pro. Use this report as one
    important tool, along with a vehicle inspection and test drive, to make a better decision about your next used car.
  </div>

  <div class="review-stmt">
    I have reviewed and received a copy of the Car Inspection Pro Vehicle History Report for this {esc(vehicle_label)}
    vehicle (VIN: {esc(vin)}), which is based on information supplied to Car Inspection Pro and available as of {esc(issued_on)}.
  </div>

  <div class="signatures">
    <div class="sig"><div class="line"></div><div class="cap">Customer Signature &nbsp;Date</div></div>
    <div class="sig"><div class="line"></div><div class="cap">Dealer Signature &nbsp;Date</div></div>
  </div>

  <div class="copyright">© {datetime.now().year} Car Inspection Pro. All rights reserved.</div>
</body>
</html>"""


def make_report_number(vin: str) -> str:
    now = datetime.now()
    return f"CIP-{now:%Y%m%d}-{vin[-6:].upper()}-{now:%H%M%S}"


# ---- Example Usage ----
if __name__ == "__main__":
    report_data = {
        "vin": "1G1PC5SB5F7121276",
        "vehicle": {
            "ModelYear": 2015,
            "Make": "CHEVROLET",
            "Model": "CRUZE",
            "BodyClass": "Sedan 4 DR",
            "DisplacementL": "1.4",
            "EngineCylinders": "4",
            "FuelTypePrimary": "Gasoline",
            "DriveType": "Front Wheel Drive",
        }
    }

    html = build_report_html(
        report_data,
        make_report_number(report_data["vin"]),
        datetime.now().strftime("%m/%d/%Y"),
    )

    with open("/tmp/carinspectionpro_report.html", "w") as f:
        f.write(html)
    print("Report generated: /tmp/carinspectionpro_report.html")
