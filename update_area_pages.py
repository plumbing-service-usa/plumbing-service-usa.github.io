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

def slug_to_name(slug):
    """plumbing-repair-paradise-valley → Paradise Valley"""
    # Strip 'plumbing-repair-' prefix
    area_slug = slug.replace('plumbing-repair-', '')
    return ' '.join(w.capitalize() for w in area_slug.split('-'))

def fix_page(path, city, state, abbr, title, desc, kw):
    if not os.path.exists(path):
        return 'SKIP'
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    html = re.sub(r'<title>[^<]+</title>', f'<title>{title}</title>', html)
    html = re.sub(r'<meta name="description" content="[^"]+"',
                  f'<meta name="description" content="{desc}"', html)
    html = re.sub(r'<meta name="keywords" content="[^"]+"',
                  f'<meta name="keywords" content="{kw}"', html)
    html = re.sub(r'<meta property="og:title" content="[^"]+"',
                  f'<meta property="og:title" content="{title}"', html)
    html = re.sub(r'<meta property="og:description" content="[^"]+"',
                  f'<meta property="og:description" content="{desc}"', html)
    html = re.sub(r'<meta name="twitter:title" content="[^"]+"',
                  f'<meta name="twitter:title" content="{title}"', html)
    html = re.sub(r'<meta name="twitter:description" content="[^"]+"',
                  f'<meta name="twitter:description" content="{desc}"', html)

    # Brand link
    html = re.sub(
        r'<a class="brand" href="https://plumbersinusa\.com/[^"]+" aria-label="[^"]+">Plumbing Repair</a>',
        '<a class="brand" href="https://plumbersinusa.com/" aria-label="PlumbersInUSA.com - Home">PlumbersInUSA.com</a>',
        html
    )

    # Footer h4
    html = re.sub(
        r'<h4>Plumbing Repair in ' + re.escape(city) + r', ' + re.escape(abbr) + r'</h4>',
        f'<h4>Plumbing Services in {city}, {abbr}</h4>',
        html
    )

    # Footer copyright
    html = re.sub(
        r'&copy; 2026 Plumbing Repair Services in ' + re.escape(city) + r', ' + re.escape(state) + r'\. All rights reserved\. \| Licensed &amp; Insured',
        f'&copy; 2026 PlumbersInUSA.com | Licensed &amp; Insured Plumbers in {city}, {state}',
        html
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return 'OK'

print("Updating area pages...")
ok = skip = 0

for (cslug, city, state, abbr) in CITIES:
    city_path = os.path.join(BASE, cslug)
    city_lc = city.lower()

    # plumbing-repair-{area} pages
    for sub in os.listdir(city_path):
        if not sub.startswith('plumbing-repair-'):
            continue
        area = slug_to_name(sub)
        area_lc = area.lower()
        path = os.path.join(city_path, sub, 'index.html')

        title = f"Licensed Plumbers in {area}, {city} {abbr} | Free Quote"
        desc  = (f"Licensed & insured plumbers serving {area}, {city}, {state}. "
                 f"Emergency plumbing, drain cleaning, water heater repair & more. "
                 f"Same-day service, free written quote. Call now!")
        kw    = (f"plumber {area_lc}, plumbing repair {area_lc}, drain cleaning {area_lc}, "
                 f"plumber near {area_lc}, {city_lc} plumber, plumbing services {area_lc}")

        r = fix_page(path, city, state, abbr, title, desc, kw)
        if r == 'SKIP':
            skip += 1
            print(f"  SKIP  {cslug}/{sub}")
        else:
            ok += 1

    # areas/index.html
    path = os.path.join(city_path, 'areas', 'index.html')
    title = f"Plumbing Service Areas in {city}, {state} | PlumbersInUSA.com"
    desc  = (f"View all neighborhoods and service areas covered by our licensed plumbers in {city}, {state}. "
             f"Emergency plumbing, drain cleaning, water heater repair & more across {abbr}.")
    kw    = (f"plumber {city_lc}, plumbing service areas {city_lc}, neighborhoods {city_lc}, "
             f"plumber near me {city_lc}, {city_lc} plumbing services")

    r = fix_page(path, city, state, abbr, title, desc, kw)
    if r == 'SKIP':
        skip += 1
        print(f"  SKIP  {cslug}/areas")
    else:
        ok += 1

print(f"Done. OK={ok}  SKIP={skip}")
