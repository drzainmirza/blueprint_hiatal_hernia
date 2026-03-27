"""
UNCOVR Paragraph Library — v0.1
================================
Paragraphs keyed by section name.

Sections that have {placeholders} are surgeon dropdowns.
The OPTIONS comment above each paragraph lists exactly what
can go in each placeholder — the surgeon picks from these.
"""

PARAGRAPHS = {

    # ── No dropdowns — fully static ───────────────────────────────────────

    "BOILERPLATE_SETUP": (
        "After informed consent was obtained, the patient was brought to the operating room "
        "and positioned on the operating room table in a supine position. The site, location "
        "and nature of surgery were confirmed with the patient. The patient was then administered "
        "general anesthesia in the usual fashion. The patients arms were tucked and legs placed "
        "in a supine position with a foot board. TED hose and SCDs were placed. This surgery was "
        "performed with the dv5 robot.\n\n"
        "A time out procedure was performed.\n\n"
        "The abdomen was then sterile prepped and draped in the standard fashion. lidocaine 1% "
        "was infiltrated in the supraumbilical area and a 8 mm trocar was placed supraumbilically "
        "using a blunt port after the abdomen was insufflated to 15 mm of pressure with a Veress "
        "needle. We placed our 8 mm ports robotic ports in the following fashion two trocars spaced "
        "by a palm breadth on the patients left. One 8mm trocar on the patients right. A RUQ 5mm "
        "trocar for liver retraction with a snake retractor and attached to the bed with a snake "
        "retractor. A vessel sealer, monopolar scissors, cadiere and a fenestrated bipolar instrument."
    ),

    # ── OPTIONS ───────────────────────────────────────────────────────────
    # {sliding_cm}  : "2", "3", "4", "5"
    # {hill_grade}  : "II", "III", "IV"
    # {egd_extra}   : "" (nothing), "Significant erosive esophagitis was noted in the distal esophagus.",
    #                 "LA grade C esophagitis was identified.",
    #                 "Long segment Barrett's disease was noted in the distal esophagus."

    "EGD_INITIAL": (
        "EGD: upper endoscopy revealed the presence of a {sliding_cm} cm sliding component "
        "with a paraesophageal component and a Hill Grade {hill_grade} valve. "
        "The pylorus was also intubated and the proximal duodenum evaluated. {egd_extra}"
    ),

    # ── OPTIONS ───────────────────────────────────────────────────────────
    # {hernia_size} : "small", "moderate sized", "small to moderate sized", "giant"
    # {esoph_length}: "2", "3", "3.5", "4", "5"

    "HIATAL_DISSECTION": (
        "HIATAL DISSECTION:\n"
        "We began our dissection by dividing the pars flaccida preserving the hepatic branch of "
        "the anterior vagus nerve and then mobilizing the esophagus at the right crus, identifying "
        "the junction with the left crus posterior to the esophagus. We then divided the "
        "phrenoesophageal membrane anteriorly and incised the hernia sac of a {hernia_size} "
        "paraesophageal hernia at 12 o'clock. This incision was carried circumferentially around "
        "the hiatal defect freeing up the origin of the sac. Dissection was then continued cephalad "
        "and the sac was dissected off either pleura, the esophagus, the aorta and the middle "
        "mediastinum. The esophagus was then mobilized by dividing its mesentery off the aorta. "
        "{esoph_length} cm of intra-abdominal esophagus was confirmed. Dissection was performed "
        "beyond the left inferior pulmonary vein. The short gastric vessels along the greater "
        "curvature through the splenic hilum up to the level of the left crus were divided. "
        "The esophagus was freed from the left crus. The esophagus was now circumferentially "
        "mobilized at the hiatus."
    ),

    # ── OPTIONS ───────────────────────────────────────────────────────────
    # {effraction_side}: "left", "right", "bilateral"

    "PLEURAL_EFFRACTION": (
        "PLEURAL EFFRACTION:\n"
        "During the hiatal dissection, a {effraction_side} pleurotomy was created. "
        "This pleural defect was expanded to create an open pneumothorax to prevent "
        "a tension pneumothorax."
    ),

    # ── OPTIONS ───────────────────────────────────────────────────────────
    # {vagus_branch}        : "anterior", "posterior", "hepatic branch of the anterior"
    # {vagus_injury_extent} : "partially transected", "fully transected", "stretched but intact"

    "VAGUS_NERVE_TRAUMA": (
        "VAGUS NERVE INJURY:\n"
        "During dissection, an injury to the {vagus_branch} vagus nerve was identified. "
        "The nerve was noted to be {vagus_injury_extent}. "
        "This was documented and the remainder of the procedure was continued."
    ),

    # ── OPTIONS ───────────────────────────────────────────────────────────
    # {collis_neo_length}: "3", "4", "5"

    "COLLIS_GASTROPLASTY": (
        "COLLIS GASTROPLASTY:\n"
        "Due to inadequate intra-abdominal esophageal length, a Collis gastroplasty "
        "was performed for esophageal lengthening. A bougie was placed along the lesser "
        "curvature of the stomach. A wedge-type fundectomy was performed using an "
        "endoscopic linear stapler along the bougie to create a {collis_neo_length} cm "
        "neo-esophagus. The staple line was inspected and confirmed hemostatic. "
        "Adequate intra-abdominal esophageal length was now achieved."
    ),

    # ── OPTIONS ───────────────────────────────────────────────────────────
    # {mesh_size}   : "7x5cm", "7x10cm", "10x15cm"
    # {esoph_length}: "2", "3", "3.5", "4", "5"

    "HERNIA_REPAIR_WITH_MESH": (
        "PARAESOPHAGEAL HERNIA REPAIR:\n"
        "As our protocol to measure tension at closure of the crura on the dv5 using force "
        "feedback instruments. This was performed with a single 0 ethibond suture to the anterior "
        "most portion of the crural defect (abutting the posterior esophagus). Dropping the "
        "pneumoperitoneum to 10mm of Hg closing tension was measured needed to reduce the defect "
        "by one cm. This was then used to approximate both sides of the crura.\n\n"
        "The repair was performed with running 0 permanent vlok suture and run back. "
        "{mesh_size} Phasix ST mesh was placed and sutured in place with a single double pledgeted "
        "0 ethibond horizontal mattress zero ethibond suture. "
        "There was {esoph_length} cm of subdiaphragmatic esophageal length."
    ),

    # ── No dropdowns — fully static ───────────────────────────────────────

    "HERNIA_REPAIR_NO_MESH": (
        "PARAESOPHAGEAL HERNIA REPAIR:\n"
        "As our protocol to measure tension at closure of the crura on the dv5 using force "
        "feedback instruments. This was performed with a single 0 ethibond suture to the anterior "
        "most portion of the crural defect (abutting the posterior esophagus). Dropping the "
        "pneumoperitoneum to 10mm of Hg closing tension was measured needed to reduce the defect "
        "by one cm. This was then used to approximate both sides of the crura.\n\n"
        "The repair was performed with running 0 permanent vlok suture and run back."
    ),

    # ── OPTIONS ───────────────────────────────────────────────────────────
    # {myotomy_gastric_cm}: "1.5", "2", "2.5", "3"

    "HELLERS_MYOTOMY": (
        "HELLER'S MYOTOMY:\n"
        "An anterior esophageal myotomy was performed. The longitudinal and circular "
        "muscle fibers of the distal esophagus were divided for approximately 6 cm on "
        "the esophagus and extended {myotomy_gastric_cm} cm onto the gastric cardia. "
        "The mucosa was confirmed to be intact and bulging appropriately through the "
        "myotomy site. Hemostasis was achieved."
    ),

    # ── No dropdowns — fully static ───────────────────────────────────────

    "TOUPET_FUNDOPLICATION": (
        "TOUPET FUNDOPLICATION:\n"
        "A shoe shine maneuver was performed and the fundus delivered through the retroesophageal "
        "window (posterior fundus). 2 posterior gastropexy sutures were used to approximate this "
        "part of the hiatal defect to the back of the retroesophageal wrap. An internal wrap stitch "
        "was placed in the right and the left on the inside of the posterior and anterior "
        "fundoplication respectively. An apical stitch from the fundus to the left of the esophagus "
        "and the central tendon was placed and this was utilized as a fulcrum from the "
        "fundoplication. The fundoplication was completed with 2 separate columns of 3 stitches "
        "each separated by 1cm to create a 2 cm wrap on the right (posterior fundoplication) and "
        "the left (anterior fundoplication) of the esophagus at and above the level of the GEJ. "
        "The stitches were placed at 9 and 1 o'clock. 2-0 ethibond sutures were used.\n\n"
        "We performed a wrap of the fundus through the retroesophageal window outside both vagus "
        "nerves. This was a 2 cm long wrap using 2-0 Ethibond and incorporating a portion of the "
        "wall of the esophagus."
    ),

    "NISSEN_FUNDOPLICATION": (
        "NISSEN FUNDOPLICATION:\n"
        "A shoe shine maneuver was performed and the fundus delivered through the retroesophageal "
        "window. A 360-degree floppy Nissen fundoplication was created using 2-0 Ethibond sutures "
        "to create a 2 cm wrap incorporating a portion of the wall of the esophagus. The wrap was "
        "confirmed to be tension-free and appropriately positioned around the esophagus."
    ),

    "DOR_FUNDOPLICATION": (
        "DOR FUNDOPLICATION:\n"
        "A Dor fundoplication was fashioned with a total of 6 interrupted 2-0 ethibond "
        "sutures allowing for a 180 anterior fundoplication by using the now freed "
        "fundus. Endoscopically a decent anterior fundoplication was confirmed."
    ),

    # ── No dropdowns — fully static ───────────────────────────────────────

    "PYLOROPLASTY": (
        "PYLOROPLASTY:\n"
        "The pylorus was identified by looking for the prepyloric vein, the branches "
        "of the anterior vagus (crows feet) and palpating the ring of muscle as well "
        "as endoscopically. The monopolar scissors was used to enter the distal antrum. "
        "The division of the wall and the pyloric ring continued in a linear "
        "(longitudinal fashion) until the enterotomy was 5 cm long, equally on the "
        "stomach and pylorus. The pylorus was closed using the Heineke-Mikulicz fashion "
        "using a single 3-0 absorbable vlok suture in a running fashion starting in the "
        "cephalad side (lesser curvature) running inferiorly and then run back for a "
        "Lembert layer. The closure integrity was confirmed by ensuring the tightness "
        "of each bite. The repair was placed underwater and a leak test was performed "
        "with no leak."
    ),

    # ── OPTIONS ───────────────────────────────────────────────────────────
    # {linx_sizer_mm}  : "11", "13", "14"
    # {linx_device_mm} : "14", "16", "17"

    "LINX_IMPLANTATION": (
        "LINX IMPLANTATION:\n"
        "Using the sizer the distal esophagus at the level of the GEJ/LES just above "
        "the GEJ fat pad. We sized the esophagus to be at {linx_sizer_mm}mm (this is "
        "where the sizer \"popped off\") and did this run twice. Therefore a "
        "{linx_device_mm}mm LINX device was opened and placed. Using the standard "
        "technique the LINX was placed around the GEJ and within the posterior vagus "
        "and clasped anteriorly. The LINX was freely (but not excessively) mobile."
    ),

    # ── OPTIONS ───────────────────────────────────────────────────────────
    # {egd_completion_finding}:
    #   "A completion EGD confirmed an excellent subdiaphragmatic fundoplication."
    #   "A completion EGD confirmed a viable distal esophagus and stomach as well as a posterior fundoplication."
    #   "A completion EGD confirmed the presence of a subdiaphragmatic GEJ."

    "EGD_COMPLETION": (
        "The endoscope was removed after confirming the presence of a \"stacked coin\" appearance "
        "to the fundoplication. {egd_completion_finding}"
    ),

    # ── No dropdowns — fully static ───────────────────────────────────────

    "CLOSURE": (
        "The instruments were centralized and removed. The robot was undocked. The liver retractor "
        "was removed. The trocars were removed under direct visualization and the abdomen was "
        "desufflated. Skin was closed using 4-0 monocryl. All instrument and sponge counts were "
        "correct X2.\n\n"
        "I thank you for involving me in this patient's care."
    ),

}