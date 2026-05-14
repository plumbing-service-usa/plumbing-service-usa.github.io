"""
v2 update — competitor-research-informed FAQ Q4/Q5 replacement.

Research sources:
  Roto-Rooter drain-cleaning: "Drain Cleaning vs Drain Clearing" concept; FAQ "Do you offer emergency drain cleaning?"
  Parker & Sons emergency: "No extra charge nights/weekends/holidays" differentiator
  Roto-Rooter water heater: FAQ "What size water heater is right for my home?" + "How often should I do maintenance?"
  Mr. Rooter sewer line: FAQ "Do I need a permit?" + "How long do sewer pipes last?"
  Reliant + Mr. Rooter leak: FAQ "Will detection disrupt my home?" + "Does insurance cover it?"
  Multiple sources pipe repair: FAQ "What causes pipes to burst?" + "How long does repair take?"

Each FAQ answer is original — competitive questions used as search-query targets only.
"""
import os, re

BASE = r"C:\Users\Dhruvisha\Desktop\plumbing-site"

CITIES = [
    ("plumber-phoenix-az",       "Phoenix",       "Arizona",        "AZ"),
    ("plumber-houston-tx",       "Houston",        "Texas",          "TX"),
    ("plumber-dallas-tx",        "Dallas",         "Texas",          "TX"),
    ("plumber-austin-tx",        "Austin",         "Texas",          "TX"),
    ("plumber-san-antonio-tx",   "San Antonio",    "Texas",          "TX"),
    ("plumber-fort-worth-tx",    "Fort Worth",     "Texas",          "TX"),
    ("plumber-charlotte-nc",     "Charlotte",      "North Carolina", "NC"),
    ("plumber-raleigh-nc",       "Raleigh",        "North Carolina", "NC"),
    ("plumber-greensboro-nc",    "Greensboro",     "North Carolina", "NC"),
    ("plumber-nashville-tn",     "Nashville",      "Tennessee",      "TN"),
    ("plumber-memphis-tn",       "Memphis",        "Tennessee",      "TN"),
    ("plumber-tampa-fl",         "Tampa",          "Florida",        "FL"),
    ("plumber-jacksonville-fl",  "Jacksonville",   "Florida",        "FL"),
    ("plumber-denver-co",        "Denver",         "Colorado",       "CO"),
    ("plumber-atlanta-ga",       "Atlanta",        "Georgia",        "GA"),
    ("plumber-louisville-ky",    "Louisville",     "Kentucky",       "KY"),
    ("plumber-las-vegas-nv",     "Las Vegas",      "Nevada",         "NV"),
    ("plumber-albuquerque-nm",   "Albuquerque",    "New Mexico",     "NM"),
    ("plumber-oklahoma-city-ok", "Oklahoma City",  "Oklahoma",       "OK"),
    ("plumber-portland-or",      "Portland",       "Oregon",         "OR"),
]

# old_q4/old_q5 must match EXACTLY what update_service_pages.py (v1) wrote.
# new_q4/new_q5/new_a4/new_a5 are the competitor-research-informed replacements.
SERVICES = [
    {
        "slug": "drain-cleaning",
        # v1 questions (to find + remove)
        "old_q4_tpl": "Can I use chemical drain cleaners instead of calling a plumber in {city}?",
        "old_q5_tpl": "How often should drains be professionally cleaned in {city}?",
        # v2 questions (competitor-informed — Roto-Rooter H2 "Drain Cleaning vs Drain Clearing" + FAQ "emergency drain cleaning")
        "new_q4_tpl": "What is the difference between drain cleaning and drain clearing in {city}?",
        "new_a4_tpl": ("Drain clearing removes an immediate blockage so water flows again — it's a temporary fix. "
                       "Professional drain cleaning goes further: our hydro-jetting service scours the entire interior "
                       "of the pipe wall with high-pressure water, removing built-up grease, mineral scale, soap residue, "
                       "and root fibers that cause blockages to keep returning. In {city}, full drain cleaning is the "
                       "recommended solution whenever a clog has recurred more than once."),
        "new_q5_tpl": "Do you offer emergency drain cleaning in {city}?",
        "new_a5_tpl": ("Yes — our {city} drain cleaning team is available 24/7, including nights, weekends, and holidays "
                       "at no extra surcharge. Severe drain backups, overflowing fixtures, and main sewer blockages are "
                       "treated as same-day emergencies. A licensed {city} technician will be dispatched to your address "
                       "within 1–2 hours of your call."),
    },
    {
        "slug": "emergency-plumbing",
        "old_q4_tpl": "What counts as a plumbing emergency in {city}?",
        "old_q5_tpl": "Will homeowner's insurance cover emergency plumbing repairs in {city}?",
        # v2 — Parker & Sons "no extra charge nights/weekends" differentiator
        "new_q4_tpl": "Is there an extra charge for emergency plumbing at night or on weekends in {city}?",
        "new_a4_tpl": ("No — we provide 24/7 emergency plumbing in {city} with no additional surcharge for nights, "
                       "weekends, or holidays. You receive the same upfront written quote at 2 AM on a Sunday as you "
                       "would on a weekday morning. Many plumbing companies charge after-hours premiums of 50–100% — "
                       "we don't. Call anytime and a licensed {city} technician will be dispatched immediately."),
        "new_q5_tpl": "What should I do immediately while waiting for the emergency plumber in {city}?",
        "new_a5_tpl": ("While our {city} emergency plumber is en route: (1) Locate and shut off your main water supply "
                       "valve — usually near your water meter or where the main line enters the home — to stop flooding "
                       "immediately. (2) Turn off your water heater to prevent tank damage from running dry. (3) Move "
                       "valuables away from water-affected areas. (4) Document all visible damage with photos for your "
                       "insurance claim. Do not use any drains, toilets, or fixtures until our technician arrives and "
                       "assesses the situation."),
    },
    {
        "slug": "water-heater-repair",
        "old_q4_tpl": "Should I repair or replace my water heater in {city}?",
        "old_q5_tpl": "Is a tankless water heater worth the upgrade in {city}?",
        # v2 — Roto-Rooter FAQ "What size?" + "How often maintenance?"
        "new_q4_tpl": "What size water heater is right for my {city} home?",
        "new_a4_tpl": ("Water heater sizing for {city} homes depends on household size: 1–2 people need a 30–40 gallon "
                       "tank; 3–4 people need 40–50 gallons; 5+ people need 50–80 gallons. For tankless units, sizing is "
                       "based on peak demand in gallons per minute (GPM) at your target temperature rise. Our {city} "
                       "technicians assess your household's actual hot water usage patterns and recommend the right-sized "
                       "unit — not the most expensive one — during your free on-site quote."),
        "new_q5_tpl": "How often should I schedule water heater maintenance in {city}?",
        "new_a5_tpl": ("Annual water heater maintenance in {city} should include: tank flushing to remove sediment buildup, "
                       "anode rod inspection (replace when less than 50% remains), pressure relief valve testing, "
                       "thermostat calibration, and burner inspection on gas units. Consistent maintenance extends water "
                       "heater life by 3–5 years and prevents unexpected cold-water emergencies. Our {city} plumbers "
                       "offer a complete annual water heater maintenance service — ask about pricing when you call."),
    },
    {
        "slug": "pipe-repair",
        "old_q4_tpl": "When should I repipe my {city} home instead of repairing individual pipes?",
        "old_q5_tpl": "What pipe material is best for homes in {city}?",
        # v2 — "What causes pipes to burst?" (high-search-volume query) + "How long does repair take?"
        "new_q4_tpl": "What causes pipes to burst or leak in {city} homes?",
        "new_a4_tpl": ("The most common pipe failure causes in {city} include: thermal stress from extreme temperature "
                       "swings (expansion and contraction of pipe materials), ground movement from expansive soils stressing "
                       "buried pipes and joints, normal wear on pipes over 30–40 years old, water pressure above 80 PSI "
                       "straining fittings, tree root intrusion into exterior water lines, and corrosion in older "
                       "galvanized steel or cast iron systems. Identifying the root cause before repairing is essential — "
                       "our licensed plumbers diagnose the underlying issue so the same pipe doesn't fail again."),
        "new_q5_tpl": "How long does pipe repair take in {city}?",
        "new_a5_tpl": ("Most single-section pipe repairs in {city} are completed same-day, typically in 2–4 hours. "
                       "Emergency burst pipe repairs receive priority dispatch and are resolved the same day in nearly all "
                       "cases — we restore water service as quickly as possible. Full home repiping takes 2–4 days "
                       "depending on house size and pipe material. You receive a detailed written timeline in your free "
                       "quote before any work begins, so you know exactly what to expect."),
    },
    {
        "slug": "leak-detection",
        "old_q4_tpl": "How do I know if I have a hidden water leak in my {city} home?",
        "old_q5_tpl": "How much does professional leak detection cost in {city}?",
        # v2 — Reliant FAQ "Will it disrupt my home?" + Mr. Rooter "Does insurance cover it?"
        "new_q4_tpl": "Will leak detection disrupt my {city} home or require demolition?",
        "new_a4_tpl": ("Professional leak detection in {city} is non-invasive by design. We use acoustic listening "
                       "devices, thermal imaging cameras, electronic pressure testing, and video pipe inspection to "
                       "precisely locate the leak source before any work begins. In most cases, we pinpoint the exact "
                       "leak location without any cutting, digging, or demolition whatsoever. Only the minimal area "
                       "immediately around the confirmed leak requires access for repair — protecting your floors, walls, "
                       "and landscaping from unnecessary damage."),
        "new_q5_tpl": "Does homeowners' insurance cover water leak detection and repair in {city}?",
        "new_a5_tpl": ("Most {city} homeowners' insurance policies cover sudden and accidental water damage — such as "
                       "damage caused by a burst pipe — but typically do not cover the cost of routine leak detection or "
                       "the underlying plumbing repair itself. However, water damage to floors, walls, ceilings, and "
                       "belongings caused by the leak is usually covered. Our team provides detailed written inspection "
                       "reports and complete technical documentation to support your insurance claim. We work with all "
                       "major carriers and can communicate directly with your adjuster if needed."),
    },
    {
        "slug": "sewer-line-repair",
        "old_q4_tpl": "What's the difference between sewer line repair and full replacement in {city}?",
        "old_q5_tpl": "Is trenchless sewer repair available in {city}, and is it worth it?",
        # v2 — Mr. Rooter FAQ "Do I need a permit?" + "How long do pipes last?"
        "new_q4_tpl": "Do I need a permit for sewer line repair or replacement in {city}?",
        "new_a4_tpl": ("Sewer line work involving excavation or significant pipe replacement typically requires a permit "
                       "in {city}, {state}. For minor spot repairs — clearing a root blockage or patching a short section "
                       "— permits are often not required. Our licensed {city} plumbers handle all permit applications, "
                       "scheduling inspections, and code compliance on your behalf. All permitted sewer line work comes "
                       "with a documented inspection record that protects your home's resale value."),
        "new_q5_tpl": "How long do sewer pipes last in {city} homes?",
        "new_a5_tpl": ("Sewer pipe lifespan in {city} depends on material: ABS or PVC plastic lasts 50–80+ years; cast "
                       "iron pipes last 25–100 years depending on soil conditions and water chemistry; clay sewer pipe — "
                       "common in homes built before 1980 — lasts 50–60 years but becomes brittle, cracks easily, and is "
                       "highly susceptible to root intrusion over time. If your {city} home was built before 1980, a "
                       "camera inspection of your sewer line every 5–7 years is the best way to catch deterioration "
                       "before it becomes a costly emergency."),
    },
]

# ── Helpers ────────────────────────────────────────────────────────────────────

def new_faq_html(q, a):
    return f'<div class="faq-item"><div class="faq-q">{q} <span>▼</span></div><div class="faq-a">{a}</div></div>'

def new_faq_schema_block(q, a):
    # Returns the replacement for one schema Question block
    # Escapes double quotes and backslashes in a/q for valid JSON
    q_json = q.replace('\\', '\\\\').replace('"', '\\"')
    a_json = a.replace('\\', '\\\\').replace('"', '\\"')
    return (
        '{\n'
        '      "@type": "Question",\n'
        f'      "name": "{q_json}",\n'
        '      "acceptedAnswer": {\n'
        '        "@type": "Answer",\n'
        f'        "text": "{a_json}"\n'
        '      }\n'
        '    }'
    )

def update(city_slug, city, state, abbr, svc):
    path = os.path.join(BASE, city_slug, svc['slug'], 'index.html')
    if not os.path.exists(path):
        return 'SKIP'

    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    c, st, ab = city, state, abbr

    old_q4 = svc['old_q4_tpl'].format(city=c, state=st, abbr=ab)
    old_q5 = svc['old_q5_tpl'].format(city=c, state=st, abbr=ab)
    new_q4 = svc['new_q4_tpl'].format(city=c, state=st, abbr=ab)
    new_a4 = svc['new_a4_tpl'].format(city=c, state=st, abbr=ab)
    new_q5 = svc['new_q5_tpl'].format(city=c, state=st, abbr=ab)
    new_a5 = svc['new_a5_tpl'].format(city=c, state=st, abbr=ab)

    # ── 1. Replace FAQ Q4 in HTML ──────────────────────────────────────────────
    old_q4_esc = re.escape(old_q4)
    html = re.sub(
        r'<div class="faq-item"><div class="faq-q">' + old_q4_esc + r' <span>▼</span></div><div class="faq-a">[^<]*</div></div>',
        new_faq_html(new_q4, new_a4),
        html
    )

    # ── 2. Replace FAQ Q5 in HTML ──────────────────────────────────────────────
    old_q5_esc = re.escape(old_q5)
    html = re.sub(
        r'<div class="faq-item"><div class="faq-q">' + old_q5_esc + r' <span>▼</span></div><div class="faq-a">[^<]*</div></div>',
        new_faq_html(new_q5, new_a5),
        html
    )

    # ── 3. Replace FAQ Q4 in JSON-LD FAQPage schema ────────────────────────────
    old_q4_json_esc = re.escape(old_q4.replace('"', '\\"'))
    html = re.sub(
        r'\{\s*"@type":\s*"Question",\s*"name":\s*"' + old_q4_json_esc + r'",\s*"acceptedAnswer":\s*\{.*?\}\s*\}',
        new_faq_schema_block(new_q4, new_a4),
        html, flags=re.DOTALL
    )

    # ── 4. Replace FAQ Q5 in JSON-LD FAQPage schema ────────────────────────────
    old_q5_json_esc = re.escape(old_q5.replace('"', '\\"'))
    html = re.sub(
        r'\{\s*"@type":\s*"Question",\s*"name":\s*"' + old_q5_json_esc + r'",\s*"acceptedAnswer":\s*\{.*?\}\s*\}',
        new_faq_schema_block(new_q5, new_a5),
        html, flags=re.DOTALL
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return 'OK'

# ── Run ────────────────────────────────────────────────────────────────────────
print(f"Applying competitor-informed FAQ updates to {len(CITIES) * len(SERVICES)} service pages...")
ok = skip = err = 0
for (cslug, city, state, abbr) in CITIES:
    for svc in SERVICES:
        r = update(cslug, city, state, abbr, svc)
        if r == 'OK':
            ok += 1
        elif r == 'SKIP':
            skip += 1
        else:
            err += 1
            print(f"  ERR  {cslug}/{svc['slug']}")
print(f"Done. OK={ok}  SKIP={skip}  ERR={err}")
