import os, re

BASE = r"C:\Users\Dhruvisha\Desktop\plumbing-site"

# (city-slug, city, state, abbr, blog-slug)
CITIES = [
    ("plumber-phoenix-az",         "Phoenix",       "Arizona",        "AZ", "phoenix"),
    ("plumber-houston-tx",         "Houston",        "Texas",          "TX", "houston"),
    ("plumber-dallas-tx",          "Dallas",         "Texas",          "TX", "dallas"),
    ("plumber-austin-tx",          "Austin",         "Texas",          "TX", "austin"),
    ("plumber-san-antonio-tx",     "San Antonio",    "Texas",          "TX", "san-antonio"),
    ("plumber-fort-worth-tx",      "Fort Worth",     "Texas",          "TX", "fort-worth"),
    ("plumber-charlotte-nc",       "Charlotte",      "North Carolina", "NC", "charlotte"),
    ("plumber-raleigh-nc",         "Raleigh",        "North Carolina", "NC", "raleigh"),
    ("plumber-greensboro-nc",      "Greensboro",     "North Carolina", "NC", "greensboro"),
    ("plumber-nashville-tn",       "Nashville",      "Tennessee",      "TN", "nashville"),
    ("plumber-memphis-tn",         "Memphis",        "Tennessee",      "TN", "memphis"),
    ("plumber-tampa-fl",           "Tampa",          "Florida",        "FL", "tampa"),
    ("plumber-jacksonville-fl",    "Jacksonville",   "Florida",        "FL", "jacksonville"),
    ("plumber-denver-co",          "Denver",         "Colorado",       "CO", "denver"),
    ("plumber-atlanta-ga",         "Atlanta",        "Georgia",        "GA", "atlanta"),
    ("plumber-louisville-ky",      "Louisville",     "Kentucky",       "KY", "louisville"),
    ("plumber-las-vegas-nv",       "Las Vegas",      "Nevada",         "NV", "las-vegas"),
    ("plumber-albuquerque-nm",     "Albuquerque",    "New Mexico",     "NM", "albuquerque"),
    ("plumber-oklahoma-city-ok",   "Oklahoma City",  "Oklahoma",       "OK", "oklahoma-city"),
    ("plumber-portland-or",        "Portland",       "Oregon",         "OR", "portland"),
]

# (folder-prefix, new-title-tpl, new-desc-tpl, new-keywords-tpl)
BLOGS = [
    (
        "how-to-unclog-drain",
        "How to Unclog a Drain in {city}, {abbr} — Step-by-Step Guide",
        "Learn how to unclog a drain in {city}, {abbr} with these expert DIY methods — from boiling water to a drain snake. Plus when to call a licensed {city} plumber.",
        "how to unclog a drain {city_lc}, clogged drain {city_lc}, unclog drain diy {city_lc}, drain cleaning {city_lc}, slow drain fix {city_lc}, plumber {city_lc}",
    ),
    (
        "signs-you-need-a-plumber",
        "7 Signs You Need a Plumber in {city}, {abbr} | Expert Advice",
        "7 warning signs {city} homeowners should never ignore — from slow drains to low water pressure. Know when to call a licensed {city} plumber before damage gets worse.",
        "signs you need a plumber {city_lc}, when to call a plumber {city_lc}, plumbing warning signs {city_lc}, plumbing emergency {city_lc}, plumber near me {city_lc}",
    ),
    (
        "water-heater-repair-or-replace",
        "Water Heater: Repair or Replace? {city}, {abbr} Homeowner's Guide",
        "Should you repair or replace your water heater in {city}, {abbr}? Learn the key factors — age, repair cost, efficiency — with expert advice from licensed {city} plumbers.",
        "water heater repair or replace {city_lc}, water heater cost {city_lc}, water heater lifespan {city_lc}, water heater replacement {city_lc}, plumber {city_lc}",
    ),
    (
        "fix-a-running-toilet",
        "How to Fix a Running Toilet in {city}, {abbr} — Easy DIY Guide",
        "Step-by-step guide to fix a running toilet in {city}, {abbr}. Diagnose flapper, fill valve, and float issues yourself — or call a licensed {city} plumber for fast repair.",
        "fix running toilet {city_lc}, running toilet repair {city_lc}, toilet keeps running {city_lc}, toilet flapper replacement {city_lc}, plumber {city_lc}",
    ),
    (
        "low-water-pressure-causes",
        "Low Water Pressure in {city}, {abbr}: Common Causes & Fixes",
        "Why is your water pressure low in {city}, {abbr}? Discover the 7 most common causes — clogged aerators, pipe leaks, corroded pipes — and get expert {city} plumber solutions.",
        "low water pressure {city_lc}, water pressure problems {city_lc}, causes of low water pressure {city_lc}, water pressure fix {city_lc}, plumber {city_lc}",
    ),
    (
        "plumbing-tips",
        "Plumbing Maintenance Tips for {city}, {abbr} Homeowners | Expert Guide",
        "Expert plumbing maintenance tips for {city}, {abbr} homeowners. Prevent costly repairs with seasonal checks, water heater flushing, leak detection, and more — from licensed {city} plumbers.",
        "plumbing tips {city_lc}, plumbing maintenance {city_lc}, prevent plumbing problems {city_lc}, home plumbing advice {city_lc}, plumber {city_lc}",
    ),
]

# Blog index page (blog/)
BLOG_INDEX = (
    "blog",
    "Plumbing Tips & Guides for {city}, {abbr} Homeowners | PlumbersInUSA.com",
    "Free plumbing tips, DIY guides, and expert advice for {city}, {abbr} homeowners. Drain cleaning, water heater repair, pipe maintenance — from licensed local plumbers.",
    "plumbing tips {city_lc}, plumbing blog {city_lc}, plumbing guides {city_lc}, plumbing advice {city_lc}, plumber near me {city_lc}",
)

def fix_page(path, city, state, abbr, city_lc, title, desc, kw):
    if not os.path.exists(path):
        return 'SKIP'
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Title
    html = re.sub(r'<title>[^<]+</title>', f'<title>{title}</title>', html)

    # Meta description
    html = re.sub(r'<meta name="description" content="[^"]+"',
                  f'<meta name="description" content="{desc}"', html)

    # Keywords
    html = re.sub(r'<meta name="keywords" content="[^"]+"',
                  f'<meta name="keywords" content="{kw}"', html)

    # OG title + description
    html = re.sub(r'<meta property="og:title" content="[^"]+"',
                  f'<meta property="og:title" content="{title}"', html)
    html = re.sub(r'<meta property="og:description" content="[^"]+"',
                  f'<meta property="og:description" content="{desc}"', html)

    # Twitter title + description
    html = re.sub(r'<meta name="twitter:title" content="[^"]+"',
                  f'<meta name="twitter:title" content="{title}"', html)
    html = re.sub(r'<meta name="twitter:description" content="[^"]+"',
                  f'<meta name="twitter:description" content="{desc}"', html)

    # Brand link → PlumbersInUSA.com
    html = re.sub(
        r'<a class="brand" href="https://plumbersinusa\.com/[^"]+" aria-label="[^"]+">Plumbing Repair</a>',
        '<a class="brand" href="https://plumbersinusa.com/" aria-label="PlumbersInUSA.com - Home">PlumbersInUSA.com</a>',
        html
    )

    # Footer first col h4
    html = re.sub(
        r'<h4>Plumbing Repair in ' + re.escape(city) + r', ' + re.escape(abbr) + r'</h4>',
        f'<h4>Plumbing Guides for {city}, {abbr}</h4>',
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

# ── Run ────────────────────────────────────────────────────────────────────────
total = len(CITIES) * (len(BLOGS) + 1)
print(f"Updating {total} blog pages...")
ok = skip = 0

for (cslug, city, state, abbr, blog_slug) in CITIES:
    cl = city.lower().replace(' ', '-')  # for regex, keep original case in templates
    city_lc = city.lower()  # for keywords

    # Blog guide pages
    for (prefix, title_tpl, desc_tpl, kw_tpl) in BLOGS:
        folder = f"{prefix}-{blog_slug}"
        path = os.path.join(BASE, cslug, folder, 'index.html')
        title = title_tpl.format(city=city, state=state, abbr=abbr)
        desc  = desc_tpl.format(city=city, state=state, abbr=abbr)
        kw    = kw_tpl.format(city=city, state=state, abbr=abbr, city_lc=city_lc)
        r = fix_page(path, city, state, abbr, city_lc, title, desc, kw)
        if r == 'SKIP':
            skip += 1
            print(f"  SKIP  {cslug}/{folder}")
        else:
            ok += 1

    # Blog index page
    (_, bi_title_tpl, bi_desc_tpl, bi_kw_tpl) = BLOG_INDEX
    path = os.path.join(BASE, cslug, 'blog', 'index.html')
    title = bi_title_tpl.format(city=city, state=state, abbr=abbr)
    desc  = bi_desc_tpl.format(city=city, state=state, abbr=abbr)
    kw    = bi_kw_tpl.format(city=city, state=state, abbr=abbr, city_lc=city_lc)
    r = fix_page(path, city, state, abbr, city_lc, title, desc, kw)
    if r == 'SKIP':
        skip += 1
        print(f"  SKIP  {cslug}/blog")
    else:
        ok += 1

print(f"Done. OK={ok}  SKIP={skip}")
