"""
UNCOVR Blueprint — Pure Logic Spec
====================================
Three input sources:
  MODEL    = auto-detected from surgical video (confidence 0-1, threshold 0.5)
  SURGEON  = per-case dropdown/toggle in the UI
  SETUP    = configured once before app is used
"""


# ═══════════════════════════════════════════════════════════════════════════
# SETUP CONFIG
# ═══════════════════════════════════════════════════════════════════════════

robot_type = "dv5"                      # "dv5", "Xi"
typical_duration_mins = 90
is_teaching_facility = True/False       # determines modifier 82 eligibility


# ═══════════════════════════════════════════════════════════════════════════
# NOTE SECTIONS — in order of appearance
# ═══════════════════════════════════════════════════════════════════════════

# ── PRE-OP DIAGNOSIS (appears before procedure description) ───────────────
# One dropdown per detected procedure category. Surgeon picks diagnosis + ICD-10.
# Post-op diagnosis defaults to "Same" unless surgeon changes it.

detected_procedures = []    # built automatically from MODEL detections below

if MODEL detects any fundoplication OR SURGEON toggles "tif_performed" ON:
    detected_procedures append "FUNDOPLICATION"
    SURGEON picks {fundo_diagnosis} from:
        "GERD without esophagitis [K21.9]"
        "GERD with esophagitis, without bleeding [K21.00]"
        "GERD with esophagitis, with bleeding [K21.01]"
        "Barrett's esophagus without dysplasia [K22.70]"
        "Other" → free text

if MODEL detects "5.1_Cruroplasty":
    detected_procedures append "HIATAL_HERNIA_REPAIR"
    SURGEON picks {hernia_diagnosis} from:
        "Diaphragmatic hernia, no obstruction or gangrene [K44.9]"
        "Dysphagia, unspecified [R13.10]"
        "Dysphagia, pharyngoesophageal phase [R13.14]"
        "Other" → free text

if MODEL detects "7.1_Hellers_Myotomy":
    detected_procedures append "HELLERS_MYOTOMY"
    SURGEON picks {myotomy_diagnosis} from:
        "Achalasia of cardia [K22.0]"
        "Other" → free text

if MODEL detects "12.1_LINX_Reflux_Management_System":
    detected_procedures append "LINX"
    SURGEON picks {linx_diagnosis} from:
        "GERD without esophagitis [K21.9]"
        "GERD with esophagitis, without bleeding [K21.00]"
        "Other" → free text

include PREOP_DIAGNOSIS paragraph         # lists all selected diagnoses + ICD-10 codes
include POSTOP_DIAGNOSIS paragraph        # defaults to "Same"

# ── PROCEDURES PERFORMED (auto-populated from detected procedures) ────────
include PROCEDURES_PERFORMED paragraph    # lists detected procedures as line items

# ── OPERATIVE NOTE BODY ──────────────────────────────────────────────────

Always include BOILERPLATE_SETUP paragraph               # uses {robot_type}

if MODEL detects "1.10_Intraoperative_Endoscopy":
    include EGD_INITIAL paragraph
    # {sliding_cm}:  "2", "3", "4", "5"
    # {hill_grade}:  "II", "III", "IV"
    # {egd_extra}:   "" | "Significant erosive esophagitis..." | "LA grade C..." | "Long segment Barrett's..."

if MODEL detects "1.5_Lysis_of_Adhesions":
    include LYSIS_OF_ADHESIONS paragraph

if MODEL detects "2.4_Hiatal_&_Oesophageal_Dissection":
    include HIATAL_DISSECTION paragraph
    # {hernia_size}:  "small", "moderate sized", "small to moderate sized", "giant"
    # {esoph_length}: "2", "3", "3.5", "4", "5"

if MODEL detects "C.1_Pleural_Effraction":
    include PLEURAL_EFFRACTION paragraph
    # {effraction_side}: "left", "right", "bilateral"

if MODEL detects "C.2_Vagus_Nerve_Trauma":
    include VAGUS_NERVE_TRAUMA paragraph
    # {vagus_branch}:        "anterior", "posterior", "hepatic branch of the anterior"
    # {vagus_injury_extent}: "partially transected", "fully transected", "stretched but intact"

# Surgeon multi-select — zero or more
if SURGEON selects "STOMACH_INJURY":     include STOMACH_INJURY paragraph
if SURGEON selects "SPLENIC_INJURY":     include SPLENIC_INJURY paragraph
if SURGEON selects "ESOPHAGEAL_INJURY":  include ESOPHAGEAL_INJURY paragraph

if MODEL detects "4.1_Collis_Gastroplasty":
    include COLLIS_GASTROPLASTY paragraph
    # {collis_neo_length}: "3", "4", "5"

if MODEL detects "5.1_Cruroplasty":
    if MODEL detects "6.1_Mesh_Placement":
        include HERNIA_REPAIR_WITH_MESH paragraph
        # {mesh_size}: "7x5cm", "7x10cm", "10x15cm"
        # {esoph_length}: shared with dissection
    else:
        include HERNIA_REPAIR_NO_MESH paragraph

if MODEL detects "7.1_Hellers_Myotomy":
    include HELLERS_MYOTOMY paragraph
    # {myotomy_gastric_cm}: "1.5", "2", "2.5", "3"

if MODEL detects "8.3_Fundoplication_Toupet":
    include TOUPET_FUNDOPLICATION paragraph
elif MODEL detects "8.2_Fundoplication_Nissen":
    include NISSEN_FUNDOPLICATION paragraph
elif MODEL detects "8.4_Fundoplication_Dor":
    include DOR_FUNDOPLICATION paragraph

if MODEL detects "9.1_Pyloroplasty":
    include PYLOROPLASTY paragraph

if SURGEON toggles "tif_performed" ON:
    include TIF paragraph
    # {tif_doctor_name}: free text

if MODEL detects "12.1_LINX_Reflux_Management_System":
    include LINX_IMPLANTATION paragraph
    # {linx_sizer_mm}:  "11", "13", "14"
    # {linx_device_mm}: "14", "16", "17"

if MODEL detects "1.10_Intraoperative_Endoscopy":
    include EGD_COMPLETION paragraph
    # {egd_completion_finding}:
    #   "A completion EGD confirmed an excellent subdiaphragmatic fundoplication."
    #   "...viable distal esophagus and stomach as well as a posterior fundoplication."
    #   "...the presence of a subdiaphragmatic GEJ."

if MODEL detects "11.1_Drain_Placement":
    include DRAIN_PLACEMENT paragraph

actual_duration_mins  = SURGEON input (total operation time in minutes)
extra_mins            = actual_duration_mins - typical_duration_mins
threshold             = typical_duration_mins * 0.25

if extra_mins > threshold:
    modifier 22 MAY apply. Surgeon must also provide:

    {modifier_22_step}:   the step/thing that caused the extra time
                          (some detected by MODEL, some written by SURGEON)
    {modifier_22_mins}:   minutes spent on that specific step/thing
    {modifier_22_reason}: medical necessity — why that step/thing was needed
        "reoperative anatomy requiring extensive adhesiolysis"
        "morbid obesity causing significantly impaired visualization"
        "dense inflammatory adhesions from chronic GERD"
        "extensive mediastinal scarring from prior surgery"
        "conversion from laparoscopic to open approach"

    if {modifier_22_reason} is provided AND {modifier_22_mins} is provided:
        include MODIFIER_22 paragraph

if SETUP is_teaching_facility AND SURGEON toggles "no_resident_available" ON:
    include MODIFIER_82_ATTESTATION paragraph
    # {assistant_doctor_name}: free text

Always include CLOSURE paragraph                          # always


# ═══════════════════════════════════════════════════════════════════════════
# CPT CODE LOGIC
# ═══════════════════════════════════════════════════════════════════════════

# Primary CPT codes — mutually exclusive
if MODEL detects "5.1_Cruroplasty":
    if MODEL detects "6.1_Mesh_Placement":
        primary cpt code = 43282                        # hernia repair WITH mesh
    else:
        primary cpt code = 43281                        # hernia repair NO mesh
elif MODEL detects any fundoplication:
    primary cpt code = 43280                            # standalone fundo. NOT with 43279/43281/43282
else:
    primary cpt code = none

# Add-on CPT codes
if MODEL detects "4.1_Collis_Gastroplasty" AND primary cpt code is 43280 or 43281 or 43282:
    add-on cpt code = 43283

# Modifier 22 — appends to primary cpt code only, NOT to add-on cpt codes
if modifier_22_qualifies (see MODIFIER 22 section above):
    primary cpt code = primary cpt code + "-22"         # e.g. 43282 → 43282-22

# Modifier 82 — teaching facility, no qualified resident available
# Primary surgeon bills the normal primary cpt code (with or without -22)
# Assistant surgeon bills the SAME primary cpt code with "-82" appended
if SETUP is_teaching_facility AND SURGEON toggled "no_resident_available" ON:
    assistant cpt code = primary cpt code + "-82"       # e.g. 43282-82
