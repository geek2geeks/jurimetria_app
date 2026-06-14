import os
import random
import json
import pdfplumber
from pathlib import Path

source_dir = Path(os.getenv("PDF_SOURCE_DIR", "data/raw"))
courts = ["STJ", "STA", "TRL", "TRP", "TRC", "TRE", "TRG"]

selected_pdfs = []
court_samples = {c: [] for c in courts}

# Gather sample pool
print("Scanning PDFs...")
all_pdfs = list(source_dir.rglob("*.pdf"))

for pdf in all_pdfs:
    try:
        court = pdf.relative_to(source_dir).parts[0]
        if court in court_samples and len(court_samples[court]) < 50:
            court_samples[court].append(pdf)
    except (ValueError, IndexError):
        pass

# Select criteria
selected = []
for c, files in court_samples.items():
    if files:
        selected.extend(random.sample(files, min(2, len(files))))

# Try to find specific years
older = [p for p in all_pdfs if "2009" in p.name or "2008" in p.name]
if older: selected.append(older[0])

recent = [p for p in all_pdfs if "2024" in p.name or "2025" in p.name]
if recent: selected.append(recent[0])

# Just take a subset of ~15 to inspect
selected = list(set(selected))[:15]

results = []

for path in selected:
    res = {
        "path": str(path),
        "court": path.relative_to(source_dir).parts[0],
        "year_in_filename": "Unknown",
        "pages": 0,
        "has_ecli": False,
        "has_url": False,
        "has_relator": False,
        "has_n_doc": False,
        "has_data_acordao": False,
        "has_meio": False,
        "has_decisao": False,
        "has_descritores": False,
        "has_sumario": False,
        "has_decisao_integral": False,
        "has_iii_decisao": False,
        "has_tcpdf": False,
        "has_footer_page": False,
        "has_footer_rua": False,
        "has_footer_email": False
    }

    # Simple year guess from filename e.g. ECLI_PT_STJ_2015_...
    parts = path.name.split('_')
    for p in parts:
        if p.isdigit() and len(p) == 4:
            res["year_in_filename"] = p
            break

    try:
        with pdfplumber.open(path) as pdf:
            res["pages"] = len(pdf.pages)
            if res["pages"] > 0:
                page1 = pdf.pages[0].extract_text() or ""
                p1_lower = page1.lower()
                res["has_ecli"] = "ecli:pt:" in p1_lower
                res["has_url"] = "http" in p1_lower and "csm.org.pt" in p1_lower or "jurisprudencia.csm.org.pt" in p1_lower

                res["has_relator"] = "relator" in p1_lower
                res["has_n_doc"] = "nº do documento" in p1_lower or "nº convencional" in p1_lower
                res["has_data_acordao"] = "data do acórdão" in p1_lower
                res["has_meio"] = "meio processual" in p1_lower
                res["has_decisao"] = "decisão:" in p1_lower or "\ndecisão" in p1_lower
                res["has_descritores"] = "descritores" in p1_lower

                # Check all pages for some global labels
                full_text = ""
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text() or ""
                    full_text += text + "\n"
                    t_lower = text.lower()
                    if "sumário:" in t_lower: res["has_sumario"] = True
                    if "decisão integral:" in t_lower: res["has_decisao_integral"] = True
                    if "powered by tcpdf" in t_lower: res["has_tcpdf"] = True
                    if "rua duque de palmela" in t_lower: res["has_footer_rua"] = True
                    if "csm@csm.org.pt" in t_lower: res["has_footer_email"] = True
                    if "página" in t_lower and "/" in t_lower: res["has_footer_page"] = True

                last_page = pdf.pages[-1].extract_text() or ""
                res["has_iii_decisao"] = "iii - decisão" in last_page.lower() or "iii – decisão" in last_page.lower() or "decisão" in last_page.lower()

    except Exception as e:
        res["error"] = str(e)

    results.append(res)

output_path = Path(os.getenv("PDF_INSPECTION_OUTPUT", "docs/pdf_structure_report_data.json"))
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"Inspection complete. Saved to {output_path}")
