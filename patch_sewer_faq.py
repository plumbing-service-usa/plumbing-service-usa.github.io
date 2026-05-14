"""Fix sewer-line-repair Q4 duplicate: original Q3 already asks about permits.
Replace Q4 with trenchless question (another high-value query from Mr. Rooter research)."""
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

def faq_html(q, a):
    return f'<div class="faq-item"><div class="faq-q">{q} <span>▼</span></div><div class="faq-a">{a}</div></div>'

def faq_schema_block(q, a):
    q_j = q.replace('"', '\\"')
    a_j = a.replace('"', '\\"')
    return ('{\n'
            '      "@type": "Question",\n'
            f'      "name": "{q_j}",\n'
            '      "acceptedAnswer": {\n'
            '        "@type": "Answer",\n'
            f'        "text": "{a_j}"\n'
            '      }\n'
            '    }')

ok = 0
for (cslug, city, state, abbr) in CITIES:
    path = os.path.join(BASE, cslug, 'sewer-line-repair', 'index.html')
    if not os.path.exists(path):
        continue

    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    old_q = f"Do I need a permit for sewer line repair or replacement in {city}?"
    new_q = f"What is trenchless sewer line repair and is it available in {city}?"
    new_a = (f"Trenchless sewer line repair repairs or replaces your {city} sewer pipe from the inside — without "
             f"digging up your yard, driveway, or landscaping. The two main trenchless methods are: (1) Pipe lining "
             f"(CIPP — Cured-In-Place Pipe), where a resin-coated liner is inserted and cured inside the existing "
             f"pipe to create a smooth new interior; and (2) Pipe bursting, where a new pipe is pulled through the "
             f"old one, simultaneously fracturing and replacing it. Trenchless methods are available throughout {city} "
             f"and typically cost 20–40% less than traditional open-cut excavation when pipe conditions qualify.")

    # HTML replacement
    old_q_esc = re.escape(old_q)
    html = re.sub(
        r'<div class="faq-item"><div class="faq-q">' + old_q_esc + r' <span>▼</span></div><div class="faq-a">[^<]*</div></div>',
        faq_html(new_q, new_a),
        html
    )

    # Schema replacement
    old_q_j_esc = re.escape(old_q.replace('"', '\\"'))
    html = re.sub(
        r'\{\s*"@type":\s*"Question",\s*"name":\s*"' + old_q_j_esc + r'",\s*"acceptedAnswer":\s*\{.*?\}\s*\}',
        faq_schema_block(new_q, new_a),
        html, flags=re.DOTALL
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    ok += 1

print(f"Patched {ok} sewer-line-repair pages.")
