import os, re, json

BASE = r"C:\Users\Dhruvisha\Desktop\plumbing-site"

# ── City data ──────────────────────────────────────────────────────────────────
CITIES = [
    {"slug":"plumber-phoenix-az","city":"Phoenix","state":"Arizona","abbr":"AZ","rate":"$85–$150",
     "drain_local":"Phoenix's extremely hard water (300+ mg/L) accelerates mineral buildup inside pipes, making clogs more frequent than in softer-water cities",
     "emergency_local":"Phoenix's extreme summer temperatures above 110°F and occasional winter freezes stress pipes and connections — sudden failures are common year-round",
     "wh_local":"Phoenix's extremely hard water (300+ mg/L) deposits sediment in water heaters rapidly, cutting efficiency and lifespan significantly faster than the national average",
     "pipe_local":"Phoenix's expansive desert clay soils shift with monsoon rains, stressing underground pipe connections and causing joint separation throughout the metro area",
     "leak_local":"Phoenix's high-mineral water and shifting desert soils create ideal conditions for slab leak formation — the city has one of the highest slab leak rates in the Southwest",
     "sewer_local":"Drought-resistant trees like mesquite and palo verde send deep roots toward sewer moisture in Phoenix's dry desert climate, causing frequent sewer line intrusions"},
    {"slug":"plumber-houston-tx","city":"Houston","state":"Texas","abbr":"TX","rate":"$80–$150",
     "drain_local":"Houston's flat topography reduces natural drain pressure, and the city's clay-rich soil promotes aggressive root intrusion into drain lines throughout the metro",
     "emergency_local":"Houston's highly expansive Beaumont Clay soil swells and contracts with humidity swings, frequently triggering slab leaks and pipe joint separations — the city averages some of the highest emergency plumbing call rates in Texas",
     "wh_local":"Houston's moderately hard water (150–200 mg/L) and high Gulf Coast humidity accelerate tank corrosion and anode rod wear, shortening water heater lifespan",
     "pipe_local":"Houston's highly expansive black clay (Beaumont Clay) shifts dramatically between wet and dry seasons, applying enormous cyclic stress to buried water and sewer pipes",
     "leak_local":"Houston's expansive clay soils and frequent heavy Gulf Coast rains create significant slab leak risk — Houston ranks among the top US cities for foundation movement and slab leak frequency",
     "sewer_local":"Houston's aging clay sewer infrastructure in older Heights and Montrose neighborhoods, combined with aggressive root growth in humid conditions, causes frequent sewer backups"},
    {"slug":"plumber-dallas-tx","city":"Dallas","state":"Texas","abbr":"TX","rate":"$80–$150",
     "drain_local":"Dallas's hard water (230+ mg/L) and famous black expansive clay soils create conditions for both mineral-based clogs and root intrusion into drain lines",
     "emergency_local":"Dallas's extreme temperature swings — from 110°F summers to sudden winter ice storms — are the leading cause of burst pipe emergencies, and the city's clay soils amplify foundation and pipe stress year-round",
     "wh_local":"Dallas's hard water (230+ mg/L) causes rapid sediment accumulation in water heater tanks, reducing efficiency and shortening lifespan — annual flushing is critical in the Dallas metro",
     "pipe_local":"Dallas's infamous black expansive clay (Houston Black) swells up to 30% when wet, applying enormous cyclic stress to underground pipes throughout the metroplex",
     "leak_local":"Dallas's highly expansive soils and extreme temperature swings make it one of the highest-risk US cities for foundation slab leaks — early detection is critical to preventing costly repairs",
     "sewer_local":"Dallas's expansive clay soils and large urban oak tree canopy are the primary causes of root intrusion into sewer lines across older Dallas neighborhoods"},
    {"slug":"plumber-austin-tx","city":"Austin","state":"Texas","abbr":"TX","rate":"$85–$155",
     "drain_local":"Austin's hard water with high calcium from the Edwards Aquifer causes significant mineral buildup in drains and fixtures — one of the top plumbing complaints in Central Texas",
     "emergency_local":"Austin's rapid growth, older central neighborhoods, and dramatic freeze events like Winter Storm Uri combine to create frequent plumbing emergencies across the metro area",
     "wh_local":"Austin's very hard Edwards Aquifer water causes heavy calcium buildup inside water heaters — tanks in Austin homes typically need descaling or replacement 20–30% sooner than the national average",
     "pipe_local":"Austin sits on the Balcones Fault Zone — shifting limestone bedrock combined with clay soils creates chronic underground pipe movement and joint stress throughout Central Austin",
     "leak_local":"Austin's limestone bedrock and clay soil combination creates significant slab leak risk — particularly in older Central Austin and Hyde Park homes on original concrete slab foundations",
     "sewer_local":"Austin's aging sewer infrastructure in central neighborhoods, combined with aggressive cedar and oak tree root growth, causes frequent sewer line blockages requiring professional service"},
    {"slug":"plumber-san-antonio-tx","city":"San Antonio","state":"Texas","abbr":"TX","rate":"$80–$145",
     "drain_local":"San Antonio's very hard Edwards Aquifer water (350+ mg/L) is among the hardest in Texas — severe mineral scale buildup in drains, pipes, and fixtures is the norm, not the exception",
     "emergency_local":"San Antonio's combination of scorching summer heat, occasional hard freezes, and aging infrastructure in historic neighborhoods creates frequent emergency plumbing situations year-round",
     "wh_local":"San Antonio has some of the hardest water in Texas at 350+ mg/L — Edwards Aquifer water rapidly scales water heater tanks, with many units requiring replacement years ahead of national averages",
     "pipe_local":"San Antonio's expansive clay soils and limestone karst geology stress both above-ground and buried pipes year-round with combined thermal and ground-movement cycles",
     "leak_local":"San Antonio's hard water, clay soils, and high foundation movement risk make the city one of Texas's highest-risk areas for both pipe corrosion leaks and slab foundation leaks",
     "sewer_local":"San Antonio's older neighborhoods feature aging clay sewer pipes that are highly susceptible to root intrusion from oak and pecan trees, plus joint separation from soil movement"},
    {"slug":"plumber-fort-worth-tx","city":"Fort Worth","state":"Texas","abbr":"TX","rate":"$80–$145",
     "drain_local":"Fort Worth's hard water and highly expansive Blackland Prairie clay soils contribute to both mineral scale buildup and root intrusion drain blockages throughout Tarrant County",
     "emergency_local":"Fort Worth's extreme North Texas temperature swings and the same highly expansive Blackland Prairie clay soils that plague Dallas drive high rates of burst pipes and slab leak emergencies",
     "wh_local":"Fort Worth's hard municipal water causes scale buildup in water heaters and premature anode rod failure — the Blackland Prairie water chemistry demands more frequent water heater maintenance",
     "pipe_local":"Fort Worth sits on the same highly expansive Blackland Prairie clay soils as Dallas — pipe joint separation and slab foundation movement are endemic issues requiring local plumbing expertise",
     "leak_local":"Fort Worth's black clay soils and temperature extremes put underground pipes and slabs under constant cyclic stress, creating high slab leak risk throughout Tarrant County",
     "sewer_local":"Fort Worth's clay soils and mature neighborhood tree canopy create significant root intrusion risk in aging clay sewer systems — especially in older Historic Southside and Ryan Place areas"},
    {"slug":"plumber-charlotte-nc","city":"Charlotte","state":"North Carolina","abbr":"NC","rate":"$85–$150",
     "drain_local":"Charlotte's red Piedmont clay soils support aggressive tree root growth that infiltrates drain lines, while high summer humidity accelerates grease buildup in kitchen drain systems",
     "emergency_local":"Charlotte's rapid growth puts pressure on aging infrastructure in older South End and Dilworth neighborhoods, while periodic January ice storms regularly cause burst pipe emergencies",
     "wh_local":"Charlotte's moderately hard water (100–150 mg/L) from Mountain Island Lake has a manageable scale buildup rate — but the city's humid summers accelerate external tank corrosion and fitting wear",
     "pipe_local":"Charlotte's red Piedmont clay soils swell when wet and crack when dry, applying cyclic stress to buried water and sewer pipes throughout the Mecklenburg County area",
     "leak_local":"Charlotte's red clay soils and older craftsman-era homes with original copper or galvanized pipes in neighborhoods like Plaza Midwood create moderate slab and pipe leak risk",
     "sewer_local":"Charlotte's mature tree canopy — with aggressive root systems from oaks, sweetgums, and Bradford pears — is the leading cause of sewer line root intrusion in older neighborhoods"},
    {"slug":"plumber-raleigh-nc","city":"Raleigh","state":"North Carolina","abbr":"NC","rate":"$85–$150",
     "drain_local":"Raleigh's sandy loam soils allow tree roots to spread widely and infiltrate drain lines, while rapid growth in new construction areas creates frequent debris-related blockages",
     "emergency_local":"Raleigh's rapid population growth has created plumbing emergencies in both aging Bungalow Belt neighborhoods and newly developed suburban areas where infrastructure is still settling",
     "wh_local":"Raleigh's relatively soft Falls Lake water keeps scale buildup low, but the city's humid summers accelerate external tank corrosion and water heater connection joint deterioration",
     "pipe_local":"Raleigh's sandy clay soils provide less pipe support than denser clay regions — combined with thermal expansion from hot summers and cold winters, pipe joint stress is significant",
     "leak_local":"Raleigh's high seasonal water table in low-lying areas creates external pipe corrosion risk, while older downtown neighborhoods still have original galvanized or cast iron pipe systems",
     "sewer_local":"Raleigh's rapid population growth has strained existing sewer capacity, and mature oaks and maples in older Five Points and Oakwood neighborhoods cause frequent root intrusion blockages"},
    {"slug":"plumber-greensboro-nc","city":"Greensboro","state":"North Carolina","abbr":"NC","rate":"$80–$145",
     "drain_local":"Greensboro's Piedmont red clay soils support vigorous root growth that targets drain lines, while many older downtown neighborhoods have aging clay pipe systems prone to blockage",
     "emergency_local":"Greensboro's position in the North Carolina Piedmont makes it vulnerable to winter ice storms — the region's leading cause of sudden burst pipe emergencies in residential plumbing",
     "wh_local":"Greensboro's moderately hard municipal water causes gradual scale buildup in water heater tanks — annual descaling maintenance extends equipment life significantly in Guilford County homes",
     "pipe_local":"Greensboro's clay soils and older housing stock — much of it built before 1980 — mean many homes still have original galvanized or cast iron pipes that are approaching end of life",
     "leak_local":"Greensboro's older housing stock and clay soils create moderate water leak risk — many homes in Fisher Park and Irving Park still have original plumbing systems installed 40–60 years ago",
     "sewer_local":"Greensboro's older clay sewer pipes and mature urban tree canopy make root intrusion into sewer lines one of the most common plumbing service calls in Guilford County"},
    {"slug":"plumber-nashville-tn","city":"Nashville","state":"Tennessee","abbr":"TN","rate":"$85–$155",
     "drain_local":"Nashville's limestone karst geology produces hard water (200+ mg/L from the Cumberland River basin) that accelerates mineral scale buildup inside drains and pipes throughout Davidson County",
     "emergency_local":"Nashville's rapid growth and mix of Victorian-era Germantown homes with new Brentwood construction creates diverse emergency plumbing challenges — from aging cast iron failures to new system defects",
     "wh_local":"Nashville's hard water from Cumberland River limestone creates significant calcium scale inside water heater tanks — affecting heating efficiency and dramatically shortening tank lifespan",
     "pipe_local":"Nashville sits on a limestone karst foundation where sinkholes and shifting bedrock create pipe movement and joint separation issues unique to Middle Tennessee geology",
     "leak_local":"Nashville's limestone karst geology and older craftsman-era homes in Germantown and East Nashville create a high-risk environment for hidden slab leaks and foundation movement",
     "sewer_local":"Nashville's rapid growth has strained older combined sewer systems, and aggressive oak and sycamore tree roots actively target sewer lines in established neighborhoods"},
    {"slug":"plumber-memphis-tn","city":"Memphis","state":"Tennessee","abbr":"TN","rate":"$75–$140",
     "drain_local":"Memphis's alluvial Mississippi Delta soils have high clay content and frequent high water tables that stress drain systems year-round and promote root intrusion in older neighborhoods",
     "emergency_local":"Memphis's older housing stock — much of it pre-1970s — combined with periodic severe winter ice storms creates frequent plumbing emergencies across Shelby County",
     "wh_local":"Memphis's moderately hard water and high seasonal humidity accelerate both internal sediment buildup and external tank corrosion in water heater units — especially in unconditioned garage spaces",
     "pipe_local":"Memphis's alluvial delta soils — highly plastic and prone to seasonal movement — combined with a high water table, creates challenging conditions for buried pipe stability throughout the metro",
     "leak_local":"Memphis's high groundwater table and clay alluvial soils create external pipe corrosion and hydrostatic pressure conditions that lead to frequent water leak issues in older neighborhoods",
     "sewer_local":"Memphis's aging sewer infrastructure, much of it original clay pipe from the early 20th century, is highly susceptible to root infiltration and joint failure requiring professional repair"},
    {"slug":"plumber-tampa-fl","city":"Tampa","state":"Florida","abbr":"FL","rate":"$80–$150",
     "drain_local":"Tampa's sandy subtropical soils and high humidity promote fast-growing root systems that readily invade drain lines, while the Floridan Aquifer's high mineral content accelerates pipe scale",
     "emergency_local":"Tampa's tropical storm season (June–November) and frequent heavy rainfalls create sudden flooding emergencies — and saltwater proximity from Tampa Bay accelerates pipe and fixture corrosion",
     "wh_local":"Tampa's hard Floridan Aquifer water (160–200 mg/L) combined with Florida's year-round high temperatures accelerate water heater sediment buildup and anode rod wear beyond national averages",
     "pipe_local":"Tampa's sandy soil provides minimal pipe bedding support, and proximity to Tampa Bay increases saltwater corrosion risk for buried metal pipes in coastal areas of Hillsborough County",
     "leak_local":"Tampa's sandy soils shift easily under pipe loads, and hard Floridan Aquifer water accelerates joint corrosion — creating significant leak risk in older concrete block homes throughout the area",
     "sewer_local":"Tampa's fast-growing tropical root systems and active limestone karst geography with documented sinkhole activity create unique sewer line challenges across Hillsborough County"},
    {"slug":"plumber-jacksonville-fl","city":"Jacksonville","state":"Florida","abbr":"FL","rate":"$80–$145",
     "drain_local":"Jacksonville's sandy subtropical soil and high humidity allow tree roots to spread aggressively toward drain moisture, while low coastal elevation creates drainage challenges in many neighborhoods",
     "emergency_local":"Jacksonville's frequent tropical storms, high tidal flooding risk along the St. Johns River, and humid subtropical climate create year-round plumbing emergency conditions throughout Duval County",
     "wh_local":"Jacksonville's humid subtropical climate and moderately hard Floridan Aquifer water create high water heater corrosion risk — units in unconditioned garages degrade significantly faster in Florida's heat",
     "pipe_local":"Jacksonville's sandy limestone soils shift under heavy rains and provide minimal pipe bedding support — combined with occasional tidal flooding, joint separation risk is elevated",
     "leak_local":"Jacksonville's sandy soils, tidal flooding risk, and aging pipe infrastructure in Riverside and Springfield neighborhoods create significant water leak risk throughout the city",
     "sewer_local":"Jacksonville's low coastal elevation and high water table make sewer backups a persistent risk — especially during tropical storm events when sewer systems are overwhelmed"},
    {"slug":"plumber-denver-co","city":"Denver","state":"Colorado","abbr":"CO","rate":"$90–$160",
     "drain_local":"Denver's moderately hard Rocky Mountain water (150–250 mg/L) causes mineral scale buildup in drains, while freeze-thaw cycles cause debris intrusion and pipe stress in unheated spaces",
     "emergency_local":"Denver's dramatic freeze-thaw cycles — with temperatures dropping below 0°F in winter then rapidly rising to 80°F+ in spring — make burst frozen pipes one of the most common plumbing emergencies in the Mile High City",
     "wh_local":"Denver's moderately hard mountain water and extreme seasonal temperature swings stress water heater tanks significantly — thermal expansion during winter cold snaps is the leading cause of sudden water heater failures",
     "pipe_local":"Denver's dramatic seasonal temperature swings cause significant thermal expansion and contraction in pipes — especially in exposed crawl spaces, garages, and uninsulated exterior walls common in older Denver homes",
     "leak_local":"Denver's freeze-thaw soil movement and aging pipe infrastructure in Capitol Hill, Washington Park, and Baker neighborhoods create significant hidden leak detection needs",
     "sewer_local":"Denver's mature urban tree canopy and seasonal ground freeze-thaw cycles put significant stress on older clay sewer pipes throughout the city's established neighborhoods"},
    {"slug":"plumber-atlanta-ga","city":"Atlanta","state":"Georgia","abbr":"GA","rate":"$85–$155",
     "drain_local":"Atlanta's Georgia red clay soils support aggressive root systems that readily invade drain lines, while high summer humidity accelerates grease buildup in kitchen drain systems year-round",
     "emergency_local":"Atlanta's periodic winter ice storms — the city sits in a marginal freeze zone where pipes are often poorly insulated — make ice-related burst pipes a seasonal emergency that catches many homeowners off guard",
     "wh_local":"Atlanta's moderately soft Chattahoochee River water (40–80 mg/L) keeps scale buildup low, but humid Georgia summers accelerate external tank and connection corrosion on water heater units",
     "pipe_local":"Atlanta's red Georgia clay soils expand dramatically when wet and contract sharply when dry — this cyclic soil movement is the leading cause of underground pipe joint failure throughout the metro area",
     "leak_local":"Atlanta's red clay soil movement and older Craftsman-era homes in Grant Park, Kirkwood, and Poncey-Highland with original galvanized pipes create significant water leak detection needs",
     "sewer_local":"Atlanta's red clay soils and dense urban tree canopy — with aggressive oak and pine root systems — make sewer line root intrusion the most common sewer problem in the Atlanta metro"},
    {"slug":"plumber-louisville-ky","city":"Louisville","state":"Kentucky","abbr":"KY","rate":"$80–$145",
     "drain_local":"Louisville's karst limestone bedrock produces moderately hard water (150–200 mg/L) that causes gradual mineral buildup in drains, while heavy Ohio River Valley rainfall promotes year-round root infiltration",
     "emergency_local":"Louisville's Ohio River Valley location exposes it to severe winter cold snaps that regularly freeze pipes in older homes — the city's high percentage of pre-1960 housing stock amplifies this risk",
     "wh_local":"Louisville's moderately hard Ohio River water and harsh winters that stress tank integrity combine to make water heater maintenance especially important for Jefferson County homeowners",
     "pipe_local":"Louisville's karst limestone geology — with documented sinkholes and underground voids in the area — combined with older housing stock in Germantown and Crescent Hill, creates pipe movement and joint stress challenges",
     "leak_local":"Louisville's karst geology creates ground instability that stresses buried pipes, while older neighborhoods still on original lead or galvanized pipes have significant leak detection needs",
     "sewer_local":"Louisville's aging combined sewer overflow (CSO) system and mature urban tree canopy make sewer backups and root intrusion among the most common plumbing service calls across Jefferson County"},
    {"slug":"plumber-las-vegas-nv","city":"Las Vegas","state":"Nevada","abbr":"NV","rate":"$90–$165",
     "drain_local":"Las Vegas has some of the hardest water in the United States at over 300 mg/L TDS from Lake Mead — mineral scale buildup in drains and fixtures is the most common plumbing issue in Clark County",
     "emergency_local":"Las Vegas's extreme summer heat regularly exceeding 115°F and near-freezing winter nights create dramatic pipe thermal stress — combined with the country's hardest water, sudden failures are common year-round",
     "wh_local":"Las Vegas has the hardest municipal water in the country at 300+ mg/L — sediment builds in water heater tanks at an extreme rate, requiring descaling every 6–12 months to maintain efficiency",
     "pipe_local":"Las Vegas's extreme desert heat — with ground temperatures reaching 140°F+ in summer — and extremely hard water cause accelerated mineral scaling and thermal stress throughout the home's water supply pipes",
     "leak_local":"Las Vegas's extremely hard water causes accelerated corrosion and pinhole leaks in copper pipes, while shifting desert soil under slabs creates significant slab leak risk throughout the Las Vegas Valley",
     "sewer_local":"Las Vegas's desert climate limits tree root risk but creates unique sewer issues: extreme mineral scale buildup inside sewer pipes and occasional sand intrusion in older Clark County sewer systems"},
    {"slug":"plumber-albuquerque-nm","city":"Albuquerque","state":"New Mexico","abbr":"NM","rate":"$80–$145",
     "drain_local":"Albuquerque's hard Rio Grande aquifer water and caliche-heavy desert soils promote both mineral scale in drains and pipe joint corrosion throughout Bernalillo County",
     "emergency_local":"Albuquerque's high desert climate brings both scorching summer days above 100°F and cold winter nights below 15°F — the intense freeze-thaw cycle is the leading cause of burst pipe emergencies in the metro area",
     "wh_local":"Albuquerque's hard Rio Grande aquifer water causes significant sediment scale in water heaters — the city's extreme seasonal temperature swings also stress tank integrity and connection fittings",
     "pipe_local":"Albuquerque's caliche (hardened calcium carbonate) soils and minor seismic activity from the Rio Grande Rift make underground pipe movement and joint failure common throughout the metro area",
     "leak_local":"Albuquerque's hard water causes pinhole leaks in copper pipes over time, while caliche desert soils prevent moisture from dispersing and can mask slow leak accumulation until damage is extensive",
     "sewer_local":"Albuquerque's adobe-era homes often have older clay or Orangeburg sewer pipes, while desert-adapted deep-rooted plants actively seek sewer moisture in the dry New Mexico climate"},
    {"slug":"plumber-oklahoma-city-ok","city":"Oklahoma City","state":"Oklahoma","abbr":"OK","rate":"$75–$140",
     "drain_local":"Oklahoma City sits on some of the most expansive clay soils in the United States — soil movement is a primary cause of drain line joint separation and pipe blockages throughout Oklahoma County",
     "emergency_local":"Oklahoma City's severe weather extremes — from ice storms and blizzards to 110°F heat — combined with the most expansive clay soils in the US, drive one of the highest per-capita emergency plumbing rates in the country",
     "wh_local":"Oklahoma City's hard Lake Hefner water (200+ mg/L) accelerates sediment buildup in water heater tanks, while severe winter temperature drops create thermal shock failure risk in standard tank units",
     "pipe_local":"Oklahoma City's Vanoss clay soils are among the most expansive in North America — pipe joint separation and slab foundation movement are endemic issues requiring specialized local plumbing expertise",
     "leak_local":"Oklahoma City's highly expansive clay soils create the highest slab foundation movement rate of any major US city — slab leaks are extremely common and require professional leak detection equipment",
     "sewer_local":"Oklahoma City's expansive clay soils cause sewer pipe joint separation as the ground heaves and contracts seasonally — sewer line repair and replacement is one of the most requested plumbing services in the area"},
    {"slug":"plumber-portland-or","city":"Portland","state":"Oregon","abbr":"OR","rate":"$90–$165",
     "drain_local":"Portland's very soft, mildly acidic Bull Run water dissolves residue from older pipes, and the Pacific Northwest's high rainfall means tree roots are always near moisture in drain lines",
     "emergency_local":"Portland's older housing stock — one of the highest percentages of pre-1950 homes in the Western US — combined with occasional heavy snowstorms, creates significant burst pipe and pipe failure risks throughout Multnomah County",
     "wh_local":"Portland's soft, slightly acidic Bull Run water is gentle on scale buildup but aggressively corrodes water heater anodes and tank linings — anode rod replacement every 3–4 years is critical to prevent tank failure",
     "pipe_local":"Portland's older housing stock and slightly acidic water create significant pipe corrosion risk — many homes in Irvington, Ladd's Addition, and Sellwood still have original lead, galvanized, or early copper pipes",
     "leak_local":"Portland's soft, slightly acidic water accelerates copper pipe corrosion and pinhole leaks over time — the city's high annual rainfall also means any hidden leak creates rapid moisture and mold damage",
     "sewer_local":"Portland's wet Pacific Northwest climate and dense urban tree canopy make root intrusion into sewer lines nearly universal in older homes — Douglas fir, cedar, and Japanese maple roots are frequent offenders"},
]

# ── Service data ───────────────────────────────────────────────────────────────
SERVICES = [
    {
        "slug": "drain-cleaning",
        "name": "Drain Cleaning",
        "local_key": "drain_local",
        "title_tpl": "Drain Cleaning {city}, {abbr} | Licensed Plumbers | Free Quote",
        "desc_tpl": "Expert drain cleaning in {city}, {abbr}. Hydro-jetting & clog removal by licensed, insured plumbers. Same-day service available. Free written quote. Call now!",
        "kw_tpl": "drain cleaning {city_lc}, drain clog {city_lc}, hydro jetting {city_lc}, clogged drain {city_lc}, plumber {city_lc}, drain cleaning cost {city_lc}",
        "og_title_tpl": "Drain Cleaning in {city}, {abbr} | Licensed & Same-Day Service",
        "schema_desc_tpl": "Expert drain cleaning and clog removal in {city}, {abbr}. Licensed & insured plumbers. Hydro-jetting and snake service available.",
        "intro_p_tpl": "Slow drains and stubborn clogs are among the most common plumbing problems for {city}, {state} homeowners. {local_note}. Our licensed drain cleaning team uses professional-grade hydro-jetting and snake equipment to fully clear blockages — not just push them further down the pipe. We serve all {city} neighborhoods with same-day service and free written quotes.",
        "faq_q4": "Can I use chemical drain cleaners instead of calling a plumber in {city}?",
        "faq_a4": "Chemical drain cleaners can corrode pipes — especially in older {city} homes with galvanized or cast iron pipe systems — and typically only clear the surface of a blockage, leading to recurring clogs. Professional hydro-jetting fully removes grease, scale, and root intrusions in a single service call. It's more effective, pipe-safe, and longer-lasting.",
        "faq_q5": "How often should drains be professionally cleaned in {city}?",
        "faq_a5": "Most {city} homeowners benefit from professional drain cleaning every 1–2 years as preventive maintenance. Homes with older pipes, mature trees in the yard, or local water quality challenges may need service more frequently. Kitchen drains handling grease typically benefit from annual cleaning to prevent slow drain buildup.",
    },
    {
        "slug": "emergency-plumbing",
        "name": "Emergency Plumbing",
        "local_key": "emergency_local",
        "title_tpl": "24/7 Emergency Plumber {city}, {abbr} | Call Now | Free Quote",
        "desc_tpl": "24/7 emergency plumbing in {city}, {abbr}. Licensed & insured, 1–2 hour response. Burst pipes, flooding & slab leaks handled fast. Call now — free quote!",
        "kw_tpl": "emergency plumber {city_lc}, 24/7 plumber {city_lc}, burst pipe {city_lc}, plumbing emergency {city_lc}, emergency plumbing cost {city_lc}, plumber near me {city_lc}",
        "og_title_tpl": "24/7 Emergency Plumber in {city}, {abbr} | Fast 1–2 Hour Response",
        "schema_desc_tpl": "24/7 emergency plumbing repair in {city}, {abbr}. Licensed & insured. 1–2 hour response for burst pipes, flooding, and slab leaks.",
        "intro_p_tpl": "When a plumbing emergency strikes your {city} home, every minute counts. {local_note}. Our licensed 24/7 emergency plumbing team responds within 1–2 hours anywhere in {city}, day or night, 365 days a year — including holidays. We handle burst pipes, slab leaks, flooding, sewage backups, and all critical plumbing failures with a free written quote before any work begins.",
        "faq_q4": "What counts as a plumbing emergency in {city}?",
        "faq_a4": "A plumbing emergency in {city} includes: burst or frozen pipes, sewage backing up into your home, water flooding from a broken pipe or fixture, loss of all water service, a water heater failure causing flooding, or a suspected gas line leak. If the issue risks structural water damage or makes your home unsafe to occupy, call our 24/7 emergency line immediately — don't wait.",
        "faq_q5": "Will homeowner's insurance cover emergency plumbing repairs in {city}?",
        "faq_a5": "Standard homeowner's insurance in {city} typically covers sudden and accidental water damage — such as a burst pipe — but not gradual leaks or deferred maintenance issues. Document all damage with photos immediately, contact your insurance provider, and request a detailed written estimate. Our team works with all major insurance carriers and can provide the documentation needed for your claim.",
    },
    {
        "slug": "water-heater-repair",
        "name": "Water Heater Repair",
        "local_key": "wh_local",
        "title_tpl": "Water Heater Repair {city}, {abbr} | Same-Day Service | Free Quote",
        "desc_tpl": "Water heater repair & replacement in {city}, {abbr}. Same-day service by licensed plumbers. Gas, electric & tankless units. Prevent cold showers. Free quote. Call now!",
        "kw_tpl": "water heater repair {city_lc}, water heater replacement {city_lc}, tankless water heater {city_lc}, hot water heater {city_lc}, plumber {city_lc}, water heater cost {city_lc}",
        "og_title_tpl": "Water Heater Repair in {city}, {abbr} | Same-Day Service",
        "schema_desc_tpl": "Professional water heater repair and replacement in {city}, {abbr}. Licensed & insured plumbers. Same-day service for gas, electric & tankless units.",
        "intro_p_tpl": "A failing water heater disrupts your entire household — and {city} homeowners face specific local challenges. {local_note}. Our licensed water heater technicians provide same-day repair and replacement throughout {city}, {state}, working on all major brands and types — traditional tank, tankless, gas, and electric. Every job includes a free written quote and upfront pricing before work begins.",
        "faq_q4": "Should I repair or replace my water heater in {city}?",
        "faq_a4": "The standard rule for {city} homeowners: if your water heater is over 10 years old and needs a repair costing more than 50% of a new unit, replacement is the better long-term investment. Newer units are 20–35% more energy-efficient and better designed to handle local water quality conditions. Our technicians give an honest, no-pressure repair vs. replace recommendation on every service call.",
        "faq_q5": "Is a tankless water heater worth the upgrade in {city}?",
        "faq_a5": "Tankless water heaters are an excellent choice for most {city} homes — they're 24–34% more energy-efficient than traditional tank units and provide endless hot water on demand. The typical payback period is 5–8 years through energy savings. Our team can recommend the correctly sized unit for your household's hot water demand and guide you through any available rebates.",
    },
    {
        "slug": "pipe-repair",
        "name": "Pipe Repair",
        "local_key": "pipe_local",
        "title_tpl": "Pipe Repair {city}, {abbr} | Licensed Plumbers | Free Quote",
        "desc_tpl": "Expert pipe repair in {city}, {abbr}. Burst pipes, leaking pipes & repiping by licensed, insured plumbers. Same-day service available. Free written quote. Call now!",
        "kw_tpl": "pipe repair {city_lc}, burst pipe {city_lc}, leaking pipe {city_lc}, repiping {city_lc}, plumber {city_lc}, pipe replacement {city_lc}",
        "og_title_tpl": "Pipe Repair in {city}, {abbr} | Licensed & Same-Day Service",
        "schema_desc_tpl": "Expert pipe repair and repiping services in {city}, {abbr}. Licensed & insured plumbers. Burst pipes, leaking pipes, and full repiping.",
        "intro_p_tpl": "Pipe problems in {city} range from pinhole leaks to complete burst failures — and they get worse fast. {local_note}. Our licensed pipe repair specialists serve all {city} neighborhoods with same-day service for urgent repairs and scheduled repiping projects. We work on all pipe materials — copper, PVC, PEX, CPVC, galvanized steel, and cast iron — with free written estimates and upfront pricing on every job.",
        "faq_q4": "When should I repipe my {city} home instead of repairing individual pipes?",
        "faq_a4": "Repiping your {city} home is the right choice when: pipes are over 50 years old, you've had more than 2–3 separate leaks in a single year, your water has a discolored or metallic taste, or your home still has original galvanized steel or lead pipes. A full repipe with modern PEX or copper eliminates ongoing repair costs and improves water quality immediately.",
        "faq_q5": "What pipe material is best for homes in {city}?",
        "faq_a5": "For new installations and repiping in {city}, PEX tubing is the most popular choice — it's flexible (handles ground movement well), resistant to freeze damage, corrosion-resistant, and works well with a wide range of water quality conditions. Cross-linked PEX-A is our top recommendation for water supply lines. For drain and vent lines, Schedule 40 PVC or ABS provides reliable, long-lasting performance.",
    },
    {
        "slug": "leak-detection",
        "name": "Leak Detection",
        "local_key": "leak_local",
        "title_tpl": "Leak Detection {city}, {abbr} | Find Hidden Water Leaks | Free Quote",
        "desc_tpl": "Professional leak detection in {city}, {abbr}. Advanced equipment finds slab leaks, pipe leaks & hidden water damage fast. Licensed & insured. Free quote. Call now!",
        "kw_tpl": "leak detection {city_lc}, water leak {city_lc}, hidden leak {city_lc}, slab leak {city_lc}, plumber {city_lc}, water leak detection cost {city_lc}",
        "og_title_tpl": "Leak Detection in {city}, {abbr} | Slab & Pipe Leaks Found Fast",
        "schema_desc_tpl": "Professional leak detection in {city}, {abbr}. Licensed & insured plumbers using acoustic and electronic equipment to locate all types of hidden water leaks.",
        "intro_p_tpl": "Hidden water leaks in {city} homes can cause thousands of dollars in damage before they're visible. {local_note}. Our licensed leak detection specialists use acoustic listening devices, thermal imaging cameras, and electronic pressure testing to locate leaks precisely — including slab leaks, underground pipe leaks, and in-wall leaks — without unnecessary digging or demolition. We serve all {city} neighborhoods.",
        "faq_q4": "How do I know if I have a hidden water leak in my {city} home?",
        "faq_a4": "Warning signs of a hidden water leak in your {city} home include: a water bill more than 20% higher than normal with no explanation, the sound of running water when all fixtures are off, warm or wet spots on floors or walls, low water pressure on a specific line, wet patches in your yard with no irrigation, or your water meter moving when everything is closed. If you notice any of these signs, call us for a professional leak inspection.",
        "faq_q5": "How much does professional leak detection cost in {city}?",
        "faq_a5": "Professional leak detection in {city} typically costs $150–$450 depending on the type of leak and detection method required. Slab leak detection using acoustic equipment and thermal imaging is at the higher end of that range. The investment almost always saves money — catching a slab leak early can prevent $5,000–$15,000 in concrete, flooring, and water damage repairs. We provide free written quotes before starting any detection work.",
    },
    {
        "slug": "sewer-line-repair",
        "name": "Sewer Line Repair",
        "local_key": "sewer_local",
        "title_tpl": "Sewer Line Repair {city}, {abbr} | Licensed Plumbers | Free Quote",
        "desc_tpl": "Expert sewer line repair in {city}, {abbr}. Camera inspection, trenchless options available. Licensed & insured. Prevent sewage backups. Free quote. Call now!",
        "kw_tpl": "sewer line repair {city_lc}, sewer repair {city_lc}, sewer replacement {city_lc}, trenchless sewer {city_lc}, plumber {city_lc}, sewer line cost {city_lc}",
        "og_title_tpl": "Sewer Line Repair in {city}, {abbr} | Camera Inspection & Trenchless",
        "schema_desc_tpl": "Expert sewer line repair and replacement in {city}, {abbr}. Licensed & insured plumbers. Video camera inspection, trenchless pipe lining, and full sewer replacement.",
        "intro_p_tpl": "Sewer line problems in {city} range from root intrusion blockages to complete pipe collapse — and the signs aren't always obvious until damage is severe. {local_note}. Our licensed sewer line specialists use video camera inspection to diagnose your exact issue before recommending the right repair — whether hydro-jetting, trenchless pipe lining, or full sewer line replacement. We serve all {city} neighborhoods with free written estimates and same-day emergency response.",
        "faq_q4": "What's the difference between sewer line repair and full replacement in {city}?",
        "faq_a4": "Sewer line repair in {city} addresses a specific problem — such as a root intrusion blockage, a cracked pipe section, or a joint separation — typically covering a 1–5 foot length. Full replacement is recommended when a significant length of pipe is deteriorated, collapsed, or made from outdated materials like clay or Orangeburg. Camera inspection lets us diagnose precisely and recommend the most cost-effective solution for your situation.",
        "faq_q5": "Is trenchless sewer repair available in {city}, and is it worth it?",
        "faq_a5": "Yes — trenchless sewer repair options including pipe lining (CIPP) and pipe bursting are available throughout {city}. Trenchless methods avoid excavating your yard, driveway, or landscaping, and typically cost 20–40% less than traditional open-cut excavation when the pipe condition qualifies. After video camera inspection, we'll tell you clearly whether your {city} sewer line qualifies for trenchless repair and what it will cost.",
    },
]

# ── Helpers ────────────────────────────────────────────────────────────────────

def faq_item_html(q, a):
    return f'\n<div class="faq-item"><div class="faq-q">{q} <span>▼</span></div><div class="faq-a">{a}</div></div>'

def faq_item_schema(q, a):
    return f''',
    {{
      "@type": "Question",
      "name": "{q}",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "{a}"
      }}
    }}'''

def find_faq_list_close(html):
    """Return index of the </div> that closes the first <div class="faq-list">."""
    start = html.find('<div class="faq-list">')
    if start == -1:
        return -1
    depth = 0
    i = start
    while i < len(html):
        if html[i:i+4] == '<div':
            depth += 1
            i += 4
        elif html[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                return i
            i += 6
        else:
            i += 1
    return -1

def update(city, svc):
    path = os.path.join(BASE, city['slug'], svc['slug'], 'index.html')
    if not os.path.exists(path):
        return 'SKIP'

    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    c  = city['city']
    st = city['state']
    ab = city['abbr']
    cl = c.lower()
    local = city[svc['local_key']]

    # ── Substitution values ──
    title     = svc['title_tpl'].format(city=c, state=st, abbr=ab)
    desc      = svc['desc_tpl'].format(city=c, state=st, abbr=ab)
    kw        = svc['kw_tpl'].format(city=c, state=st, abbr=ab, city_lc=cl)
    og_title  = svc['og_title_tpl'].format(city=c, state=st, abbr=ab)
    sd        = svc['schema_desc_tpl'].format(city=c, state=st, abbr=ab)
    intro_p   = svc['intro_p_tpl'].format(city=c, state=st, abbr=ab, local_note=local)
    faq_q4    = svc['faq_q4'].format(city=c, state=st, abbr=ab)
    faq_a4    = svc['faq_a4'].format(city=c, state=st, abbr=ab)
    faq_q5    = svc['faq_q5'].format(city=c, state=st, abbr=ab)
    faq_a5    = svc['faq_a5'].format(city=c, state=st, abbr=ab)

    # 1. Title
    html = re.sub(r'<title>[^<]+</title>', f'<title>{title}</title>', html)

    # 2. Meta description
    html = re.sub(r'<meta name="description" content="[^"]+"',
                  f'<meta name="description" content="{desc}"', html)

    # 3. Keywords
    html = re.sub(r'<meta name="keywords" content="[^"]+"',
                  f'<meta name="keywords" content="{kw}"', html)

    # 4. OG title
    html = re.sub(r'<meta property="og:title" content="[^"]+"',
                  f'<meta property="og:title" content="{og_title}"', html)

    # 5. OG description
    html = re.sub(r'<meta property="og:description" content="[^"]+"',
                  f'<meta property="og:description" content="{desc}"', html)

    # 6. Twitter title
    html = re.sub(r'<meta name="twitter:title" content="[^"]+"',
                  f'<meta name="twitter:title" content="{og_title}"', html)

    # 7. Twitter description
    html = re.sub(r'<meta name="twitter:description" content="[^"]+"',
                  f'<meta name="twitter:description" content="{desc}"', html)

    # 8. Schema LocalBusiness/Service description (first "description" field in JSON-LD)
    html = re.sub(r'"description": "Professional professional[^"]*"',
                  f'"description": "{sd}"', html)
    # Also fix plain "Professional X" without double word (for pages that don't have the bug)
    html = re.sub(
        r'("description": ")[^"]*(?:repair|cleaning|replacement|detection)[^"]*(?:Licensed|insured)[^"]*(")',
        f'\\1{sd}\\2', html, count=1
    )

    # 9. Brand link → PlumbersInUSA.com linking to homepage
    html = re.sub(
        r'<a class="brand" href="https://plumbersinusa\.com/[^"]+" aria-label="[^"]+">Plumbing Repair</a>',
        '<a class="brand" href="https://plumbersinusa.com/" aria-label="PlumbersInUSA.com - Home">PlumbersInUSA.com</a>',
        html
    )

    # 10. Intro paragraph (first <p> after section-sub in intro section)
    html = re.sub(
        r'(class="section-sub">[^<]+</p>\s*)<p>[^<]+</p>(<br>|\s*<br\s*/>)',
        rf'\1<p>{intro_p}</p>\2',
        html, count=1
    )

    # 11. Footer first column h4 and desc
    html = re.sub(
        r'<h4>Plumbing Repair in ' + re.escape(c) + r', ' + re.escape(ab) + r'</h4>',
        f'<h4>{svc["name"]} in {c}, {ab}</h4>',
        html
    )
    html = re.sub(
        r'Licensed &amp; insured plumbing repair professionals serving ' + re.escape(c) + r', ' + re.escape(st) + r' and surrounding areas\. Available 24/7\.',
        f'Licensed &amp; insured {svc["name"].lower()} and plumbing professionals serving {c}, {st} and surrounding areas. Available 24/7.',
        html
    )

    # 12. Footer copyright
    html = re.sub(
        r'&copy; 2026 Plumbing Repair Services in ' + re.escape(c) + r', ' + re.escape(st) + r'\. All rights reserved\. \| Licensed &amp; Insured',
        f'&copy; 2026 PlumbersInUSA.com | Licensed &amp; Insured Plumbers in {c}, {st}',
        html
    )

    # 13. Add 2 FAQ items to HTML faq-list
    faq_html_new = faq_item_html(faq_q4, faq_a4) + faq_item_html(faq_q5, faq_a5)
    close_idx = find_faq_list_close(html)
    if close_idx != -1:
        html = html[:close_idx] + faq_html_new + html[close_idx:]

    # 14. Add 2 FAQ items to FAQPage JSON-LD schema
    faq_schema_addition = faq_item_schema(faq_q4, faq_a4) + faq_item_schema(faq_q5, faq_a5)
    html = re.sub(
        r'("@type":\s*"FAQPage",\s*"mainEntity":\s*\[)(.*?)(\]\s*\})',
        lambda m: m.group(1) + m.group(2) + faq_schema_addition + '\n  ' + m.group(3),
        html, flags=re.DOTALL
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return 'OK'

# ── Run ────────────────────────────────────────────────────────────────────────
print(f"Updating {len(CITIES) * len(SERVICES)} service pages...")
ok = skip = err = 0
for city in CITIES:
    for svc in SERVICES:
        result = update(city, svc)
        if result == 'OK':
            ok += 1
        elif result == 'SKIP':
            skip += 1
            print(f"  SKIP  {city['slug']}/{svc['slug']}")
        else:
            err += 1
            print(f"  ERR   {city['slug']}/{svc['slug']}: {result}")

print(f"Done. OK={ok}  SKIP={skip}  ERR={err}")
