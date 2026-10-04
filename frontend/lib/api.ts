export type Vehicle = {
  Make: string;
  Model: string;
  ModelYear: string;
  BodyClass: string;
  DisplacementL: string;
  EngineCylinders: string;
  EngineHP: string;
  FuelTypePrimary: string;
  DriveType: string;
  PlantCity: string;
  PlantCountry: string;
  Trim: string;
  Series: string;
  Doors: string;
  VIN: string;
  [key: string]: unknown;
};

export type Recall = {
  NHTSACampaignNumber: string;
  ReportReceivedDate: string;
  Component: string;
  Summary: string;
  Consequence: string;
  Remedy: string;
  [key: string]: unknown;
};

export type Complaint = {
  ODTI?: string;
  Component?: string;
  DateComplaintFiled?: string;
  Summary?: string;
  Consequence?: string;
  dateOfIncident?: string;
  crash?: boolean;
  fire?: boolean;
  numberOfDeaths?: number;
  numberOfInjuries?: number;
  manufacturer?: string;
  [key: string]: unknown;
};

export type Fuel = {
  make: string;
  model: string;
  year: string;
  VClass: string;
  trany: string;
  drive: string;
  cylinders: string;
  displ: string;
  fuelType1: string;
  city08: string;
  highway08: string;
  comb08: string;
  co2: string;
  feScore: string;
  ghgScore: string;
  [key: string]: unknown;
};

export type Safety = {
  VehicleDescription: string;
  OverallRating: string;
  OverallFrontCrashRating: string;
  FrontCrashDriversideRating: string;
  FrontCrashPassengersideRating: string;
  OverallSideCrashRating: string;
  SideCrashDriversideRating: string;
  SideCrashPassengersideRating: string;
  SidePoleCrashRating: string;
  RolloverRating: string;
  RolloverRating2: string;
  RolloverPossibility: number | string;
  FrontCrashPicture?: string | null;
  FrontCrashVideo?: string | null;
  SideCrashPicture?: string | null;
  SideCrashVideo?: string | null;
  SidePolePicture?: string | null;
  SidePoleVideo?: string | null;
  VehiclePicture?: string | null;
  [key: string]: unknown;
};

export type Tsb = {
  doc_id: string;
  make: string;
  model: string;
  model_year: string;
  summary: string;
  source_file: string;
  [key: string]: unknown;
};

export type Investigation = {
  action_no: string;
  make: string;
  model: string;
  year: string;
  component: string;
  mfr_name: string;
  date_opened: string;
  date_closed: string;
  campno: string;
  subject: string;
  summary: string;
  [key: string]: unknown;
};

export type VinReport = {
  vin: string;
  vehicle: Vehicle | null;
  recalls: Recall[];
  complaints: Complaint[];
  tsbs: Tsb[];
  investigations: Investigation[];
  safety: Safety[];
  fuel: Fuel | null;
  statuses?: Record<string, "ok" | "unavailable">;
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "";

export function getPdfPreviewUrl(vin: string): string {
  // #toolbar=0 hides the viewer toolbar (download/print buttons) in Chrome/Edge;
  // #navpanes=0 hides the sidebar.
  return `${API_BASE}/api/vin/${encodeURIComponent(vin)}/pdf/preview#toolbar=0&navpanes=0`;
}

async function readDetail(res: Response): Promise<string> {
  let detail = `Request failed (${res.status})`;
  try {
    const body = await res.json();
    detail = body.detail ?? detail;
  } catch {
    // ignore parse errors
  }
  return detail;
}

export async function fetchVinReport(vin: string): Promise<VinReport> {
  const res = await fetch(`${API_BASE}/api/vin/${encodeURIComponent(vin)}`, {
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(await readDetail(res));
  }
  return res.json();
}

export type VinDecode = {
  vin: string;
  vehicle: {
    Make: string;
    Model: string;
    ModelYear: string;
    Trim: string;
    BodyClass: string;
    DisplacementL: string;
    EngineCylinders: string;
    EngineHP: string;
    FuelTypePrimary: string;
    DriveType: string;
    Doors: string;
    TransmissionStyle: string;
    PlantCity: string;
    PlantState: string;
    PlantCountry: string;
    Series: string;
    VehicleType: string;
    ManufacturerName: string;
  };
};

export async function fetchVinDecode(vin: string): Promise<VinDecode> {
  const res = await fetch(`${API_BASE}/api/vin/${encodeURIComponent(vin)}/decode`, {
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(await readDetail(res));
  }
  return res.json();
}

export async function generateReport(vin: string, plan: string): Promise<Blob> {
  const res = await fetch(
    `${API_BASE}/api/vin/${encodeURIComponent(vin)}/generate-report?plan=${plan}`,
    { method: "POST" },
  );
  if (!res.ok) {
    throw new Error(await readDetail(res));
  }
  return res.blob();
}

export function validateVin(vin: string): string | null {
  const clean = vin.trim().toUpperCase();
  if (clean.length !== 17) {
    return "VIN must be exactly 17 characters.";
  }
  if (/[IOQ]/.test(clean)) {
    return "VIN cannot contain the letters I, O, or Q.";
  }
  if (!/^[A-HJ-NPR-Z0-9]{17}$/.test(clean)) {
    return "VIN contains invalid characters.";
  }
  if (!checkVinChecksum(clean)) {
    return "VIN failed the check digit (checksum) validation.";
  }
  return null;
}

export type QuickBooksStatus = {
  configured: boolean;
  client_id?: string | null;
  env: string;
  realm_id?: string | null;
};

export async function fetchQuickBooksStatus(): Promise<QuickBooksStatus> {
  const res = await fetch(`${API_BASE}/api/quickbooks/status`, { cache: "no-store" });
  if (!res.ok) {
    return { configured: false, env: "sandbox", client_id: null, realm_id: null };
  }
  return res.json();
}

export type PdfCheckoutResult = {
  order_id: string;
  provider: string;
  price_usd: number;
  plan: string;
  reports: number;
};

export async function pdfCheckout(vin: string, cardToken: string, plan: string): Promise<PdfCheckoutResult> {
  const res = await fetch(`${API_BASE}/api/vin/${encodeURIComponent(vin)}/pdf/checkout`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ card_token: cardToken, plan }),
  });
  if (!res.ok) {
    throw new Error(await readDetail(res));
  }
  return res.json();
}

export async function capturePdf(vin: string, orderId: string): Promise<Blob> {
  const res = await fetch(
    `${API_BASE}/api/vin/${encodeURIComponent(vin)}/pdf/capture?order_id=${encodeURIComponent(orderId)}`,
    { method: "POST" },
  );
  if (!res.ok) {
    throw new Error(await readDetail(res));
  }
  return res.blob();
}

export function downloadBlob(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

export function getQuickBooksAuthUrl(): string {
  return `${API_BASE}/api/quickbooks/auth`;
}

export type PaypalCheckoutResult = {
  approve_url: string;
  order_id: string;
  provider: string;
  plan: string;
  price_usd: number;
};

export async function paypalCheckout(vin: string, plan: string): Promise<PaypalCheckoutResult> {
  const res = await fetch(`${API_BASE}/api/paypal/checkout`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ vin, plan }),
  });
  if (!res.ok) {
    throw new Error(await readDetail(res));
  }
  return res.json();
}

export type PaypalOrderStatus = {
  order_id: string;
  paypal_order_id?: string;
  vin: string;
  plan: string;
  status: "pending" | "paid";
  price_usd: number;
};

export async function paypalCapture(orderId: string): Promise<PaypalOrderStatus> {
  const res = await fetch(`${API_BASE}/api/paypal/capture`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ order_id: orderId }),
  });
  if (!res.ok) {
    throw new Error(await readDetail(res));
  }
  return res.json();
}

export async function paypalOrderStatus(orderId: string): Promise<PaypalOrderStatus> {
  const res = await fetch(`${API_BASE}/api/paypal/order/${encodeURIComponent(orderId)}`);
  if (!res.ok) {
    throw new Error(await readDetail(res));
  }
  return res.json();
}

export async function paypalDownload(orderId: string): Promise<Blob> {
  const deadline = Date.now() + 180000;
  while (Date.now() < deadline) {
    const res = await fetch(`${API_BASE}/api/paypal/report/${encodeURIComponent(orderId)}`);
    if (res.ok) {
      return res.blob();
    }
    if (res.status === 202) {
      await new Promise((r) => setTimeout(r, 2000));
      continue;
    }
    throw new Error(await readDetail(res));
  }
  throw new Error("The report is still being prepared. Please refresh the page and try again.");
}

const VIN_TRANSLITERATION: Record<string, number> = {
  "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
  A: 1, B: 2, C: 3, D: 4, E: 5, F: 6, G: 7, H: 8,
  J: 1, K: 2, L: 3, M: 4, N: 5, P: 7, R: 9,
  S: 2, T: 3, U: 4, V: 5, W: 6, X: 7, Y: 8, Z: 9,
};

const VIN_WEIGHTS = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2];

function checkVinChecksum(vin: string): boolean {
  if (vin.length !== 17) return false;
  let total = 0;
  for (let i = 0; i < 17; i++) {
    const value = VIN_TRANSLITERATION[vin[i]];
    if (value === undefined) return false;
    total += value * VIN_WEIGHTS[i];
  }
  const checkChar = total % 11 === 10 ? "X" : String(total % 11);
  return checkChar === vin[8];
}
