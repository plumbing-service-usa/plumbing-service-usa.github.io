"""
create_new_blogs.py
Generate 6 new blog post types for all 20 cities (120 new pages).
Inspired by competitor topic research — all content is original.

New blog types:
  1. garbage-disposal-repair-{slug}
  2. slab-leak-detection-{slug}
  3. diy-vs-professional-plumbing-{slug}
  4. spring-plumbing-checklist-{slug}
  5. holiday-plumbing-tips-{slug}
  6. copper-vs-pex-pipes-{slug}

Also updates each city's blog/index.html to include the 6 new article cards.
"""
import os, re

BASE = r"C:\Users\Dhruvisha\Desktop\plumbing-site"

CITIES = [
    ("plumber-phoenix-az",       "Phoenix",       "Arizona",        "AZ", "phoenix"),
    ("plumber-houston-tx",       "Houston",        "Texas",          "TX", "houston"),
    ("plumber-dallas-tx",        "Dallas",         "Texas",          "TX", "dallas"),
    ("plumber-austin-tx",        "Austin",         "Texas",          "TX", "austin"),
    ("plumber-san-antonio-tx",   "San Antonio",    "Texas",          "TX", "san-antonio"),
    ("plumber-fort-worth-tx",    "Fort Worth",     "Texas",          "TX", "fort-worth"),
    ("plumber-charlotte-nc",     "Charlotte",      "North Carolina", "NC", "charlotte"),
    ("plumber-raleigh-nc",       "Raleigh",        "North Carolina", "NC", "raleigh"),
    ("plumber-greensboro-nc",    "Greensboro",     "North Carolina", "NC", "greensboro"),
    ("plumber-nashville-tn",     "Nashville",      "Tennessee",      "TN", "nashville"),
    ("plumber-memphis-tn",       "Memphis",        "Tennessee",      "TN", "memphis"),
    ("plumber-tampa-fl",         "Tampa",          "Florida",        "FL", "tampa"),
    ("plumber-jacksonville-fl",  "Jacksonville",   "Florida",        "FL", "jacksonville"),
    ("plumber-denver-co",        "Denver",         "Colorado",       "CO", "denver"),
    ("plumber-atlanta-ga",       "Atlanta",        "Georgia",        "GA", "atlanta"),
    ("plumber-louisville-ky",    "Louisville",     "Kentucky",       "KY", "louisville"),
    ("plumber-las-vegas-nv",     "Las Vegas",      "Nevada",         "NV", "las-vegas"),
    ("plumber-albuquerque-nm",   "Albuquerque",    "New Mexico",     "NM", "albuquerque"),
    ("plumber-oklahoma-city-ok", "Oklahoma City",  "Oklahoma",       "OK", "oklahoma-city"),
    ("plumber-portland-or",      "Portland",       "Oregon",         "OR", "portland"),
]

CSS = """*{box-sizing:border-box;margin:0;padding:0}
:root{--primary:#1B4F8A;--secondary:#E84C1E;--dark:#0f172a;--light:#f1f5f9;--text:#1e293b}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:var(--text);line-height:1.7}
.skip-nav{position:absolute;left:-9999px;top:0;background:var(--primary);color:#fff;padding:8px 16px;z-index:9999;border-radius:0 0 4px 0}
.skip-nav:focus{left:0}
.site-header{background:var(--primary);padding:0 20px;position:sticky;top:0;z-index:100;box-shadow:0 2px 8px rgba(0,0,0,.2)}
.header-inner{max-width:1100px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;height:64px}
.brand{color:#fff;font-size:1.15em;font-weight:700;text-decoration:none}
.nav-links{display:flex;list-style:none;gap:16px;align-items:center;margin:0;padding:0}
.header-phone-link{background:var(--secondary);color:#fff!important;padding:7px 14px;border-radius:6px;font-weight:700;font-size:.9em;text-decoration:none}
.hero{background:linear-gradient(135deg,#1B4F8A 0%,#0d3060 100%);color:#fff;padding:70px 20px 60px;text-align:center}
.hero-inner{max-width:800px;margin:0 auto}
.hero h1{font-size:2.4em;font-weight:800;margin-bottom:16px;line-height:1.2}
.hero-sub{font-size:1.15em;opacity:.9;margin-bottom:24px}
.hero-cta{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}
.btn-call{background:var(--secondary);color:#fff;padding:14px 28px;border-radius:8px;font-size:1.05em;font-weight:700;text-decoration:none;display:inline-block;box-shadow:0 4px 14px rgba(0,0,0,.2)}
.cta-banner .btn-call{background:#fff;color:var(--secondary);box-shadow:0 4px 20px rgba(0,0,0,.25)}
.btn-outline{background:transparent;color:#fff;border:2px solid rgba(255,255,255,.7);padding:13px 26px;border-radius:8px;font-size:1.05em;font-weight:600;text-decoration:none}
section{padding:60px 20px}
.section-inner{max-width:1100px;margin:0 auto}
.section-inner h2{font-size:1.9em;font-weight:800;color:var(--dark);margin-bottom:10px}
.section-sub{color:#64748b;font-size:1.05em;margin-bottom:32px}
.bg-light{background:var(--light)}
.cta-banner{background:linear-gradient(135deg,var(--secondary),#c73d14);color:#fff;text-align:center;padding:60px 20px}
.cta-banner h2{font-size:2em;font-weight:800;margin-bottom:12px}
.cta-phone-big{display:block;font-size:1.8em;font-weight:800;margin:16px 0}
.faq-list{max-width:800px}
.faq-item{border:1px solid #e2e8f0;border-radius:10px;margin-bottom:12px;overflow:hidden}
.faq-q{padding:18px 20px;font-weight:700;cursor:pointer;display:flex;justify-content:space-between;background:#fff}
.faq-a{padding:16px 20px;background:var(--light);font-size:.97em;line-height:1.7}
.breadcrumb{font-size:.88em;color:#64748b;margin-bottom:20px}
.breadcrumb a{color:var(--primary);text-decoration:none}
.sticky-cta{position:fixed;bottom:0;left:0;right:0;background:var(--secondary);z-index:200;display:flex;justify-content:center}
.sticky-cta a{color:#fff;padding:14px 24px;font-weight:700;text-decoration:none;font-size:1em;width:100%;text-align:center}
footer{background:var(--dark);color:#c9d1e0;padding:40px 20px 20px}
.footer-inner{max-width:1100px;margin:0 auto}
.footer-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:28px;margin-bottom:28px}
.footer-col h4{color:#fff;font-size:1em;margin-bottom:12px}
.footer-col ul{list-style:none}
.footer-col li{margin-bottom:7px;font-size:.92em}
.footer-col a{color:#94a3b8;text-decoration:none}
.footer-bottom{border-top:1px solid #2d3748;padding-top:16px;text-align:center;font-size:.84em;color:#64748b}
@media(max-width:768px){
  .hamburger-call{display:inline-block!important}
  .nav-links{display:none;position:absolute;top:56px;left:0;right:0;background:var(--primary);flex-direction:column;gap:0;padding:8px 0;box-shadow:0 4px 12px rgba(0,0,0,.3);z-index:99}
  .nav-links.open{display:flex}
  .nav-links li{border-bottom:1px solid rgba(255,255,255,.1)}
  .nav-links li a{display:block;padding:12px 20px;font-size:1em!important}
  .nav-links .header-phone-link{margin:8px 16px;display:block;text-align:center}
  .hamburger{display:flex;flex-direction:column;gap:5px;cursor:pointer;background:none;border:none;padding:8px;margin-left:8px}
  .hamburger span{display:block;width:24px;height:2px;background:#fff;border-radius:2px;transition:.3s}
  .hamburger.open span:nth-child(1){transform:translateY(7px) rotate(45deg)}
  .hamburger.open span:nth-child(2){opacity:0}
  .hamburger.open span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
  .header-inner{height:56px;position:relative}
  .brand{font-size:.92em;max-width:160px;line-height:1.3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .desktop-call{display:none}
  .hero{padding:44px 16px 36px}
  .hero h1{font-size:1.75em}
  .hero-sub{font-size:1em}
  .hero-cta{flex-direction:column;align-items:center}
  .btn-call,.btn-outline{width:100%;max-width:320px;text-align:center;padding:13px 20px}
  .section-inner h2{font-size:1.45em}
  .footer-grid{grid-template-columns:1fr 1fr}
  .cta-banner{padding:40px 16px}
  .cta-banner h2{font-size:1.5em}
  .cta-phone-big{font-size:1.4em}
  section{padding:44px 16px}
  .faq-list{max-width:100%}
}
@media(max-width:480px){
  .hero h1{font-size:1.5em}
  .section-inner h2{font-size:1.3em}
  .footer-grid{grid-template-columns:1fr}
  .footer-col{padding-bottom:16px;border-bottom:1px solid #2d3748}
  .footer-col:last-child{border-bottom:none}
  .cta-banner h2{font-size:1.25em}
  .cta-phone-big{font-size:1.2em}
  .sticky-cta a{font-size:.9em;padding:12px 16px}
  section{padding:36px 14px}
}
@media(min-width:769px){.hamburger{display:none}.nav-links{display:flex!important}}"""

# ── Blog type definitions ─────────────────────────────────────────────────────

def get_blogs(city, state, abbr, city_lc):
    c, st, ab, cl = city, state, abbr, city_lc
    return [
        # ── 1. Garbage Disposal Repair ─────────────────────────────────────────
        {
            "slug_prefix": "garbage-disposal-repair",
            "title": f"Garbage Disposal Not Working in {c}? Common Problems & Fixes",
            "desc": f"Garbage disposal not working in {c}, {ab}? Learn the most common problems — humming, leaking, won't turn on — plus step-by-step fixes and when to call a licensed {c} plumber.",
            "kw": f"garbage disposal repair {cl}, garbage disposal not working {cl}, garbage disposal problems {cl}, garbage disposal replacement {cl}, plumber {cl}",
            "h1": f"Garbage Disposal Not Working in {c}? Here's What to Do",
            "hero_sub": f"Troubleshooting guide from licensed plumbing repair professionals serving {c}, {st}",
            "intro": f"Garbage disposals are one of the hardest-working appliances in {c} kitchens. When your unit stops working, jams, leaks, or makes unusual noises, most problems can be diagnosed and fixed without an expensive service call. This guide covers every common garbage disposal problem {c} homeowners face and exactly what to do about each one.",
            "label": "Garbage Disposal Repair Guide",
            "sections": [
                ("🔇 Garbage Disposal Is Humming but Not Spinning",
                 f"A humming disposal means the motor is getting power but the grinding plate is jammed. Turn off power at the circuit breaker. Look under the unit for the hex key socket (usually 1/4\") — insert an Allen wrench and work it back and forth to free the jam. Remove the obstruction through the sink opening (never reach in while powered). Press the red reset button on the bottom of the unit, restore power, and test. This resolves most disposal jams in {c} homes in under 10 minutes."),
                ("🔴 Garbage Disposal Won't Turn On at All",
                 f"If pressing the switch produces no response whatsoever: (1) Press the red reset button on the bottom of the unit — it trips automatically when the motor overheats. (2) Check that the outlet under the sink has power by plugging in another device. (3) Check your circuit breaker panel for a tripped breaker. (4) If the unit is more than 10 years old and still won't run after reset, the motor has failed. Most {c} homeowners find a reset resolves the problem. If not, our team provides same-day disposal replacement with an upfront written quote."),
                ("💧 Garbage Disposal Is Leaking",
                 f"Disposal leaks occur in three places — each with a different fix: (1) Top of unit at the sink flange: worn plumber's putty seal. Tighten the three mounting bolts or reseal with fresh putty. (2) Side of unit at the dishwasher drain hose: tighten the hose clamp or replace the hose. (3) Bottom of the unit: internal seal failure — the unit must be replaced, this cannot be repaired. Bottom leaks are common in {c} disposals over 8 years old. Call our {c} plumbing team for a same-day replacement."),
                ("🚫 What Never Goes in a Garbage Disposal",
                 f"The most common cause of disposal failure in {c} homes is putting the wrong items in the unit. Never put in: grease, oil, or fat (solidifies in pipes), fibrous vegetables like celery or artichokes (tangle around grinder), starchy foods like potato peels or pasta (form thick paste), eggshells, fruit pits, bones, or any non-food items. Always run cold water before, during, and 30 seconds after running the disposal — this flushes debris through the drain and protects the unit's bearings."),
                ("🔧 When to Call a Licensed Plumber in {city}",
                 f"Call our {c} plumbing team immediately when: the disposal leaks from the bottom (unrepairable seal failure), the reset button trips repeatedly on the same day (motor overheating), grinding sounds continue after you've cleared all visible jams, the unit is over 12 years old and problems keep recurring, or water drains slowly even with the disposal running (a separate drain clog). We provide same-day garbage disposal repair and replacement throughout {c} with a free written quote before work begins."),
            ],
            "faqs": [
                (f"Why is my garbage disposal humming but not spinning in {c}?",
                 f"A humming disposal that won't spin has a jammed grinding plate. Turn off power at the circuit breaker, insert a 1/4\" Allen wrench into the socket on the bottom of the unit, and work it back and forth to free the jam. Remove debris through the drain opening (power must be off), press the red reset button on the bottom of the unit, restore power, and test. If the problem persists, call a licensed {c} plumber — the motor or grinding assembly may need replacement."),
                ("What should never go in a garbage disposal?",
                 f"Never put grease or cooking oil (clogs drain pipes), fibrous vegetables like celery or artichoke leaves (wrap around grinder components), starchy foods like potato peels, rice, or pasta (expand and form paste), eggshells (inner membrane wraps around impellers), fruit pits, bones, or non-food items in a garbage disposal. Run cold water before, during, and 30 seconds after each use to flush the drain line. This prevents the buildup issues that commonly affect {c} disposal drain lines."),
                (f"How long does a garbage disposal last in {c} homes?",
                 f"Most garbage disposals in {c} homes last 8–15 years with proper use. Signs it's time for replacement: the unit requires frequent resets, it leaks from the bottom (internal seal failure), it makes loud grinding or metal-on-metal noises even after clearing jams, or the motor only hums without spinning despite clearing the jam and pressing reset. If your disposal is over 10 years old and experiencing repeated problems, replacement is more cost-effective than continued repairs."),
                (f"Can I replace my garbage disposal myself in {c}?",
                 f"A like-for-like garbage disposal swap is a manageable DIY project if you're comfortable working under a sink — disconnect the drain connections and dishwasher hose, unmount the old unit, and mount the new one on the existing flange. However, if the installation requires changes to drain piping, a new electrical outlet, or a different mounting size, call a licensed {c} plumber. Improper drain connections cause leaks and allow sewer gas into your home — a risk not worth taking to save a service call."),
            ],
        },
        # ── 2. Slab Leak Detection ─────────────────────────────────────────────
        {
            "slug_prefix": "slab-leak-detection",
            "title": f"Slab Leaks in {c}: Warning Signs, Causes & Repair Guide",
            "desc": f"What is a slab leak in {c}, {ab}? Learn the 7 warning signs, what causes slab leaks in {c} homes, professional detection methods, and repair options from licensed {c} plumbers.",
            "kw": f"slab leak {cl}, slab leak detection {cl}, slab leak repair {cl}, slab leak signs {cl}, plumber {cl}",
            "h1": f"Slab Leaks in {c}: Warning Signs, Causes & What to Do",
            "hero_sub": f"Expert slab leak guide from licensed plumbing repair professionals serving {c}, {st}",
            "intro": f"A slab leak is one of the most serious — and most expensive — plumbing problems a {c} homeowner can face. Water leaking under your concrete foundation causes structural damage, mold growth, and dramatically higher water bills, often without any obvious visible sign until significant damage has occurred. This guide covers everything {c} homeowners need to know about slab leaks: how to recognize them, what causes them, and what your repair options are.",
            "label": "Slab Leak Detection Guide",
            "sections": [
                ("🏠 What Is a Slab Leak?",
                 f"A slab leak occurs when a water supply line or drain line running beneath your home's concrete foundation develops a crack, hole, or joint failure. The leak is hidden under concrete, so water seeps into the soil below the foundation and sometimes up through the slab itself. In {c}, slab leaks most commonly affect copper water supply pipes that have been in place for 20+ years, though PVC drain lines under the slab can also fail from soil movement and root intrusion."),
                ("⚠️ 7 Warning Signs of a Slab Leak in {c} Homes",
                 f"Watch for these indicators in your {c} home: (1) Water bill spikes with no change in usage. (2) Warm or hot spots on your floor — especially on tile or hardwood — from a hot water line leak. (3) Sound of running water when all fixtures are turned off. (4) Cracks appearing in your walls or flooring. (5) Damp or wet carpeting near exterior walls with no rain source. (6) Mold or mildew smell from floors or lower walls. (7) Low water pressure throughout the home despite no fixture changes."),
                ("🔍 What Causes Slab Leaks in {city}?",
                 f"The main causes of slab leaks in {c} homes are: (1) Pipe corrosion — copper pipes react with minerals in water and acidic soils over time. (2) Abrasion — pipes rub against concrete or gravel as they expand and contract with temperature changes, wearing pinhole leaks over decades. (3) Soil movement — ground settling, expansive clay soils, and seismic activity shift the foundation and stress buried pipes. (4) High water pressure — pressure consistently above 80 PSI accelerates joint failure. (5) Poor original installation — pipes installed without adequate bedding material contact concrete directly and abrade faster."),
                ("🛠️ How Slab Leaks Are Detected",
                 f"Licensed {c} plumbers use non-invasive methods to pinpoint slab leaks before any concrete is touched: (1) Electronic leak detection — sensitive listening equipment identifies the acoustic signature of water escaping under pressure through concrete. (2) Thermal imaging — infrared cameras reveal temperature differences on the floor surface caused by hot water leaks. (3) Pressure testing — isolating sections of the plumbing system identifies which line is losing pressure. (4) Video inspection — for drain line leaks, a camera is fed through the pipe to visually locate the failure point. Most slab leaks can be pinpointed within inches without any cutting."),
                ("🏗️ Slab Leak Repair Options in {city}",
                 f"Once a slab leak is confirmed in your {c} home, you have three repair approaches: (1) Spot repair — jackhammer a targeted section of concrete, repair the specific pipe failure, and repour. Best for isolated leaks in otherwise sound piping. (2) Pipe rerouting — run new pipe through the walls and attic, bypassing the under-slab line entirely. No concrete breaking required; preferred when the slab pipe is deteriorating overall. (3) Epoxy pipe lining — inject an epoxy liner through the existing pipe to seal pinholes and restore pipe integrity from the inside. Our {c} plumbers will assess which method is most appropriate and cost-effective for your specific situation."),
            ],
            "faqs": [
                (f"How do I know if I have a slab leak in my {c} home?",
                 f"The clearest signs of a slab leak are: an unexplained spike in your water bill, the sound of running water when all fixtures are off, warm spots on your floor, low water pressure throughout the home, and cracks forming in walls or flooring. To confirm, turn off all water fixtures, then check your water meter — if the dial still moves, water is leaking somewhere in your {c} home's plumbing system. Call a licensed {c} plumber for electronic slab leak detection to pinpoint the location precisely."),
                (f"How much does slab leak repair cost in {c}?",
                 f"Slab leak repair costs in {c} range from $500–$4,000+ depending on the repair method. Spot repair with concrete jackhammering typically costs $1,500–$3,500 including concrete restoration. Pipe rerouting through walls costs $1,000–$3,000 but avoids concrete work entirely. Epoxy pipe lining ranges from $500–$2,000 for a single line. The most cost-effective option depends on your pipe age, location, and material — our {c} plumbers provide a detailed written quote after leak detection so you can compare options before committing."),
                (f"Can a slab leak be repaired without breaking concrete in {c}?",
                 f"Yes — in many cases. Pipe rerouting installs new supply lines through your walls and attic, completely bypassing the failing under-slab pipe without any concrete removal. Epoxy pipe lining seals pinholes and small cracks from inside the existing pipe. Neither method requires jackhammering. However, if the leak is in a drain line, spot repair with targeted concrete removal is often the only practical option. Our licensed {c} plumbing team will recommend the least-invasive effective solution for your specific leak location and pipe condition."),
                (f"Does homeowners insurance cover slab leaks in {c}?",
                 f"Most {c} homeowners insurance policies cover sudden and accidental water damage caused by a slab leak — including damage to flooring, walls, and belongings — but typically do not cover the cost of the plumbing repair itself or the concrete restoration. Some policies include limited \"access coverage\" for opening the slab. Review your policy's water damage exclusions carefully. Our team provides detailed written inspection reports and technical documentation to support your insurance claim, and we communicate directly with adjusters when needed."),
            ],
        },
        # ── 3. DIY vs Professional Plumbing ───────────────────────────────────
        {
            "slug_prefix": "diy-vs-professional-plumbing",
            "title": f"DIY vs Professional Plumbing in {c}: Which Jobs to Do Yourself",
            "desc": f"Which plumbing jobs can you DIY in {c}, {ab} — and which require a licensed plumber? Learn safe DIY repairs, when professional help is essential, and the hidden risks of DIY plumbing mistakes.",
            "kw": f"diy plumbing {cl}, when to call a plumber {cl}, plumbing jobs {cl}, plumbing permits {cl}, licensed plumber {cl}",
            "h1": f"DIY vs Professional Plumbing in {c}: What You Can Fix Yourself",
            "hero_sub": f"Practical guidance from licensed plumbing repair professionals serving {c}, {st}",
            "intro": f"Every {c} homeowner faces a plumbing issue eventually. Knowing which repairs you can safely handle yourself — and which ones require a licensed {c} plumber — saves money without putting your home, health, or insurance coverage at risk. This guide gives you a clear framework for making that decision every time.",
            "label": "DIY vs Professional Plumbing Guide",
            "sections": [
                ("✅ Safe DIY Plumbing Repairs in {city}",
                 f"These repairs are low-risk, require no permit, and are manageable for most {c} homeowners with basic tools: replacing a toilet flapper or fill valve (turns off water supply, swap the part, restore water), swapping a faucet aerator (unscrew, clean or replace, reattach), replacing a showerhead (unscrew, apply thread tape, install new), clearing a simple sink clog (plunger or hand snake), replacing supply hose under a sink or toilet (turn off shutoff valve, swap the braided hose), and caulking around a tub or shower (remove old caulk, dry thoroughly, apply fresh bead). Keep the water shutoff valve location in mind — knowing how to stop water flow is essential for any DIY plumbing work."),
                ("🚨 Plumbing Jobs That Require a Licensed Plumber in {city}",
                 f"These jobs require licensing, permits, or specialized equipment in {c}: any work on the main water supply line entering your home, water heater installation or replacement (gas line connections require licensed work), sewer line repair or replacement, adding new plumbing fixtures that require new supply or drain lines, moving existing plumbing, water pressure regulator replacement, and any repair involving opening walls or slabs. In {c}, unpermitted plumbing work can void your homeowner's insurance, create liability during home sale, and result in failed inspections. A licensed {c} plumber obtains all required permits and handles inspections on your behalf."),
                ("⚠️ The Hidden Risks of DIY Plumbing in {city}",
                 f"DIY plumbing mistakes in {c} homes create problems that cost far more to fix than the original repair would have: improperly soldered or over-tightened fittings fail weeks later and cause water damage, incorrect drain slopes cause recurring clogs and sewage backups, cross-connection between supply and drain systems creates health hazards, working on gas water heaters without proper training risks carbon monoxide leaks, and using incorrect pipe materials fails inspection and must be redone. {c} water damage claims frequently exceed $10,000 — a repair that should have cost $300 professionally."),
                ("💰 When DIY Costs More Than Hiring a Pro",
                 f"DIY plumbing in {c} costs more than professional service when: you buy wrong parts and have to make multiple hardware store trips, you damage adjacent plumbing while attempting a repair, the repair fails and causes water damage that isn't covered by insurance (because unlicensed work voided your coverage), you need to hire a plumber anyway to fix the original problem plus your DIY damage, or a failed permit inspection requires demolishing finished work. For any repair beyond simple fixture replacements, compare the cost of a professional {c} plumber quote against your time investment and risk before starting."),
                ("🔍 How to Find a Licensed Plumber in {city}",
                 f"Verify any {c} plumber you hire: (1) Check their license with the {st} state licensing board — licensed plumbers are required to carry this documentation. (2) Confirm they carry general liability and workers compensation insurance — ask for certificates. (3) Get a written, itemized quote before work begins — legitimate {c} plumbers provide written estimates, not verbal approximations. (4) Check reviews on Google and the Better Business Bureau. Our licensed {c} plumbing team provides all credentials upfront, written quotes for every job, and guaranteed workmanship."),
            ],
            "faqs": [
                (f"Is it legal to do my own plumbing in {c}, {st}?",
                 f"Homeowners in {st} can legally perform plumbing repairs on their own primary residence in most cases, but work beyond simple maintenance — such as adding new lines, replacing a water heater, or any work requiring a permit — must be inspected regardless of who does it. If your DIY work fails inspection, you may be required to tear it out and hire a licensed contractor to redo it. For anything beyond basic fixture repair or clog clearing in your {c} home, check {st}'s plumbing code requirements or contact a licensed {c} plumber before starting."),
                (f"What plumbing repairs can I do without a permit in {c}?",
                 f"In {c}, most like-for-like fixture replacements do not require a permit: replacing a toilet, faucet, or showerhead with a same-type unit, swapping a water heater for a same-capacity same-fuel-type unit (varies by jurisdiction), and clearing drain clogs. However, any work that changes the plumbing system — adding fixtures, moving drain lines, changing pipe size, or installing a new water heater in a different location — typically requires a permit and inspection. When in doubt, call {c} building services or ask a licensed {c} plumber before starting."),
                ("What happens if my DIY plumbing work causes water damage?",
                 f"If water damage results from unpermitted or unlicensed plumbing work in your {c} home, your homeowner's insurance may deny the claim entirely — most policies exclude damage caused by work that should have been performed by a licensed professional. You would be responsible for all repair costs out of pocket, including structural drying, mold remediation, and rebuilding finished surfaces. This risk is the primary reason our licensed {c} plumbers recommend professional service for any repair beyond simple fixture maintenance."),
                (f"How do I verify a plumber is licensed in {st}?",
                 f"Check the {st} Contractor Licensing Board website — every licensed plumber in {st} has a public record with their license number, expiration date, and any disciplinary actions. Ask any {c} plumber you're considering for their license number and look it up before work begins. Also request proof of general liability insurance and workers compensation coverage. Our {c} plumbing team provides all licensing and insurance documentation upfront — no need to ask."),
            ],
        },
        # ── 4. Spring Plumbing Checklist ───────────────────────────────────────
        {
            "slug_prefix": "spring-plumbing-checklist",
            "title": f"Spring Plumbing Checklist for {c}, {ab} Homeowners | 2026",
            "desc": f"Complete spring plumbing checklist for {c}, {ab} homeowners. Inspect pipes, water heater, sewer, and outdoor faucets after winter — before summer demand peaks. From licensed {c} plumbers.",
            "kw": f"spring plumbing checklist {cl}, plumbing maintenance {cl}, spring plumbing tips {cl}, plumbing inspection {cl}, plumber {cl}",
            "h1": f"Spring Plumbing Checklist for {c} Homeowners",
            "hero_sub": f"Annual maintenance guide from licensed plumbing repair professionals serving {c}, {st}",
            "intro": f"Spring is the ideal time for {c} homeowners to inspect their plumbing system before summer demand peaks. Winter temperature swings stress pipes, joints, and water heater components. A thorough spring inspection catches small problems — a hairline crack, early corrosion, slow sediment buildup — before they become emergency repairs. This checklist covers everything that should be inspected each spring in a {c} home.",
            "label": "Spring Plumbing Checklist",
            "sections": [
                ("🌿 Outdoor Plumbing Spring Checklist",
                 f"Start outside your {c} home: (1) Inspect all hose bibs (outdoor spigots) for cracks from winter freezing — even in milder {c} winters, brief freezes can split the internal washer seat. Turn each on fully and check for drips or reduced flow. (2) Check your irrigation system — turn on each zone and walk the perimeter looking for broken heads, sunken emitters, and leaking valve boxes. (3) Inspect the main water meter box for pooling water that could indicate a leak in the supply line. (4) Check all exterior drain covers for debris that accumulated over winter and clear them before spring rains."),
                ("🔧 Indoor Plumbing Spring Inspection",
                 f"Move through your {c} home and check: (1) Under every sink — look for moisture, water stains, or active drips on supply lines, shutoff valves, and P-traps. Valves that haven't been exercised in years can seize open or fail when you need them most — turn each one fully off and back on. (2) Check toilet bases for rocking movement (wax ring failure) and staining around the base (slow leak). (3) Inspect all visible pipe runs in the basement, crawlspace, or utility closet for corrosion, joint staining, or new cracks. (4) Test every drain in the home for slow drainage — spring is the right time to hydro-jet drains before summer guest season."),
                ("🔥 Water Heater Spring Service",
                 f"Your water heater needs annual attention: (1) Flush the tank — connect a hose to the drain valve, turn off the cold supply, and drain until the water runs clear. Sediment that accumulates at the bottom reduces efficiency and accelerates tank corrosion. In {c}, water hardness varies by neighborhood, but most homes benefit from an annual flush. (2) Test the pressure relief (T&P) valve — carefully lift the lever to verify it opens and reseats properly. A stuck T&P valve is a safety hazard. (3) Check the anode rod — if less than 50% of the original rod remains, replace it. This small rod is what prevents tank corrosion. (4) On gas units, verify the burner ignites cleanly and the flue pipe has no visible corrosion or disconnections."),
                ("🔬 Sewer & Drain Spring Checks",
                 f"Winter root growth in {c} sewer lines peaks in spring as trees send out feeder roots seeking moisture: (1) If you notice slow drains throughout the home (multiple fixtures), gurgling sounds when water drains, or sewage odors from floor drains, schedule a camera inspection before the problem becomes a full blockage. (2) Check all floor drains in utility rooms, garages, and basements — pour a gallon of water into each to refill evaporated P-traps and prevent sewer gas entry. (3) If your home was built before 1980 and you haven't had a sewer camera inspection in 5+ years, spring is the right time to check the condition of aging clay or cast iron sewer lines."),
                ("📞 When to Call a {city} Plumber This Spring",
                 f"Schedule a licensed {c} plumber if your spring inspection reveals: any active leak under sinks, around toilets, or from the water heater; a hose bib that drips or has reduced flow (internal valve damage); multiple slow drains throughout the home; water heater over 10 years old with sediment or anode rod problems; visible corrosion on copper or galvanized pipes; or if your {c} home has original plumbing over 40 years old. Our team offers complete spring plumbing inspections with a written condition report so you know exactly what needs attention before small problems become summer emergencies."),
            ],
            "faqs": [
                (f"What plumbing should I check every spring in {c}?",
                 f"Every spring, {c} homeowners should inspect: all outdoor hose bibs for freeze damage, under-sink supply lines and shutoff valves for slow drips, the water heater (flush sediment, test T&P valve, check anode rod), all toilets for base leaks or rocking, floor drains (refill P-traps), and sewer line condition if the home is pre-1980. The most important check is turning on every shutoff valve under sinks and toilets — valves that seize open fail when you need them in an emergency."),
                (f"How do I check for winter pipe damage in {c}?",
                 f"After winter in {c}, check all supply pipes in unheated spaces (garage, crawlspace, exterior walls) for hairline cracks — even slow seeps cause major damage over time. Turn on each hose bib and check for drips, reduced flow, or water coming from unexpected locations around the fitting. Under sinks, wipe each pipe with a dry paper towel and check for moisture. If your water bill increased over winter without a usage reason, a frozen pipe may have cracked without fully failing — call a {c} plumber for a pressure test."),
                ("Should I flush my water heater in spring?",
                 f"Yes — an annual tank flush is recommended for most water heaters to remove sediment that accumulates at the bottom of the tank. Sediment reduces efficiency, causes popping sounds during heating, accelerates corrosion, and reduces the effective capacity of your tank. Connect a garden hose to the drain valve, shut off the cold water supply, and drain until the water runs clear. For tankless water heaters, spring is a good time to descale the heat exchanger — especially in areas with hard water. Our {c} plumbers include a full water heater service in our spring inspection package."),
                (f"What are signs my sewer line needs spring inspection in {c}?",
                 f"Schedule a {c} sewer camera inspection this spring if you notice: multiple slow drains throughout the home (not just one fixture), gurgling sounds from floor drains or toilets when other fixtures drain, sewage odors from drains or the yard, wet or unusually green patches in your yard above the sewer line path, or if your home is pre-1980 with original clay or cast iron sewer pipe. Tree root intrusion is the most common cause of spring sewer problems in {c} — roots actively seek water through joint cracks and grow significantly during spring."),
            ],
        },
        # ── 5. Holiday Plumbing Tips ───────────────────────────────────────────
        {
            "slug_prefix": "holiday-plumbing-tips",
            "title": f"Holiday Plumbing Tips for {c} Homeowners | Avoid Emergency Calls",
            "desc": f"Holiday plumbing tips for {c}, {ab} homeowners. Prevent kitchen drain clogs, toilet backups, and garbage disposal failures during Thanksgiving, Christmas, and New Year's gatherings.",
            "kw": f"holiday plumbing tips {cl}, thanksgiving plumbing {cl}, holiday drain clog {cl}, emergency plumber holiday {cl}, plumber {cl}",
            "h1": f"Holiday Plumbing Tips for {c} Homeowners",
            "hero_sub": f"Prevent holiday plumbing emergencies — guide from licensed plumbing repair professionals in {c}, {st}",
            "intro": f"The holiday season is the busiest time of year for {c} plumbers. Extra guests, more cooking, and increased bathroom use put more strain on your home's plumbing in a few days than it normally sees in weeks. A little preparation before guests arrive prevents the most common holiday plumbing disasters — and knowing what to do when problems happen keeps your gathering on track.",
            "label": "Holiday Plumbing Tips Guide",
            "sections": [
                ("✅ Pre-Holiday Plumbing Checklist for {city} Homes",
                 f"Before guests arrive at your {c} home: (1) Test all toilets — a running or slowly-flushing toilet will be overwhelmed by extra use. Replace any worn flapper before the holiday. (2) Check under all sinks for slow drips that will worsen under high-use conditions. (3) Locate your main water shutoff valve and make sure all adults in the home know where it is — in a plumbing emergency, seconds matter. (4) Have a plunger accessible in every bathroom — don't make guests search for one. (5) Run hot water through all drains to verify good flow before cooking begins. If any drain is sluggish before guests arrive, have it cleared professionally."),
                ("🍽️ Kitchen Drain & Garbage Disposal Holiday Rules",
                 f"The kitchen is where most {c} holiday plumbing emergencies originate. For your disposal: never put turkey bones, skin, or fat down the disposal — grease solidifies in pipes and causes blockages that won't clear until the pipe is professionally cleaned. Potato peels, celery, and onion skins also clog disposals. For your kitchen drain: pour cooking grease into a jar or can and dispose of it in the trash — never in the drain. Run cold water for 30 seconds before and after using the disposal. If the drain is draining slowly before your gathering, hydro-jet it before guests arrive rather than hoping it holds up."),
                ("🚿 Bathroom Plumbing Tips for Extra Guests",
                 f"With extra guests comes significantly increased bathroom load in your {c} home: (1) Allow 10–15 minutes between showers — this prevents water heater recovery issues and gives slow drains time to clear. (2) Post a small sign asking guests not to flush items other than toilet paper — wet wipes, paper towels, and cotton products cause blockages even when labeled 'flushable.' (3) Place a small trash can in every bathroom near the toilet — guests will use it if it's there. (4) If you have a septic system, remind guests to conserve water and avoid harsh cleaners that disrupt septic bacteria."),
                ("🚨 Most Common Holiday Plumbing Emergencies in {city}",
                 f"The top holiday plumbing calls our {c} team receives: (1) Grease-clogged kitchen drains from holiday cooking — turkey fat, bacon grease, and butter all solidify in pipes. (2) Toilet clogs from overuse and flushed non-flushable items. (3) Garbage disposal jams from fibrous vegetables and bones. (4) Slow or backed-up bathroom drains from hair and soap buildup under extra demand. (5) Water heater recovery complaints from consecutive showers depleting the tank. The good news: most of these are preventable with the steps above, and our {c} team is available 24/7 when they're not."),
                ("📞 Emergency Plumbing on Holidays in {city}",
                 f"If a plumbing emergency strikes during your {c} holiday gathering: (1) Locate and close the main water shutoff valve immediately to stop flooding. (2) Turn off your water heater to prevent damage from running dry. (3) Move valuables away from water-affected areas. (4) Document damage with photos for your insurance claim. (5) Call our {c} emergency plumbing line — we respond 24/7, including Thanksgiving, Christmas, and New Year's Day, with no extra holiday surcharge. A licensed {c} plumber will be dispatched within 1–2 hours."),
            ],
            "faqs": [
                (f"Why is Thanksgiving the busiest day for plumbers in {c}?",
                 f"Thanksgiving combines the three leading causes of drain emergencies: large amounts of cooking grease entering kitchen drains (turkey fat, butter, pan drippings), garbage disposal overload from fibrous vegetable scraps and starchy potato peels, and significantly increased toilet use from extra guests. The combination of a full kitchen drain and maximum bathroom traffic overwhelms systems that handle normal daily load without issue. In {c}, our plumbers respond to more emergency calls on Thanksgiving than on any other single day of the year."),
                ("What should never go down the drain during holiday cooking?",
                 f"Never put turkey or chicken skin, cooking grease or fat (pour into a can and trash it), potato peels, celery, onion skins, artichoke leaves, eggshells, rice, pasta, or flour down your kitchen drain. These items either solidify in your drain pipes or expand with water and create blockages that require professional clearing. Even with a garbage disposal, starchy and fibrous items cause problems. The simplest rule: if it came from a can, box, or refrigerator, it can go in the trash or disposal. If it's liquid fat or cooking grease, it goes in the trash."),
                (f"How do I prevent toilet clogs with extra guests in {c}?",
                 f"Place a small, clearly visible trash can next to every toilet in your {c} home before guests arrive — guests will use it if it's available, reducing what gets flushed. Post a polite note asking guests to flush only toilet paper. Check that each toilet flushes with full force before your event — a weak flush is the first sign of a partial clog that will worsen under extra use. Avoid 'flushable' wipes — they don't dissolve and are a leading cause of sewer blockages. If a toilet runs slowly, have a plunger accessible and visible in each bathroom."),
                (f"Is emergency plumbing available on holidays in {c}?",
                 f"Yes — our {c} plumbing team provides 24/7 emergency service on all holidays, including Thanksgiving, Christmas Eve, Christmas Day, and New Year's Eve and Day, at no extra surcharge for after-hours or holiday timing. You receive the same written upfront quote regardless of when you call. A licensed {c} technician will be dispatched to your address within 1–2 hours of your call. Don't let a holiday plumbing emergency ruin your gathering — call us and we'll have your plumbing back in service as quickly as possible."),
            ],
        },
        # ── 6. Copper vs PEX Pipes ─────────────────────────────────────────────
        {
            "slug_prefix": "copper-vs-pex-pipes",
            "title": f"Copper vs PEX Pipes in {c}: Which Is Best for Your Home?",
            "desc": f"Copper vs PEX pipes in {c}, {ab} — which pipe material is right for your home? Compare cost, lifespan, performance with {c}'s water, and get expert recommendations from licensed {c} plumbers.",
            "kw": f"copper vs pex pipes {cl}, pex plumbing {cl}, repiping {cl}, pipe material {cl}, copper pipe {cl}, plumber {cl}",
            "h1": f"Copper vs PEX Pipes in {c}: Which Is Right for Your Home?",
            "hero_sub": f"Pipe material comparison from licensed plumbing repair professionals serving {c}, {st}",
            "intro": f"If you're repiping your {c} home, replacing damaged supply lines, or building a new addition, you'll face a fundamental material choice: copper or PEX. Both are widely used throughout {c}, but they perform differently depending on your home's water chemistry, climate exposure, budget, and existing plumbing. This guide breaks down the real-world comparison for {c} homeowners so you can make the right decision.",
            "label": "Copper vs PEX Pipes Guide",
            "sections": [
                ("🔶 Copper Pipes: Advantages & Disadvantages in {city}",
                 f"Copper has been the standard water supply material in {c} homes for decades and carries real advantages: it is naturally antimicrobial, has a 50+ year lifespan in ideal conditions, is fully recyclable, handles high temperatures without expansion concerns, and is compatible with all fittings and fixtures. However, copper has significant downsides in certain {c} conditions: it is susceptible to pinhole corrosion from water with low pH or high chloramine levels, it expands and contracts with temperature changes and can stress solder joints over decades, it costs substantially more than PEX in material and labor, and it requires torch soldering that can cause fire hazards in walls during installation."),
                ("🔵 PEX Pipes: Advantages & Disadvantages in {city}",
                 f"PEX (cross-linked polyethylene) has become the most commonly installed water supply pipe in {c} new construction for good reason: it is significantly less expensive than copper in both material and labor costs, it is flexible and can run around corners without fittings (reducing potential failure points), it is highly resistant to freeze damage (expands rather than cracks under freezing), and it resists the corrosion and pitting that affects copper in certain water conditions. Limitations: PEX cannot be used for exterior applications (degrades in UV light), requires specialized crimp or expansion fittings rather than standard threaded connections, has a shorter proven track record than copper, and cannot be reused once crimped."),
                ("🏠 Which Pipe Material Is Right for {city} Homes?",
                 f"The right choice for your {c} home depends on your specific situation. PEX is generally recommended for: whole-home repiping projects where material cost matters, homes with water conditions that have caused pitting in existing copper, areas where pipes run through exterior walls with freeze risk, and new construction. Copper is generally recommended for: short repair sections where you're matching existing copper, exterior supply lines that will be exposed to sunlight, homes where long-term durability with no plastic concerns is the priority, and high-temperature applications near water heaters. Our {c} plumbers will assess your specific water chemistry and home conditions before recommending a material."),
                ("💰 Cost Comparison: Copper vs PEX Repiping in {city}",
                 f"For a full home repipe in {c}, the cost difference is significant: copper repiping typically costs $8,000–$15,000+ for a 2,000–3,000 sq ft home, including materials and labor. PEX repiping for the same home typically runs $4,000–$8,000 — roughly 40–60% less. The savings come from lower material cost and faster installation (PEX runs through walls with fewer fittings, reducing labor hours significantly). Both materials come with manufacturer warranties, and both are installed to the same plumbing code standards. Our {c} plumbers provide detailed written quotes for both options so you can compare before committing."),
                ("🔍 What Our Licensed {city} Plumbers Recommend",
                 f"Our licensed {c} plumbing team installs both copper and PEX depending on the application. For most whole-home repiping projects in {c}, we recommend PEX-A (the highest-grade PEX, using the expansion connection method rather than crimp) for its combination of reliability, longevity, freeze resistance, and cost savings. For repairs and extensions matching existing copper systems, we typically recommend copper to avoid dissimilar-metal connection issues. For any repiping project, we provide a written materials recommendation, itemized quote, and permit handling — you make the final decision with full information."),
            ],
            "faqs": [
                (f"Is PEX or copper better for {c}'s water conditions?",
                 f"The answer depends on your {c} home's specific water chemistry. In areas with hard water or neutral-to-high pH, both materials perform well long-term. In areas with slightly acidic or aggressive water, copper is more vulnerable to pitting corrosion and PEX is the better long-term choice. If your existing copper pipes have shown pitting, pinhole leaks, or green staining, PEX is the recommended replacement material. Our {c} plumbers assess your water conditions and existing pipe condition before recommending a material — the right answer varies by neighborhood and home age."),
                (f"How long do copper pipes last in {c} homes?",
                 f"Copper pipes in {c} homes typically last 40–70+ years in favorable water conditions. However, pipes in homes with aggressive or acidic water conditions can develop pinholes in as little as 15–20 years. Signs your {c} home's copper pipes are failing: discolored (blue-green) water when you first turn on a tap, visible green staining or pitting on exposed pipe sections, multiple pinhole leaks appearing in different locations, and blue-green staining in sink bowls. If you see multiple pinholes in different areas of your home, the entire system is likely affected and full repiping is more cost-effective than continued spot repairs."),
                ("Is PEX pipe safe for drinking water?",
                 f"Yes — PEX pipe is approved for potable water use by all major plumbing codes including the International Plumbing Code and the Uniform Plumbing Code, and is NSF 61 certified for safety with drinking water. Some early studies raised concerns about taste or odor with certain PEX formulations, but modern PEX pipe produced by reputable manufacturers meets all drinking water safety standards. PEX-A (made with the peroxide method) is generally considered the highest-quality grade and has the best performance record for residential water supply applications."),
                (f"How much does repiping cost in {c}?",
                 f"Full home repiping in {c} typically costs $4,000–$15,000 depending on home size, pipe material (PEX or copper), number of stories, accessibility, and whether drywall repair is included. A 1,500 sq ft single-story home typically costs $4,000–$7,000 in PEX or $7,000–$12,000 in copper. Larger or multi-story {c} homes cost more due to additional pipe runs and wall access complexity. Our team provides a detailed written quote after an on-site assessment — no estimates over the phone, because every {c} home's plumbing layout is different."),
            ],
        },
    ]

# ── HTML Generation ───────────────────────────────────────────────────────────

HAMBURGER_JS = "var n=document.querySelector('.nav-links');var o=n.classList.toggle('open');this.classList.toggle('open');this.setAttribute('aria-expanded',o)"

def faq_schema(faqs):
    items = []
    for q, a in faqs:
        q_j = q.replace('\\', '\\\\').replace('"', '\\"')
        a_j = a.replace('\\', '\\\\').replace('"', '\\"')
        items.append(
            '    {\n'
            '      "@type": "Question",\n'
            f'      "name": "{q_j}",\n'
            '      "acceptedAnswer": {\n'
            '        "@type": "Answer",\n'
            f'        "text": "{a_j}"\n'
            '      }\n'
            '    }'
        )
    return ',\n'.join(items)

def article_card_html(url, title, excerpt):
    return (
        f'\n<article style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:28px;display:flex;flex-direction:column;gap:12px">\n'
        f'  <div style="font-size:.82em;color:#64748b;font-weight:600">📖 Plumbing Repair Guide</div>\n'
        f'  <h2 style="font-size:1.15em;margin:0"><a href="{url}" style="color:var(--dark);text-decoration:none">{title}</a></h2>\n'
        f'  <p style="color:#64748b;font-size:.92em;line-height:1.6">{excerpt}</p>\n'
        f'  <a href="{url}" style="color:var(--primary);font-weight:700;text-decoration:none;font-size:.93em">Read Guide →</a>\n'
        f'</article>\n'
    )

def build_page(cslug, city, state, abbr, city_lc, blog):
    slug_prefix = blog["slug_prefix"]
    # city blog slug for folder (re-derive from city name same way update_blog_pages does)
    city_blog_slug = city.lower().replace(' ', '-')
    folder = f"{slug_prefix}-{city_blog_slug}"
    url = f"https://plumbersinusa.com/{cslug}/{folder}/"
    geo_region = f"US-{abbr}"

    title = blog["title"]
    desc  = blog["desc"]
    kw    = blog["kw"]
    h1    = blog["h1"]
    hero_sub = blog["hero_sub"]
    intro = blog["intro"]
    sections = [(h.replace("{city}", city), b.replace("{city}", city)) for h, b in blog["sections"]]
    faqs  = [(q.replace("{city}", city).replace("{state}", state).replace("{abbr}", abbr),
              a.replace("{city}", city).replace("{state}", state).replace("{abbr}", abbr))
             for q, a in blog["faqs"]]

    faq_html_items = ''.join(
        f'<div class="faq-item"><div class="faq-q">{q} <span>&#9660;</span></div><div class="faq-a">{a}</div></div>'
        for q, a in faqs
    )

    sections_html = ''.join(
        f'<h2>{h}</h2><p>{b}</p><br>\n'
        for h, b in sections
    )

    published = blog.get("published", "2026-05-01")

    html = f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="theme-color" content="#1B4F8A">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{kw}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1">
<meta name="msvalidate.01" content="7255902715A8558A3846E514B12676EA">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://plumbersinusa.com/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="geo.region" content="{geo_region}">
<meta name="geo.placename" content="{city}">
<meta name="google-site-verification" content="ug1XewAbyHa_2MIWDCaXIb5O-BBbHqyYSmsxgTwnE2Q">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "description": "{desc}",
  "author": {{
    "@type": "Organization",
    "name": "PlumbersInUSA.com"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "PlumbersInUSA.com",
    "logo": {{
      "@type": "ImageObject",
      "url": "https://plumbersinusa.com/og-image.png"
    }}
  }},
  "datePublished": "{published}",
  "dateModified": "2026-05-19",
  "mainEntityOfPage": "{url}"
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://plumbersinusa.com/"
    }},
    {{
      "@type": "ListItem",
      "position": 2,
      "name": "Plumbing Repair {city}",
      "item": "https://plumbersinusa.com/{cslug}/"
    }},
    {{
      "@type": "ListItem",
      "position": 3,
      "name": "Blog",
      "item": "https://plumbersinusa.com/{cslug}/blog/"
    }},
    {{
      "@type": "ListItem",
      "position": 4,
      "name": "{h1}",
      "item": "{url}"
    }}
  ]
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
{faq_schema(faqs)}
  ]
}}
</script>
<style>
{CSS}
</style>
</head>
<body>
<a href="#main-content" class="skip-nav">Skip to main content</a>
<header class="site-header" role="banner">
  <div class="header-inner">
    <a class="brand" href="https://plumbersinusa.com/" aria-label="PlumbersInUSA.com - Home">PlumbersInUSA.com</a>
    <nav aria-label="Primary navigation" style="display:flex;align-items:center;gap:8px">
      <ul class="nav-links">
        <li><a href="https://plumbersinusa.com/{cslug}/" style="color:rgba(255,255,255,.85);text-decoration:none;font-size:.93em">Home</a></li>
        <li><a href="https://plumbersinusa.com/{cslug}/emergency-plumbing/" style="color:rgba(255,255,255,.85);text-decoration:none;font-size:.93em">Services</a></li>
        <li><a href="https://plumbersinusa.com/{cslug}/blog/" style="color:rgba(255,255,255,.85);text-decoration:none;font-size:.93em">Blog</a></li>
        <li class="desktop-call"><a href="tel:PHONE_NUMBER" class="header-phone-link" aria-label="Call Plumbing Repair in {city}">&#128222; Call Now</a></li>
      </ul>
      <a href="tel:PHONE_NUMBER" class="header-phone-link hamburger-call" style="display:none" aria-label="Call Now">&#128222; Call</a>
      <button class="hamburger" aria-label="Toggle menu" aria-expanded="false" onclick="{HAMBURGER_JS}">
        <span></span><span></span><span></span>
      </button>
    </nav>
  </div>
</header>
<main id="main-content">
<section class="hero">
  <div class="hero-inner">
    <h1>{h1}</h1>
    <p class="hero-sub">{hero_sub}</p>
    <div class="hero-cta">
      <a href="tel:PHONE_NUMBER" class="btn-call">&#128222; Need Help? Call &#8212; PHONE_NUMBER</a>
    </div>
  </div>
</section>
<article>
  <div class="section-inner">
    <nav aria-label="Breadcrumb" class="breadcrumb"><a href="https://plumbersinusa.com/">Home</a> &#8250; <a href="https://plumbersinusa.com/{cslug}/">Plumbing Repair {city}, {abbr}</a> &#8250; <a href="https://plumbersinusa.com/{cslug}/blog/">Blog</a> &#8250; <span aria-current="page">{h1}</span></nav>
    <p style="color:#64748b;font-size:.88em;margin-bottom:24px">Published by {city} Plumbing Repair Experts | Updated May 2026</p>
    <p style="font-size:1.05em;line-height:1.8">{intro}</p><br>
    {sections_html}
    <div style="background:var(--light);border-left:4px solid var(--primary);padding:20px 24px;border-radius:8px;margin:32px 0">
      <strong>Need professional plumbing repair help in {city}?</strong><br>
      Our licensed team serves all {city} neighborhoods &#8212; 24/7 emergency service, free quotes, same-day availability.<br><br>
      <a href="tel:PHONE_NUMBER" class="btn-call" style="font-size:.95em">&#128222; Call Now &#8212; PHONE_NUMBER</a>
    </div>
    <h2>Frequently Asked Questions</h2>
    <div class="faq-list">
      {faq_html_items}
    </div>
  </div>
</article>
<section class="bg-light">
  <div class="section-inner">
    <h2>Our Plumbing Repair Services in {city}</h2>
    <p class="section-sub">Need hands-on help? Our licensed {city} team handles all plumbing repair services:</p>
    <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:16px">
      <a href="https://plumbersinusa.com/{cslug}/drain-cleaning/" style="background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:10px 16px;text-decoration:none;color:var(--primary);font-weight:600;font-size:.9em">&#128703; Drain Cleaning</a>
      <a href="https://plumbersinusa.com/{cslug}/water-heater-repair/" style="background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:10px 16px;text-decoration:none;color:var(--primary);font-weight:600;font-size:.9em">&#128293; Water Heater Repair</a>
      <a href="https://plumbersinusa.com/{cslug}/pipe-repair/" style="background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:10px 16px;text-decoration:none;color:var(--primary);font-weight:600;font-size:.9em">&#128295; Pipe Repair</a>
      <a href="https://plumbersinusa.com/{cslug}/leak-detection/" style="background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:10px 16px;text-decoration:none;color:var(--primary);font-weight:600;font-size:.9em">&#128167; Leak Detection</a>
      <a href="https://plumbersinusa.com/{cslug}/sewer-line-repair/" style="background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:10px 16px;text-decoration:none;color:var(--primary);font-weight:600;font-size:.9em">&#9881; Sewer Line Repair</a>
      <a href="https://plumbersinusa.com/{cslug}/emergency-plumbing/" style="background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:10px 16px;text-decoration:none;color:var(--primary);font-weight:600;font-size:.9em">&#128680; Emergency Plumbing Repair</a>
    </div>
  </div>
</section>
<section>
  <div class="section-inner">
    <h2>More Plumbing Repair Tips for {city} Homeowners</h2>
    <p>Explore our complete guide library for {city}, {abbr} homeowners:</p>
    <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:16px">
      <a href="https://plumbersinusa.com/{cslug}/how-to-unclog-drain-{city_blog_slug}/" style="background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:10px 16px;text-decoration:none;color:var(--primary);font-weight:600;font-size:.92em">How to Unclog a Drain</a>
      <a href="https://plumbersinusa.com/{cslug}/signs-you-need-a-plumber-{city_blog_slug}/" style="background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:10px 16px;text-decoration:none;color:var(--primary);font-weight:600;font-size:.92em">7 Signs You Need a Plumber</a>
      <a href="https://plumbersinusa.com/{cslug}/fix-a-running-toilet-{city_blog_slug}/" style="background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:10px 16px;text-decoration:none;color:var(--primary);font-weight:600;font-size:.92em">How to Fix a Running Toilet</a>
      <a href="https://plumbersinusa.com/{cslug}/low-water-pressure-causes-{city_blog_slug}/" style="background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:10px 16px;text-decoration:none;color:var(--primary);font-weight:600;font-size:.92em">Low Water Pressure: Causes &amp; Fixes</a>
    </div>
    <br><a href="https://plumbersinusa.com/{cslug}/blog/" style="color:var(--primary);font-weight:700;text-decoration:none;font-size:.9em">View All {city} Guides &#8594;</a>
  </div>
</section>
<section class="cta-banner">
  <h2>Need Plumbing Repair in {city}?</h2>
  <a href="tel:PHONE_NUMBER" class="btn-call" style="font-size:1.2em">&#128222; Free Quote &#8212; PHONE_NUMBER</a>
  <span class="cta-phone-big">PHONE_NUMBER</span>
</section></main>
<div class="sticky-cta" role="complementary" aria-label="Call to action">
  <a href="tel:PHONE_NUMBER" aria-label="Call Plumbing Repair in {city} &#8212; PHONE_NUMBER">
    &#128222; Call Now &#8212; Free Quote: PHONE_NUMBER
  </a>
</div>
<footer role="contentinfo">
  <div class="footer-inner">
    <div class="footer-grid">
      <div class="footer-col">
        <h4>Plumbing Guides for {city}, {abbr}</h4>
        <p style="font-size:.92em;color:#94a3b8;line-height:1.7">Licensed &amp; insured plumbing repair professionals serving {city}, {state} and surrounding areas. Available 24/7.</p>
      </div>
      <div class="footer-col">
        <h4>Our Services</h4>
        <ul>
          <li><a href="https://plumbersinusa.com/{cslug}/emergency-plumbing/">&#128680; Emergency Plumbing Repair</a></li>
          <li><a href="https://plumbersinusa.com/{cslug}/drain-cleaning/">&#128703; Drain Cleaning</a></li>
          <li><a href="https://plumbersinusa.com/{cslug}/water-heater-repair/">&#128293; Water Heater Repair</a></li>
          <li><a href="https://plumbersinusa.com/{cslug}/pipe-repair/">&#128295; Pipe Repair</a></li>
          <li><a href="https://plumbersinusa.com/{cslug}/leak-detection/">&#128167; Leak Detection</a></li>
          <li><a href="https://plumbersinusa.com/{cslug}/sewer-line-repair/">&#9881; Sewer Line Repair</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Plumbing Repair Guides</h4>
        <ul>
          <li><a href="https://plumbersinusa.com/{cslug}/blog/">All Guides</a></li>
          <li><a href="https://plumbersinusa.com/{cslug}/how-to-unclog-drain-{city_blog_slug}/">How to Unclog a Drain</a></li>
          <li><a href="https://plumbersinusa.com/{cslug}/signs-you-need-a-plumber-{city_blog_slug}/">7 Signs You Need a Plumber</a></li>
          <li><a href="https://plumbersinusa.com/{cslug}/slab-leak-detection-{city_blog_slug}/">Slab Leak Detection</a></li>
          <li><a href="https://plumbersinusa.com/{cslug}/garbage-disposal-repair-{city_blog_slug}/">Garbage Disposal Repair</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Service Areas</h4>
        <ul>
          <li><a href="https://plumbersinusa.com/locations/">&#128205; All Service Areas</a></li>
          <li><a href="https://plumbersinusa.com/plumber-phoenix-az/">Phoenix, AZ</a></li>
          <li><a href="https://plumbersinusa.com/plumber-houston-tx/">Houston, TX</a></li>
          <li><a href="https://plumbersinusa.com/plumber-dallas-tx/">Dallas, TX</a></li>
          <li><a href="https://plumbersinusa.com/plumber-austin-tx/">Austin, TX</a></li>
          <li><a href="https://plumbersinusa.com/plumber-san-antonio-tx/">San Antonio, TX</a></li>
          <li><a href="https://plumbersinusa.com/plumber-fort-worth-tx/">Fort Worth, TX</a></li>
          <li><a href="https://plumbersinusa.com/locations/" style="color:#94a3b8;font-size:.88em">View All 20 Cities &#8594;</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Contact Us</h4>
        <ul>
          <li style="color:#94a3b8">{city}, {state}</li>
          <li><a href="tel:PHONE_NUMBER">PHONE_NUMBER</a></li>
          <li style="color:#94a3b8">Open 24 Hours / 7 Days</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 PlumbersInUSA.com | Licensed &amp; Insured Plumbers in {city}, {state}</p>
    </div>
  </div>
</footer>
</body>
</html>"""
    return folder, html


def update_blog_index(blog_index_path, new_article_cards):
    """Inject new article cards into the blog index page grid."""
    if not os.path.exists(blog_index_path):
        return False
    with open(blog_index_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find the closing of the blog grid (before </div></div></section><section class="cta-banner">)
    marker = '    </div>\n  </div>\n</section>\n<section class="cta-banner">'
    if marker not in html:
        # Try alternate whitespace
        marker = '</div>\n  </div>\n</section>\n<section class="cta-banner">'
    if marker not in html:
        return False

    # Skip if already updated (check for one of the new slugs)
    if 'garbage-disposal-repair' in html:
        return False  # already updated

    insertion = ''.join(new_article_cards)
    html = html.replace(marker, insertion + marker, 1)
    with open(blog_index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return True


# ── Main ──────────────────────────────────────────────────────────────────────

created = skipped = blog_idx_ok = blog_idx_skip = 0

for (cslug, city, state, abbr, _) in CITIES:
    city_lc = city.lower()
    city_blog_slug = city.lower().replace(' ', '-')
    blogs = get_blogs(city, state, abbr, city_lc)

    new_cards = []

    for blog in blogs:
        folder, html = build_page(cslug, city, state, abbr, city_lc, blog)
        out_dir = os.path.join(BASE, cslug, folder)
        out_path = os.path.join(out_dir, 'index.html')

        if os.path.exists(out_path):
            skipped += 1
            continue

        os.makedirs(out_dir, exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        created += 1

        # Build article card for blog index
        url = f"https://plumbersinusa.com/{cslug}/{folder}/"
        new_cards.append(article_card_html(url, blog["h1"], blog["desc"][:120] + "..."))

    # Update blog index
    blog_index_path = os.path.join(BASE, cslug, 'blog', 'index.html')
    if new_cards:
        ok = update_blog_index(blog_index_path, new_cards)
        if ok:
            blog_idx_ok += 1
        else:
            blog_idx_skip += 1

print(f"Created: {created} new blog pages")
print(f"Skipped (already exist): {skipped}")
print(f"Blog index pages updated: {blog_idx_ok}")
print(f"Blog index pages skipped: {blog_idx_skip}")
