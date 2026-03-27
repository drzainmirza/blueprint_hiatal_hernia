"""
UNCOVR Blueprint Routing — v0.1
================================
Takes model predictions + surgeon dropdown selections,
returns an assembled operative note.
"""

from paragraph_library import PARAGRAPHS


# ── STEP 1: Paste model outputs here ──────────────────────────────────────
#
# The model watches the surgical video and outputs a confidence score (0.0–1.0)
# for each step it detected. Paste that output dict here.
#
# Example:
#   MODEL_OUTPUT_STEPS = {
#       "1.10_Intraoperative_Endoscopy":       0.91,
#       "2.4_Hiatal_&_Oesophageal_Dissection": 0.95,
#       "5.1_Cruroplasty":                     0.93,
#       "6.1_Mesh_Placement":                  0.87,
#       "8.3_Fundoplication_Toupet":           0.89,
#   }

MODEL_OUTPUT_STEPS = {
    # paste model output here
}


# ── STEP 2: Surgeon dropdown selections ───────────────────────────────────
#
# These are the values the surgeon picks from dropdowns in the UI.
# Each key matches a {placeholder} in the paragraph library.
# Options for each are listed in the paragraph_library.py comments.

SURGEON_INPUTS = {

    # EGD_INITIAL dropdowns
    "sliding_cm":   "4",        # options: "2", "3", "4", "5"
    "hill_grade":   "IV",       # options: "II", "III", "IV"
    "egd_extra":    "",         # options: "" / "Significant erosive esophagitis was noted in the distal esophagus."
                                #          "LA grade C esophagitis was identified."
                                #          "Long segment Barrett's disease was noted in the distal esophagus."

    # HIATAL_DISSECTION dropdowns
    "hernia_size":  "moderate sized",   # options: "small" / "moderate sized" / "small to moderate sized" / "giant"
    "esoph_length": "4",                # options: "2", "3", "3.5", "4", "5"

    # HERNIA_REPAIR_WITH_MESH dropdowns
    "mesh_size":    "7x5cm",    # options: "7x5cm", "7x10cm", "10x15cm"
    # note: esoph_length above is shared with hiatal dissection

    # COLLIS_GASTROPLASTY dropdown
    "collis_neo_length": "4",              # options: "3", "4", "5"

    # HELLERS_MYOTOMY dropdown
    "myotomy_gastric_cm": "2",             # options: "1.5", "2", "2.5", "3"

    # PLEURAL_EFFRACTION dropdown
    "effraction_side": "left",             # options: "left", "right", "bilateral"

    # VAGUS_NERVE_TRAUMA dropdowns
    "vagus_branch": "anterior",            # options: "anterior", "posterior",
                                           #          "hepatic branch of the anterior"
    "vagus_injury_extent": "stretched but intact",
                                           # options: "partially transected",
                                           #          "fully transected",
                                           #          "stretched but intact"

    # EGD_COMPLETION dropdown
    "egd_completion_finding": "A completion EGD confirmed an excellent subdiaphragmatic fundoplication.",
    # options:
    #   "A completion EGD confirmed an excellent subdiaphragmatic fundoplication."
    #   "A completion EGD confirmed a viable distal esophagus and stomach as well as a posterior fundoplication."
    #   "A completion EGD confirmed the presence of a subdiaphragmatic GEJ."
}


# ── Confidence threshold ───────────────────────────────────────────────────
#
# detected() answers: "did the model see this step?"
#
# It looks up the label in MODEL_OUTPUT_STEPS and checks if the confidence
# is at or above THRESHOLD (0.5). If the label isn't in the dict at all,
# it defaults to 0.0 (not detected).
#
# Example:
#   detected(steps, "6.1_Mesh_Placement")
#   → looks up "6.1_Mesh_Placement" → finds 0.87 → 0.87 >= 0.5 → True  (mesh was placed)
#
#   detected(steps, "8.2_Fundoplication_Nissen")
#   → label not in dict → defaults to 0.0 → 0.0 >= 0.5 → False  (Nissen not performed)

THRESHOLD = 0.5

def detected(steps, label):
    return steps.get(label, 0.0) >= THRESHOLD


# ── STEP 3: Routing logic ──────────────────────────────────────────────────

def get_paragraphs(steps):
    keys = []

    keys.append("BOILERPLATE_SETUP")

    if detected(steps, "1.10_Intraoperative_Endoscopy"):
        keys.append("EGD_INITIAL")

    if detected(steps, "2.4_Hiatal_&_Oesophageal_Dissection"):
        keys.append("HIATAL_DISSECTION")

    # Complications during dissection
    if detected(steps, "C.1_Pleural_Effraction"):
        keys.append("PLEURAL_EFFRACTION")
    if detected(steps, "C.2_Vagus_Nerve_Trauma"):
        keys.append("VAGUS_NERVE_TRAUMA")

    # Esophageal lengthening (before crural closure)
    if detected(steps, "4.1_Collis_Gastroplasty"):
        keys.append("COLLIS_GASTROPLASTY")

    if detected(steps, "5.1_Cruroplasty"):
        if detected(steps, "6.1_Mesh_Placement"):
            keys.append("HERNIA_REPAIR_WITH_MESH")
        else:
            keys.append("HERNIA_REPAIR_NO_MESH")

    # Myotomy before fundoplication
    if detected(steps, "7.1_Hellers_Myotomy"):
        keys.append("HELLERS_MYOTOMY")

    if detected(steps, "8.3_Fundoplication_Toupet"):
        keys.append("TOUPET_FUNDOPLICATION")
    elif detected(steps, "8.2_Fundoplication_Nissen"):
        keys.append("NISSEN_FUNDOPLICATION")
    elif detected(steps, "8.4_Fundoplication_Dor"):
        keys.append("DOR_FUNDOPLICATION")

    # Gastric drainage after fundoplication
    if detected(steps, "9.1_Pyloroplasty"):
        keys.append("PYLOROPLASTY")

    if detected(steps, "12.1_LINX_Reflux_Management_System"):
        keys.append("LINX_IMPLANTATION")

    if detected(steps, "1.10_Intraoperative_Endoscopy"):
        keys.append("EGD_COMPLETION")

    keys.append("CLOSURE")

    return keys


# ── STEP 4: CPT codes ─────────────────────────────────────────────────────
#
# 43280 — Laparoscopic fundoplication (standalone, NO hernia repair)
#          Do NOT use with 43279, 43281, or 43282.
# 43281 — Laparoscopic hiatal hernia repair ± fundoplication, NO mesh
# 43282 — Laparoscopic hiatal hernia repair ± fundoplication, WITH mesh
# 43283 — Collis gastroplasty (ADD-ON code, must accompany 43280/43281/43282)

FUNDO_LABELS = [
    "8.3_Fundoplication_Toupet",
    "8.2_Fundoplication_Nissen",
    "8.4_Fundoplication_Dor",
]

VALID_BASE_CODES_FOR_COLLIS = {"43280", "43281", "43282"}

def get_cpt_codes(steps):
    """
    Returns a list of dicts: [{"code": "43282", "type": "primary"}, ...]
    type is either "primary" or "add-on".
    """
    codes = []

    has_cruroplasty = detected(steps, "5.1_Cruroplasty")
    has_fundo = any(detected(steps, label) for label in FUNDO_LABELS)

    # Base codes — mutually exclusive
    if has_cruroplasty:
        if detected(steps, "6.1_Mesh_Placement"):
            codes.append({"code": "43282", "type": "primary"})
        else:
            codes.append({"code": "43281", "type": "primary"})
    elif has_fundo:
        # Fundoplication without hernia repair → 43280
        codes.append({"code": "43280", "type": "primary"})

    # Add-on codes
    if detected(steps, "4.1_Collis_Gastroplasty"):
        base_codes = {c["code"] for c in codes}
        if base_codes & VALID_BASE_CODES_FOR_COLLIS: # essentially IF the valid codes are present in this case THEN do the below
            codes.append({"code": "43283", "type": "add-on"})

    return codes


# ── STEP 5: Assemble note ──────────────────────────────────────────────────

def assemble_note(keys, inputs, cpt_codes=None):
    paragraphs = []
    for k in keys:
        if k not in PARAGRAPHS:
            continue
        text = PARAGRAPHS[k]
        # Fill in any placeholders with surgeon dropdown selections
        try:
            text = text.format(**inputs)
        except KeyError:
            pass  # if a placeholder has no matching input, leave it as-is
        paragraphs.append(text)

    note = "\n\n".join(paragraphs)

    if cpt_codes:
        primary = [c["code"] for c in cpt_codes if c["type"] == "primary"]
        addons  = [c["code"] for c in cpt_codes if c["type"] == "add-on"]
        lines = []
        if primary:
            lines.append("CPT CODES: " + ", ".join(primary))
        if addons:
            lines.append("ADD-ON CODES: " + ", ".join(addons))
        note += "\n\n" + "\n".join(lines)

    return note


# ── Quick test ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    MODEL_OUTPUT_STEPS = {
        "1.10_Intraoperative_Endoscopy":       0.91,
        "2.4_Hiatal_&_Oesophageal_Dissection": 0.95,
        "5.1_Cruroplasty":                     0.93,
        "6.1_Mesh_Placement":                  0.87,
        "8.3_Fundoplication_Toupet":           0.89,
    }

    keys = get_paragraphs(MODEL_OUTPUT_STEPS)
    cpt_codes = get_cpt_codes(MODEL_OUTPUT_STEPS)
    print("Sections selected:", keys)
    print("CPT codes:", cpt_codes)
    print()
    print(assemble_note(keys, SURGEON_INPUTS, cpt_codes))
