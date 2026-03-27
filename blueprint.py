"""
UNCOVR Blueprint Routing
========================
Takes model predictions + surgeon inputs → assembled operative note.
"""

from paragraph_library import PARAGRAPHS


# ═══════════════════════════════════════════════════════════════════════════
# INPUTS
# ═══════════════════════════════════════════════════════════════════════════

SETUP_CONFIG = {
    "robot_type": "dv5",                # "dv5", "Xi"
    "typical_duration_mins": "90",      # typical operation duration in minutes
}

SURGEON_INPUTS = {
    "sliding_cm":               "4",
    "hill_grade":               "IV",
    "egd_extra":                "",
    "hernia_size":              "moderate sized",
    "esoph_length":             "4",
    "mesh_size":                "7x5cm",
    "collis_neo_length":        "4",
    "myotomy_gastric_cm":       "2",
    "effraction_side":          "left",
    "vagus_branch":             "anterior",
    "vagus_injury_extent":      "stretched but intact",
    "tif_doctor_name":          "",
    "linx_sizer_mm":            "13",
    "linx_device_mm":           "16",
    "complications":            [],
    "modifier_22_reason":       "",
    "modifier_22_extra_mins":   "",
    "egd_completion_finding":   "A completion EGD confirmed an excellent subdiaphragmatic fundoplication.",
}

SURGEON_TOGGLES = {
    "tif_performed": False,
    "modifier_22":   False,
}

MODIFIER_22_REASONS = [
    "the unusual amount of additional work needed to secure the outcome",
    "the additional work needed for the reoperative nature of the surgery",
    "significant adhesive disease requiring extensive lysis of adhesions",
    "morbid obesity complicating the procedure",
    "conversion from laparoscopic to open approach",
    "excessive blood loss requiring additional hemostatic measures",
]


# ═══════════════════════════════════════════════════════════════════════════
# DETECTION
# ═══════════════════════════════════════════════════════════════════════════

THRESHOLD = 0.5

def detected(steps, label):
    return steps.get(label, 0.0) >= THRESHOLD


# ═══════════════════════════════════════════════════════════════════════════
# ROUTING
# ═══════════════════════════════════════════════════════════════════════════

FUNDO_LABELS = [
    "8.3_Fundoplication_Toupet",
    "8.2_Fundoplication_Nissen",
    "8.4_Fundoplication_Dor",
]

VALID_BASE_CODES_FOR_COLLIS = {"43280", "43281", "43282"}


def get_paragraphs(steps, toggles=None, inputs=None):
    """Build ordered list of paragraph keys for the op note."""
    toggles = toggles or {}
    inputs = inputs or {}
    keys = []

    keys.append("BOILERPLATE_SETUP")

    if detected(steps, "1.10_Intraoperative_Endoscopy"):
        keys.append("EGD_INITIAL")

    if detected(steps, "1.5_Lysis_of_Adhesions"):
        keys.append("LYSIS_OF_ADHESIONS")

    if detected(steps, "2.4_Hiatal_&_Oesophageal_Dissection"):
        keys.append("HIATAL_DISSECTION")

    # Model-detected complications
    if detected(steps, "C.1_Pleural_Effraction"):
        keys.append("PLEURAL_EFFRACTION")
    if detected(steps, "C.2_Vagus_Nerve_Trauma"):
        keys.append("VAGUS_NERVE_TRAUMA")

    # Surgeon-indicated complications
    for complication in inputs.get("complications", []):
        if complication in PARAGRAPHS:
            keys.append(complication)

    if detected(steps, "4.1_Collis_Gastroplasty"):
        keys.append("COLLIS_GASTROPLASTY")

    if detected(steps, "5.1_Cruroplasty"):
        if detected(steps, "6.1_Mesh_Placement"):
            keys.append("HERNIA_REPAIR_WITH_MESH")
        else:
            keys.append("HERNIA_REPAIR_NO_MESH")

    if detected(steps, "7.1_Hellers_Myotomy"):
        keys.append("HELLERS_MYOTOMY")

    # Fundoplication — mutually exclusive
    if detected(steps, "8.3_Fundoplication_Toupet"):
        keys.append("TOUPET_FUNDOPLICATION")
    elif detected(steps, "8.2_Fundoplication_Nissen"):
        keys.append("NISSEN_FUNDOPLICATION")
    elif detected(steps, "8.4_Fundoplication_Dor"):
        keys.append("DOR_FUNDOPLICATION")

    if detected(steps, "9.1_Pyloroplasty"):
        keys.append("PYLOROPLASTY")

    if toggles.get("tif_performed", False):
        keys.append("TIF")

    if detected(steps, "12.1_LINX_Reflux_Management_System"):
        keys.append("LINX_IMPLANTATION")

    if detected(steps, "1.10_Intraoperative_Endoscopy"):
        keys.append("EGD_COMPLETION")

    if detected(steps, "11.1_Drain_Placement"):
        keys.append("DRAIN_PLACEMENT")

    # Modifier 22 — must pass the 25% time threshold check
    if toggles.get("modifier_22", False):
        if _modifier_22_qualifies(inputs, SETUP_CONFIG):
            keys.append("MODIFIER_22")

    keys.append("CLOSURE")

    return keys


def _modifier_22_qualifies(inputs, setup):
    """
    Modifier 22 requires:
    1. Extra time > 25% of typical procedure duration
    2. A documented reason (medical necessity)
    3. The extra time on the specific thing is clearly stated
    """
    try:
        extra = float(inputs.get("modifier_22_extra_mins", 0))
        typical = float(setup.get("typical_duration_mins", 0))
    except (ValueError, TypeError):
        return False

    if typical <= 0 or extra <= 0:
        return False

    has_reason = bool(inputs.get("modifier_22_reason", "").strip())
    exceeds_threshold = extra > (typical * 0.25)

    return exceeds_threshold and has_reason


# ═══════════════════════════════════════════════════════════════════════════
# CPT CODES
# ═══════════════════════════════════════════════════════════════════════════
#
# 43280 — Lap fundoplication (standalone, NOT with 43279/43281/43282)
# 43281 — Lap hiatal hernia repair ± fundo, NO mesh
# 43282 — Lap hiatal hernia repair ± fundo, WITH mesh
# 43283 — Collis gastroplasty (ADD-ON, requires 43280/43281/43282)

def get_cpt_codes(steps, toggles=None, inputs=None, setup=None):
    """
    Returns list of dicts: [{"code": "43282", "type": "primary"}, ...]
    Types: "primary", "add-on". Modifier 22 appends "-22" to primary codes.
    """
    toggles = toggles or {}
    inputs = inputs or {}
    setup = setup or {}
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
        codes.append({"code": "43280", "type": "primary"})

    # Add-on: Collis requires a base code
    if detected(steps, "4.1_Collis_Gastroplasty"):
        base_codes = {c["code"] for c in codes}
        if base_codes & VALID_BASE_CODES_FOR_COLLIS:
            codes.append({"code": "43283", "type": "add-on"})

    # Modifier 22 — append "-22" to primary codes if qualified
    if toggles.get("modifier_22", False) and _modifier_22_qualifies(inputs, setup):
        for c in codes:
            if c["type"] == "primary":
                c["code"] = c["code"] + "-22"

    return codes


# ═══════════════════════════════════════════════════════════════════════════
# ASSEMBLE NOTE
# ═══════════════════════════════════════════════════════════════════════════

def assemble_note(keys, inputs, cpt_codes=None, setup=None):
    all_inputs = {}
    if setup:
        all_inputs.update(setup)
    all_inputs.update(inputs)

    paragraphs = []
    for k in keys:
        if k not in PARAGRAPHS:
            continue
        text = PARAGRAPHS[k]
        try:
            text = text.format(**all_inputs)
        except KeyError:
            pass
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


# ═══════════════════════════════════════════════════════════════════════════
# TESTS
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":

    # ── Test 1: Standard case ─────────────────────────────────────────────
    print("TEST 1: Standard hiatal hernia repair with mesh + Toupet")
    print("=" * 60)

    test1_steps = {
        "1.10_Intraoperative_Endoscopy":       0.91,
        "2.4_Hiatal_&_Oesophageal_Dissection": 0.95,
        "5.1_Cruroplasty":                     0.93,
        "6.1_Mesh_Placement":                  0.87,
        "8.3_Fundoplication_Toupet":           0.89,
    }

    keys = get_paragraphs(test1_steps, SURGEON_TOGGLES, SURGEON_INPUTS)
    cpt = get_cpt_codes(test1_steps, SURGEON_TOGGLES, SURGEON_INPUTS, SETUP_CONFIG)
    print("Sections:", keys)
    print("CPT:", cpt)
    print()
    print(assemble_note(keys, SURGEON_INPUTS, cpt, SETUP_CONFIG))

    # ── Test 2: Redo case with modifier 22 ────────────────────────────────
    print("\n" + "=" * 60)
    print("TEST 2: Redo case — TIF, adhesions, drain, splenic injury, mod 22")
    print("=" * 60 + "\n")

    test2_steps = {
        "1.10_Intraoperative_Endoscopy":       0.91,
        "1.5_Lysis_of_Adhesions":              0.88,
        "2.4_Hiatal_&_Oesophageal_Dissection": 0.95,
        "C.1_Pleural_Effraction":              0.80,
        "5.1_Cruroplasty":                     0.93,
        "6.1_Mesh_Placement":                  0.87,
        "11.1_Drain_Placement":                0.90,
    }
    test2_toggles = {"tif_performed": True, "modifier_22": True}
    test2_inputs = dict(SURGEON_INPUTS)
    test2_inputs["complications"] = ["SPLENIC_INJURY"]
    test2_inputs["modifier_22_reason"] = "the additional work needed for the reoperative nature of the surgery"
    test2_inputs["modifier_22_extra_mins"] = "45"

    keys2 = get_paragraphs(test2_steps, test2_toggles, test2_inputs)
    cpt2 = get_cpt_codes(test2_steps, test2_toggles, test2_inputs, SETUP_CONFIG)
    print("Sections:", keys2)
    print("CPT:", cpt2)
    print()
    print(assemble_note(keys2, test2_inputs, cpt2, SETUP_CONFIG))

    # ── Test 3: Modifier 22 rejected — extra time below 25% ──────────────
    print("\n" + "=" * 60)
    print("TEST 3: Modifier 22 toggled ON but only 10 min extra (below 25% of 90)")
    print("=" * 60 + "\n")

    test3_inputs = dict(SURGEON_INPUTS)
    test3_inputs["modifier_22_reason"] = "morbid obesity complicating the procedure"
    test3_inputs["modifier_22_extra_mins"] = "10"
    test3_toggles = {"tif_performed": False, "modifier_22": True}

    keys3 = get_paragraphs(test1_steps, test3_toggles, test3_inputs)
    cpt3 = get_cpt_codes(test1_steps, test3_toggles, test3_inputs, SETUP_CONFIG)
    print("Sections:", keys3)
    print("CPT:", cpt3)
    print("(Modifier 22 should NOT appear — 10 min is not > 25% of 90 min)")
