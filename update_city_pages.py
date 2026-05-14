import os, re, json

BASE = r"C:\Users\Dhruvisha\Desktop\plumbing-site"

def faq_html(items):
    out = []
    for q, a in items:
        out.append(f'      <div class="faq-item">\n        <div class="faq-q">{q} <span>&#9660;</span></div>\n        <div class="faq-a">{a}</div>\n      </div>')
    return "\n".join(out)

def faq_schema(items):
    return json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in items]}, indent=2)

CITIES = [
  {
    "dir":"plumber-phoenix-az","city":"Phoenix","state":"AZ","state_full":"Arizona",
    "title":"Licensed Plumbers in Phoenix, AZ | 24/7 Emergency Service | Free Estimates",
    "desc":"Find trusted licensed plumbers in Phoenix, AZ. Emergency plumbing, drain cleaning, water heater repair & more. 24/7 service, same-day availability. Free estimates.",
    "kw":"plumbers in phoenix, phoenix plumber, emergency plumbing phoenix az, drain cleaning phoenix, water heater repair phoenix, plumber near me phoenix",
    "h1":"Trusted Plumbers in Phoenix, AZ",
    "hero_sub":"Fast, reliable plumbing services for homes and businesses across Phoenix, Arizona. Connect with licensed local plumbers for emergency repairs, drain cleaning, water heater services, leak detection, and more.",
    "intro_h2":"Professional Plumbing Services in Phoenix, Arizona",
    "intro_sub":"Your trusted local plumbing experts serving Phoenix and the surrounding metro area",
    "intro_p1":"Phoenix's desert climate and hard water create unique plumbing challenges — from mineral buildup in pipes and water heater wear to hot-season pressure spikes and cracked supply lines. Whether you're in Scottsdale, Tempe, Mesa, Glendale, or Downtown Phoenix, PlumbersInUSA.com connects you with licensed, insured plumbing professionals who know the local systems, codes, and conditions.",
    "services_h2":"Our Plumbing Services in Phoenix, AZ",
    "services_sub":"Complete plumbing solutions for Phoenix homes and businesses",
    "cta_h2":"Need a Licensed Plumber in Phoenix, AZ?",
    "cta_sub":"Connect with trusted local plumbers in Phoenix for residential and commercial plumbing needs. Free estimates, same-day service available.",
    "schema_desc":"Connect with trusted licensed plumbers in Phoenix, AZ for emergency plumbing, drain cleaning, water heater repair, leak detection, and more.",
    "faq":[
      ("How much do plumbers charge per hour in Phoenix?","Plumbing rates in Phoenix, AZ typically range from $85 to $150 per hour depending on the service type and time of day. Emergency plumbing may cost more. We always provide a free written estimate before work begins."),
      ("What is the best plumbing company in the Phoenix area?","The best plumber depends on your specific need. PlumbersInUSA.com connects you with multiple licensed, insured, and highly-rated plumbing professionals throughout Phoenix so you can compare and choose."),
      ("Do plumbers in Phoenix offer same-day service?","Yes. Most licensed plumbers in Phoenix offer same-day and 24/7 emergency service for urgent repairs including burst pipes, drain blockages, and water heater failures."),
      ("Are Phoenix plumbers licensed in Arizona?","Yes. All plumbing professionals connected through PlumbersInUSA.com serving Phoenix are fully licensed, bonded, and insured in the state of Arizona as required by state law."),
      ("What areas of Phoenix do local plumbers serve?","Local plumbers serve all Phoenix neighborhoods including Scottsdale, Tempe, Mesa, Chandler, Glendale, Peoria, Gilbert, Paradise Valley, Avondale, and Surprise."),
    ]
  },
  {
    "dir":"plumber-houston-tx","city":"Houston","state":"TX","state_full":"Texas",
    "title":"Licensed Plumbers in Houston, TX | Same-Day Service | Free Estimates",
    "desc":"Find trusted licensed plumbers in Houston, TX. Emergency plumbing, drain cleaning, water heater repair & more. 24/7 service, same-day availability. Free estimates.",
    "kw":"plumbers in houston, houston plumber, emergency plumbing houston tx, drain cleaning houston, water heater repair houston, plumber near me houston",
    "h1":"Trusted Plumbers in Houston, TX",
    "hero_sub":"Fast, reliable plumbing services for homes and businesses across Houston, Texas. Connect with licensed local plumbers for emergency repairs, drain cleaning, water heater services, and more.",
    "intro_h2":"Professional Plumbing Services in Houston, Texas",
    "intro_sub":"Your trusted local plumbing experts serving Houston and the surrounding metro area",
    "intro_p1":"Houston's heavy rainfall, clay soil, and Gulf Coast humidity create constant plumbing demands — from storm-related flooding and foundation shifts to root intrusions in sewer lines and water heater corrosion. Whether you're in Katy, Sugar Land, The Woodlands, Pearland, or Midtown Houston, PlumbersInUSA.com connects you with licensed, insured plumbing professionals who understand Houston's unique challenges.",
    "services_h2":"Our Plumbing Services in Houston, TX",
    "services_sub":"Complete plumbing solutions for Houston homes and businesses",
    "cta_h2":"Need a Licensed Plumber in Houston, TX?",
    "cta_sub":"Connect with trusted local plumbers in Houston for residential and commercial plumbing needs. Free estimates, same-day service available.",
    "schema_desc":"Connect with trusted licensed plumbers in Houston, TX for emergency plumbing, drain cleaning, water heater repair, leak detection, and more.",
    "faq":[
      ("How much do plumbers charge per hour in Houston?","Plumbing rates in Houston, TX typically range from $80 to $145 per hour depending on the service and time of day. Emergency services may cost more. Free written estimates are always provided before work begins."),
      ("What is the best plumbing company in Houston?","PlumbersInUSA.com connects you with multiple licensed, insured, and highly-rated plumbing professionals in Houston so you can compare options and choose the best fit for your needs."),
      ("Do Houston plumbers offer 24/7 emergency service?","Yes. Most licensed plumbers in Houston offer 24/7 emergency service for urgent issues including burst pipes, sewer backups, flooding, and water heater failures."),
      ("Are plumbers in Houston licensed in Texas?","Yes. All plumbing professionals connected through PlumbersInUSA.com serving Houston are fully licensed, bonded, and insured in the state of Texas."),
      ("What areas of Houston do local plumbers serve?","Local plumbers serve all Houston neighborhoods including Katy, Sugar Land, The Woodlands, Pearland, Spring, Cypress, Clear Lake, Midtown, Montrose, and River Oaks."),
    ]
  },
  {
    "dir":"plumber-dallas-tx","city":"Dallas","state":"TX","state_full":"Texas",
    "title":"Licensed Plumbers in Dallas, TX | Same-Day Service | Free Estimates",
    "desc":"Find trusted licensed plumbers in Dallas, TX. Emergency plumbing, drain cleaning, water heater repair & more. 24/7 service, same-day availability. Free estimates.",
    "kw":"plumbers in dallas, dallas plumber, emergency plumbing dallas tx, drain cleaning dallas, water heater repair dallas, plumber near me dallas",
    "h1":"Trusted Plumbers in Dallas, TX",
    "hero_sub":"Fast, reliable plumbing services for homes and businesses across Dallas, Texas. Connect with licensed local plumbers for emergency repairs, drain cleaning, water heater services, and more.",
    "intro_h2":"Professional Plumbing Services in Dallas, Texas",
    "intro_sub":"Your trusted local plumbing experts serving Dallas and the surrounding metro area",
    "intro_p1":"Dallas's expansive clay soil and extreme temperature swings — from scorching summers to occasional hard freezes — put constant stress on pipes, joints, and water lines. Foundation movement is a common cause of hidden leaks in Dallas homes. PlumbersInUSA.com connects you with licensed, insured plumbing professionals across Dallas, Plano, Irving, Frisco, Garland, and the full DFW metro.",
    "services_h2":"Our Plumbing Services in Dallas, TX",
    "services_sub":"Complete plumbing solutions for Dallas homes and businesses",
    "cta_h2":"Need a Licensed Plumber in Dallas, TX?",
    "cta_sub":"Connect with trusted local plumbers in Dallas for residential and commercial plumbing needs. Free estimates, same-day service available.",
    "schema_desc":"Connect with trusted licensed plumbers in Dallas, TX for emergency plumbing, drain cleaning, water heater repair, leak detection, and more.",
    "faq":[
      ("How much do plumbers charge per hour in Dallas?","Plumbing rates in Dallas, TX typically range from $85 to $150 per hour. Emergency and after-hours services may cost more. Free written estimates are always provided before work begins."),
      ("What is the best plumbing company in Dallas?","PlumbersInUSA.com connects you with multiple licensed, insured, and top-rated plumbing professionals across Dallas so you can compare options and choose the best fit."),
      ("Do Dallas plumbers offer same-day service?","Yes. Most licensed plumbers in Dallas offer same-day and 24/7 emergency service for issues like burst pipes, sewer backups, drain clogs, and water heater failures."),
      ("Are Dallas plumbers licensed in Texas?","Yes. All plumbing professionals connected through PlumbersInUSA.com serving Dallas are fully licensed, bonded, and insured in the state of Texas."),
      ("What areas of Dallas do local plumbers serve?","Local plumbers serve all Dallas neighborhoods including Plano, Irving, Frisco, Garland, Carrollton, Mesquite, Richardson, Highland Park, Uptown, and Deep Ellum."),
    ]
  },
  {
    "dir":"plumber-austin-tx","city":"Austin","state":"TX","state_full":"Texas",
    "title":"Licensed Plumbers in Austin, TX | 24/7 Emergency Service | Free Estimates",
    "desc":"Find trusted licensed plumbers in Austin, TX. Emergency plumbing, drain cleaning, water heater repair & more. 24/7 service, same-day availability. Free estimates.",
    "kw":"plumbers in austin, austin plumber, emergency plumbing austin tx, drain cleaning austin, water heater repair austin, plumber near me austin",
    "h1":"Trusted Plumbers in Austin, TX",
    "hero_sub":"Fast, reliable plumbing services for homes and businesses across Austin, Texas. Connect with licensed local plumbers for emergency repairs, drain cleaning, water heater services, and more.",
    "intro_h2":"Professional Plumbing Services in Austin, Texas",
    "intro_sub":"Your trusted local plumbing experts serving Austin and the surrounding metro area",
    "intro_p1":"Austin's hard water, limestone bedrock, and rapid population growth create specific plumbing challenges — from mineral scale buildup in pipes and water heaters to foundation movement causing hidden leaks in older homes. Whether you're in Round Rock, Cedar Park, Georgetown, South Congress, or East Austin, PlumbersInUSA.com connects you with licensed, insured plumbing professionals who know Austin's local systems.",
    "services_h2":"Our Plumbing Services in Austin, TX",
    "services_sub":"Complete plumbing solutions for Austin homes and businesses",
    "cta_h2":"Need a Licensed Plumber in Austin, TX?",
    "cta_sub":"Connect with trusted local plumbers in Austin for residential and commercial plumbing needs. Free estimates, same-day service available.",
    "schema_desc":"Connect with trusted licensed plumbers in Austin, TX for emergency plumbing, drain cleaning, water heater repair, leak detection, and more.",
    "faq":[
      ("How much do plumbers charge per hour in Austin?","Plumbing rates in Austin, TX typically range from $90 to $155 per hour. Emergency and after-hours services may cost more. Free written estimates are always provided before work begins."),
      ("What is the best plumbing company in Austin?","PlumbersInUSA.com connects you with multiple licensed, insured, and highly-rated plumbing professionals in Austin so you can compare options and find the right fit."),
      ("Do Austin plumbers offer same-day service?","Yes. Most licensed plumbers in Austin offer same-day and 24/7 emergency service for urgent plumbing issues including burst pipes, clogged drains, and water heater failures."),
      ("Are Austin plumbers licensed in Texas?","Yes. All plumbing professionals connected through PlumbersInUSA.com serving Austin are fully licensed, bonded, and insured in the state of Texas."),
      ("What areas of Austin do local plumbers serve?","Local plumbers serve all Austin neighborhoods including Round Rock, Cedar Park, Georgetown, Pflugerville, Lakeway, Bee Cave, South Austin, East Austin, and Westlake."),
    ]
  },
  {
    "dir":"plumber-san-antonio-tx","city":"San Antonio","state":"TX","state_full":"Texas",
    "title":"Licensed Plumbers in San Antonio, TX | 24/7 Emergency | Free Estimates",
    "desc":"Find trusted licensed plumbers in San Antonio, TX. Emergency plumbing, drain cleaning, water heater repair & more. 24/7 service, same-day availability. Free estimates.",
    "kw":"plumbers in san antonio, san antonio plumber, emergency plumbing san antonio tx, drain cleaning san antonio, water heater repair san antonio, plumber near me san antonio",
    "h1":"Trusted Plumbers in San Antonio, TX",
    "hero_sub":"Fast, reliable plumbing services for homes and businesses across San Antonio, Texas. Connect with licensed local plumbers for emergency repairs, drain cleaning, water heater services, and more.",
    "intro_h2":"Professional Plumbing Services in San Antonio, Texas",
    "intro_sub":"Your trusted local plumbing experts serving San Antonio and the surrounding metro area",
    "intro_p1":"San Antonio's hard water, caliche soil, and intense summer heat stress pipes, water heaters, and fixtures year-round. Hard water mineral deposits are a leading cause of premature water heater failure and reduced pipe flow in San Antonio homes. PlumbersInUSA.com connects you with licensed, insured plumbing professionals serving Stone Oak, Alamo Heights, New Braunfels, Schertz, Helotes, and the full metro area.",
    "services_h2":"Our Plumbing Services in San Antonio, TX",
    "services_sub":"Complete plumbing solutions for San Antonio homes and businesses",
    "cta_h2":"Need a Licensed Plumber in San Antonio, TX?",
    "cta_sub":"Connect with trusted local plumbers in San Antonio for residential and commercial plumbing needs. Free estimates, same-day service available.",
    "schema_desc":"Connect with trusted licensed plumbers in San Antonio, TX for emergency plumbing, drain cleaning, water heater repair, leak detection, and more.",
    "faq":[
      ("How much do plumbers charge per hour in San Antonio?","Plumbing rates in San Antonio, TX typically range from $75 to $135 per hour. Emergency services may cost more. Free written estimates are always provided before work begins."),
      ("What is the best plumbing company in San Antonio?","PlumbersInUSA.com connects you with multiple licensed, insured, and top-rated plumbing professionals in San Antonio so you can compare and choose the best option."),
      ("Do San Antonio plumbers offer 24/7 emergency service?","Yes. Most licensed plumbers in San Antonio offer 24/7 emergency service for burst pipes, sewer backups, water heater failures, and other urgent plumbing issues."),
      ("Are San Antonio plumbers licensed in Texas?","Yes. All plumbing professionals connected through PlumbersInUSA.com serving San Antonio are fully licensed, bonded, and insured in the state of Texas."),
      ("What areas of San Antonio do local plumbers serve?","Local plumbers serve all San Antonio neighborhoods including Stone Oak, Alamo Heights, New Braunfels, Schertz, Helotes, Leon Valley, Converse, Live Oak, and Universal City."),
    ]
  },
  {
    "dir":"plumber-fort-worth-tx","city":"Fort Worth","state":"TX","state_full":"Texas",
    "title":"Licensed Plumbers in Fort Worth, TX | 24/7 Emergency | Free Estimates",
    "desc":"Find trusted licensed plumbers in Fort Worth, TX. Emergency plumbing, drain cleaning, water heater repair & more. 24/7 service, same-day availability. Free estimates.",
    "kw":"plumbers in fort worth, fort worth plumber, emergency plumbing fort worth tx, drain cleaning fort worth, water heater repair fort worth, plumber near me fort worth",
    "h1":"Trusted Plumbers in Fort Worth, TX",
    "hero_sub":"Fast, reliable plumbing services for homes and businesses across Fort Worth, Texas. Connect with licensed local plumbers for emergency repairs, drain cleaning, water heater services, and more.",
    "intro_h2":"Professional Plumbing Services in Fort Worth, Texas",
    "intro_sub":"Your trusted local plumbing experts serving Fort Worth and the surrounding metro area",
    "intro_p1":"Fort Worth's clay soil expands and contracts with rain and drought cycles, putting pressure on buried pipes and slab foundations that can lead to hidden leaks and sewer shifts. Freeze events — while less frequent than in northern states — can cause significant pipe bursts. PlumbersInUSA.com connects you with licensed, insured plumbing professionals serving Arlington, Keller, Grapevine, Southlake, North Richland Hills, and the full Fort Worth metro.",
    "services_h2":"Our Plumbing Services in Fort Worth, TX",
    "services_sub":"Complete plumbing solutions for Fort Worth homes and businesses",
    "cta_h2":"Need a Licensed Plumber in Fort Worth, TX?",
    "cta_sub":"Connect with trusted local plumbers in Fort Worth for residential and commercial plumbing needs. Free estimates, same-day service available.",
    "schema_desc":"Connect with trusted licensed plumbers in Fort Worth, TX for emergency plumbing, drain cleaning, water heater repair, leak detection, and more.",
    "faq":[
      ("How much do plumbers charge per hour in Fort Worth?","Plumbing rates in Fort Worth, TX typically range from $80 to $145 per hour. Emergency and after-hours services may cost more. Free written estimates are always provided before work begins."),
      ("What is the best plumbing company in Fort Worth?","PlumbersInUSA.com connects you with multiple licensed, insured, and top-rated plumbing professionals in Fort Worth so you can compare and choose the best option for your needs."),
      ("Do Fort Worth plumbers offer same-day service?","Yes. Most licensed plumbers in Fort Worth offer same-day and 24/7 emergency service for urgent issues including burst pipes, blocked drains, and water heater failures."),
      ("Are Fort Worth plumbers licensed in Texas?","Yes. All plumbing professionals connected through PlumbersInUSA.com serving Fort Worth are fully licensed, bonded, and insured in the state of Texas."),
      ("What areas of Fort Worth do local plumbers serve?","Local plumbers serve all Fort Worth neighborhoods including Arlington, Keller, Grapevine, Southlake, Euless, Bedford, North Richland Hills, and the TCU area."),
    ]
  },
  {
    "dir":"plumber-charlotte-nc","city":"Charlotte","state":"NC","state_full":"North Carolina",
    "title":"Licensed Plumbers in Charlotte, NC | 24/7 Emergency | Free Estimates",
    "desc":"Find trusted licensed plumbers in Charlotte, NC. Emergency plumbing, drain cleaning, water heater repair & more. 24/7 service, same-day availability. Free estimates.",
    "kw":"plumbers in charlotte, charlotte plumber, emergency plumbing charlotte nc, drain cleaning charlotte, water heater repair charlotte, plumber near me charlotte nc",
    "h1":"Trusted Plumbers in Charlotte, NC",
    "hero_sub":"Fast, reliable plumbing services for homes and businesses across Charlotte, North Carolina. Connect with licensed local plumbers for emergency repairs, drain cleaning, water heater services, and more.",
    "intro_h2":"Professional Plumbing Services in Charlotte, North Carolina",
    "intro_sub":"Your trusted local plumbing experts serving Charlotte and the surrounding metro area",
    "intro_p1":"Charlotte's rapid growth and mix of older neighborhoods and new construction create diverse plumbing needs — from aging cast iron and galvanized pipes in historic areas to new build quality control in fast-developing suburbs. The Piedmont's clay soil also contributes to root intrusions and drain issues. PlumbersInUSA.com connects you with licensed, insured plumbing professionals serving Huntersville, Concord, Gastonia, Matthews, Ballantyne, and the full Charlotte metro.",
    "services_h2":"Our Plumbing Services in Charlotte, NC",
    "services_sub":"Complete plumbing solutions for Charlotte homes and businesses",
    "cta_h2":"Need a Licensed Plumber in Charlotte, NC?",
    "cta_sub":"Connect with trusted local plumbers in Charlotte for residential and commercial plumbing needs. Free estimates, same-day service available.",
    "schema_desc":"Connect with trusted licensed plumbers in Charlotte, NC for emergency plumbing, drain cleaning, water heater repair, leak detection, and more.",
    "faq":[
      ("How much do plumbers charge per hour in Charlotte?","Plumbing rates in Charlotte, NC typically range from $80 to $140 per hour. Emergency services may cost more. Free written estimates are always provided before work begins."),
      ("What is the best plumbing company in Charlotte?","PlumbersInUSA.com connects you with multiple licensed, insured, and top-rated plumbing professionals in Charlotte so you can compare options and choose the best fit."),
      ("Do Charlotte plumbers offer same-day service?","Yes. Most licensed plumbers in Charlotte offer same-day and 24/7 emergency service for burst pipes, clogged drains, water heater failures, and other urgent plumbing issues."),
      ("Are Charlotte plumbers licensed in North Carolina?","Yes. All plumbing professionals connected through PlumbersInUSA.com serving Charlotte are fully licensed, bonded, and insured in the state of North Carolina."),
      ("What areas of Charlotte do local plumbers serve?","Local plumbers serve all Charlotte neighborhoods including Huntersville, Concord, Gastonia, Matthews, Mint Hill, Ballantyne, NoDa, Pineville, Plaza Midwood, and South End."),
    ]
  },
  {
    "dir":"plumber-raleigh-nc","city":"Raleigh","state":"NC","state_full":"North Carolina",
    "title":"Licensed Plumbers in Raleigh, NC | 24/7 Emergency Service | Free Estimates",
    "desc":"Find trusted licensed plumbers in Raleigh, NC. Emergency plumbing, drain cleaning, water heater repair & more. 24/7 service, same-day availability. Free estimates.",
    "kw":"plumbers in raleigh, raleigh plumber, emergency plumbing raleigh nc, drain cleaning raleigh, water heater repair raleigh, plumber near me raleigh nc",
    "h1":"Trusted Plumbers in Raleigh, NC",
    "hero_sub":"Fast, reliable plumbing services for homes and businesses across Raleigh, North Carolina. Connect with licensed local plumbers for emergency repairs, drain cleaning, water heater services, and more.",
    "intro_h2":"Professional Plumbing Services in Raleigh, North Carolina",
    "intro_sub":"Your trusted local plumbing experts serving Raleigh and the surrounding metro area",
    "intro_p1":"Raleigh's rapid population growth has placed high demand on plumbing infrastructure — from older urban pipes in established neighborhoods to new construction in fast-growing suburbs. The Piedmont region's clay soil can shift seasonally, causing sewer line issues and foundation cracks that lead to hidden leaks. PlumbersInUSA.com connects you with licensed, insured plumbing professionals serving Cary, Apex, Morrisville, Wake Forest, Garner, and the full Triangle area.",
    "services_h2":"Our Plumbing Services in Raleigh, NC",
    "services_sub":"Complete plumbing solutions for Raleigh homes and businesses",
    "cta_h2":"Need a Licensed Plumber in Raleigh, NC?",
    "cta_sub":"Connect with trusted local plumbers in Raleigh for residential and commercial plumbing needs. Free estimates, same-day service available.",
    "schema_desc":"Connect with trusted licensed plumbers in Raleigh, NC for emergency plumbing, drain cleaning, water heater repair, leak detection, and more.",
    "faq":[
      ("How much do plumbers charge per hour in Raleigh?","Plumbing rates in Raleigh, NC typically range from $85 to $145 per hour. Emergency services may cost more. Free written estimates are always provided before work begins."),
      ("What is the best plumbing company in Raleigh?","PlumbersInUSA.com connects you with multiple licensed, insured, and highly-rated plumbing professionals in Raleigh so you can compare options and choose the best fit."),
      ("Do Raleigh plumbers offer same-day service?","Yes. Most licensed plumbers in Raleigh offer same-day and 24/7 emergency service for urgent issues including burst pipes, drain clogs, and water heater failures."),
      ("Are Raleigh plumbers licensed in North Carolina?","Yes. All plumbing professionals connected through PlumbersInUSA.com serving Raleigh are fully licensed, bonded, and insured in the state of North Carolina."),
      ("What areas of Raleigh do local plumbers serve?","Local plumbers serve all Raleigh neighborhoods including Cary, Apex, Morrisville, Wake Forest, Garner, Holly Springs, Knightdale, Fuquay-Varina, and North Hills."),
    ]
  },
  {
    "dir":"plumber-greensboro-nc","city":"Greensboro","state":"NC","state_full":"North Carolina",
    "title":"Licensed Plumbers in Greensboro, NC | 24/7 Emergency | Free Estimates",
    "desc":"Find trusted licensed plumbers in Greensboro, NC. Emergency plumbing, drain cleaning, water heater repair & more. 24/7 service, same-day availability. Free estimates.",
    "kw":"plumbers in greensboro, greensboro plumber, emergency plumbing greensboro nc, drain cleaning greensboro, water heater repair greensboro, plumber near me greensboro nc",
    "h1":"Trusted Plumbers in Greensboro, NC",
    "hero_sub":"Fast, reliable plumbing services for homes and businesses across Greensboro, North Carolina. Connect with licensed local plumbers for emergency repairs, drain cleaning, water heater services, and more.",
    "intro_h2":"Professional Plumbing Services in Greensboro, North Carolina",
    "intro_sub":"Your trusted local plumbing experts serving Greensboro and the surrounding area",
    "intro_p1":"Greensboro's mix of older housing stock and growing suburban development creates a wide range of plumbing needs — from deteriorating cast iron drain lines in historic neighborhoods to new-build installations in expanding areas. The Piedmont's humid subtropical climate and clay-heavy soils contribute to root intrusions and seasonal pipe stress. PlumbersInUSA.com connects you with licensed, insured plumbing professionals serving High Point, Kernersville, Jamestown, Oak Ridge, Summerfield, and the surrounding Triad area.",
    "services_h2":"Our Plumbing Services in Greensboro, NC",
    "services_sub":"Complete plumbing solutions for Greensboro homes and businesses",
    "cta_h2":"Need a Licensed Plumber in Greensboro, NC?",
    "cta_sub":"Connect with trusted local plumbers in Greensboro for residential and commercial plumbing needs. Free estimates, same-day service available.",
    "schema_desc":"Connect with trusted licensed plumbers in Greensboro, NC for emergency plumbing, drain cleaning, water heater repair, leak detection, and more.",
    "faq":[
      ("How much do plumbers charge per hour in Greensboro?","Plumbing rates in Greensboro, NC typically range from $75 to $130 per hour. Emergency services may cost more. Free written estimates are always provided before work begins."),
      ("What is the best plumbing company in Greensboro?","PlumbersInUSA.com connects you with multiple licensed, insured, and top-rated plumbing professionals in Greensboro so you can compare and choose the best option."),
      ("Do Greensboro plumbers offer same-day service?","Yes. Most licensed plumbers in Greensboro offer same-day and 24/7 emergency service for urgent plumbing issues including burst pipes, blocked drains, and water heater failures."),
      ("Are Greensboro plumbers licensed in North Carolina?","Yes. All plumbing professionals connected through PlumbersInUSA.com serving Greensboro are fully licensed, bonded, and insured in the state of North Carolina."),
      ("What areas of Greensboro do local plumbers serve?","Local plumbers serve all Greensboro neighborhoods including High Point, Kernersville, Jamestown, Oak Ridge, Summerfield, Whitsett, Friendly Center, and Downtown."),
    ]
  },
  {
    "dir":"plumber-nashville-tn","city":"Nashville","state":"TN","state_full":"Tennessee",
    "title":"Licensed Plumbers in Nashville, TN | 24/7 Emergency Service | Free Estimates",
    "desc":"Find trusted licensed plumbers in Nashville, TN. Emergency plumbing, drain cleaning, water heater repair & more. 24/7 service, same-day availability. Free estimates.",
    "kw":"plumbers in nashville, nashville plumber, emergency plumbing nashville tn, drain cleaning nashville, water heater repair nashville, plumber near me nashville",
    "h1":"Trusted Plumbers in Nashville, TN",
    "hero_sub":"Fast, reliable plumbing services for homes and businesses across Nashville, Tennessee. Connect with licensed local plumbers for emergency repairs, drain cleaning, water heater services, and more.",
    "intro_h2":"Professional Plumbing Services in Nashville, Tennessee",
    "intro_sub":"Your trusted local plumbing experts serving Nashville and the surrounding metro area",
    "intro_p1":"Nashville's rapid population growth, limestone substrate, and hard water create persistent plumbing challenges — from scale buildup in water heaters and fixtures to aging cast iron drain lines in older Music City neighborhoods. Seasonal temperature swings can also stress outdoor pipes. PlumbersInUSA.com connects you with licensed, insured plumbing professionals serving Brentwood, Franklin, Hendersonville, Mount Juliet, Antioch, East Nashville, and the full Nashville metro.",
    "services_h2":"Our Plumbing Services in Nashville, TN",
    "services_sub":"Complete plumbing solutions for Nashville homes and businesses",
    "cta_h2":"Need a Licensed Plumber in Nashville, TN?",
    "cta_sub":"Connect with trusted local plumbers in Nashville for residential and commercial plumbing needs. Free estimates, same-day service available.",
    "schema_desc":"Connect with trusted licensed plumbers in Nashville, TN for emergency plumbing, drain cleaning, water heater repair, leak detection, and more.",
    "faq":[
      ("How much do plumbers charge per hour in Nashville?","Plumbing rates in Nashville, TN typically range from $80 to $145 per hour. Emergency services may cost more. Free written estimates are always provided before work begins."),
      ("What is the best plumbing company in Nashville?","PlumbersInUSA.com connects you with multiple licensed, insured, and highly-rated plumbing professionals in Nashville so you can compare options and choose the right fit."),
      ("Do Nashville plumbers offer same-day service?","Yes. Most licensed plumbers in Nashville offer same-day and 24/7 emergency service for urgent issues including burst pipes, clogged drains, and water heater failures."),
      ("Are Nashville plumbers licensed in Tennessee?","Yes. All plumbing professionals connected through PlumbersInUSA.com serving Nashville are fully licensed, bonded, and insured in the state of Tennessee."),
      ("What areas of Nashville do local plumbers serve?","Local plumbers serve all Nashville neighborhoods including Brentwood, Franklin, Hendersonville, Mount Juliet, Antioch, Bellevue, East Nashville, Green Hills, and The Gulch."),
    ]
  },
  {
    "dir":"plumber-memphis-tn","city":"Memphis","state":"TN","state_full":"Tennessee",
    "title":"Licensed Plumbers in Memphis, TN | 24/7 Emergency Service | Free Estimates",
    "desc":"Find trusted licensed plumbers in Memphis, TN. Emergency plumbing, drain cleaning, water heater repair & more. 24/7 service, same-day availability. Free estimates.",
    "kw":"plumbers in memphis, memphis plumber, emergency plumbing memphis tn, drain cleaning memphis, water heater repair memphis, plumber near me memphis",
    "h1":"Trusted Plumbers in Memphis, TN",
    "hero_sub":"Fast, reliable plumbing services for homes and businesses across Memphis, Tennessee. Connect with licensed local plumbers for emergency repairs, drain cleaning, water heater services, and more.",
    "intro_h2":"Professional Plumbing Services in Memphis, Tennessee",
    "intro_sub":"Your trusted local plumbing experts serving Memphis and the surrounding area",
    "intro_p1":"Memphis's high humidity, clay-heavy Mississippi Delta soils, and large stock of older homes create persistent plumbing demands — from corroded cast iron drain lines and galvanized water pipes in historic neighborhoods to high water table issues affecting sewer systems. PlumbersInUSA.com connects you with licensed, insured plumbing professionals serving Germantown, Collierville, Bartlett, Cordova, East Memphis, Midtown, and Southaven.",
    "services_h2":"Our Plumbing Services in Memphis, TN",
    "services_sub":"Complete plumbing solutions for Memphis homes and businesses",
    "cta_h2":"Need a Licensed Plumber in Memphis, TN?",
    "cta_sub":"Connect with trusted local plumbers in Memphis for residential and commercial plumbing needs. Free estimates, same-day service available.",
    "schema_desc":"Connect with trusted licensed plumbers in Memphis, TN for emergency plumbing, drain cleaning, water heater repair, leak detection, and more.",
    "faq":[
      ("How much do plumbers charge per hour in Memphis?","Plumbing rates in Memphis, TN typically range from $70 to $125 per hour. Emergency services may cost more. Free written estimates are always provided before work begins."),
      ("What is the best plumbing company in Memphis?","PlumbersInUSA.com connects you with multiple licensed, insured, and top-rated plumbing professionals in Memphis so you can compare options and choose the best fit."),
      ("Do Memphis plumbers offer same-day service?","Yes. Most licensed plumbers in Memphis offer same-day and 24/7 emergency service for urgent plumbing issues including burst pipes, blocked drains, and water heater failures."),
      ("Are Memphis plumbers licensed in Tennessee?","Yes. All plumbing professionals connected through PlumbersInUSA.com serving Memphis are fully licensed, bonded, and insured in the state of Tennessee."),
      ("What areas of Memphis do local plumbers serve?","Local plumbers serve all Memphis neighborhoods including Germantown, Collierville, Bartlett, Cordova, East Memphis, Midtown, Downtown, Whitehaven, and Southaven."),
    ]
  },
  {
    "dir":"plumber-tampa-fl","city":"Tampa","state":"FL","state_full":"Florida",
    "title":"Licensed Plumbers in Tampa, FL | 24/7 Emergency Service | Free Estimates",
    "desc":"Find trusted licensed plumbers in Tampa, FL. Emergency plumbing, drain cleaning, water heater repair & more. 24/7 service, same-day availability. Free estimates.",
    "kw":"plumbers in tampa, tampa plumber, emergency plumbing tampa fl, drain cleaning tampa, water heater repair tampa, plumber near me tampa",
    "h1":"Trusted Plumbers in Tampa, FL",
    "hero_sub":"Fast, reliable plumbing services for homes and businesses across Tampa, Florida. Connect with licensed local plumbers for emergency repairs, drain cleaning, water heater services, and more.",
    "intro_h2":"Professional Plumbing Services in Tampa, Florida",
    "intro_sub":"Your trusted local plumbing experts serving Tampa and the surrounding area",
    "intro_p1":"Tampa's high humidity, hard water, coastal salt air, and hurricane season create year-round plumbing challenges — from accelerated pipe corrosion near the bay to storm drain backups and water heater mineral buildup. Older Tampa Bay neighborhoods often have aging cast iron and galvanized steel pipes in need of replacement. PlumbersInUSA.com connects you with licensed, insured plumbing professionals serving Brandon, Clearwater, Riverview, Wesley Chapel, Westchase, Hyde Park, and the full Tampa Bay area.",
    "services_h2":"Our Plumbing Services in Tampa, FL",
    "services_sub":"Complete plumbing solutions for Tampa homes and businesses",
    "cta_h2":"Need a Licensed Plumber in Tampa, FL?",
    "cta_sub":"Connect with trusted local plumbers in Tampa for residential and commercial plumbing needs. Free estimates, same-day service available.",
    "schema_desc":"Connect with trusted licensed plumbers in Tampa, FL for emergency plumbing, drain cleaning, water heater repair, leak detection, and more.",
    "faq":[
      ("How much do plumbers charge per hour in Tampa?","Plumbing rates in Tampa, FL typically range from $80 to $145 per hour. Emergency services may cost more. Free written estimates are always provided before work begins."),
      ("What is the best plumbing company in Tampa?","PlumbersInUSA.com connects you with multiple licensed, insured, and top-rated plumbing professionals in Tampa so you can compare options and choose the best fit."),
      ("Do Tampa plumbers offer same-day service?","Yes. Most licensed plumbers in Tampa offer same-day and 24/7 emergency service for urgent issues including burst pipes, storm drain backups, and water heater failures."),
      ("Are Tampa plumbers licensed in Florida?","Yes. All plumbing professionals connected through PlumbersInUSA.com serving Tampa are fully licensed, bonded, and insured in the state of Florida."),
      ("What areas of Tampa do local plumbers serve?","Local plumbers serve all Tampa neighborhoods including Brandon, Clearwater, Riverview, Wesley Chapel, Westchase, Carrollwood, Hyde Park, Ybor City, and Temple Terrace."),
    ]
  },
  {
    "dir":"plumber-jacksonville-fl","city":"Jacksonville","state":"FL","state_full":"Florida",
    "title":"Licensed Plumbers in Jacksonville, FL | 24/7 Emergency | Free Estimates",
    "desc":"Find trusted licensed plumbers in Jacksonville, FL. Emergency plumbing, drain cleaning, water heater repair & more. 24/7 service, same-day availability. Free estimates.",
    "kw":"plumbers in jacksonville, jacksonville plumber, emergency plumbing jacksonville fl, drain cleaning jacksonville, water heater repair jacksonville, plumber near me jacksonville",
    "h1":"Trusted Plumbers in Jacksonville, FL",
    "hero_sub":"Fast, reliable plumbing services for homes and businesses across Jacksonville, Florida. Connect with licensed local plumbers for emergency repairs, drain cleaning, water heater services, and more.",
    "intro_h2":"Professional Plumbing Services in Jacksonville, Florida",
    "intro_sub":"Your trusted local plumbing experts serving Jacksonville and the surrounding area",
    "intro_p1":"Jacksonville's sandy coastal soils, high water table, and storm season create unique plumbing challenges — from drainage issues and sewer line shifts to accelerated pipe corrosion in older neighborhoods near the St. Johns River. Many of Jacksonville's established homes have aging plumbing systems in need of inspection or updating. PlumbersInUSA.com connects you with licensed, insured plumbing professionals serving Orange Park, Mandarin, Riverside, Atlantic Beach, Jacksonville Beach, and the full Northeast Florida area.",
    "services_h2":"Our Plumbing Services in Jacksonville, FL",
    "services_sub":"Complete plumbing solutions for Jacksonville homes and businesses",
    "cta_h2":"Need a Licensed Plumber in Jacksonville, FL?",
    "cta_sub":"Connect with trusted local plumbers in Jacksonville for residential and commercial plumbing needs. Free estimates, same-day service available.",
    "schema_desc":"Connect with trusted licensed plumbers in Jacksonville, FL for emergency plumbing, drain cleaning, water heater repair, leak detection, and more.",
    "faq":[
      ("How much do plumbers charge per hour in Jacksonville?","Plumbing rates in Jacksonville, FL typically range from $75 to $135 per hour. Emergency services may cost more. Free written estimates are always provided before work begins."),
      ("What is the best plumbing company in Jacksonville?","PlumbersInUSA.com connects you with multiple licensed, insured, and top-rated plumbing professionals in Jacksonville so you can compare options and choose the best fit."),
      ("Do Jacksonville plumbers offer same-day service?","Yes. Most licensed plumbers in Jacksonville offer same-day and 24/7 emergency service for urgent issues including burst pipes, clogged drains, and water heater failures."),
      ("Are Jacksonville plumbers licensed in Florida?","Yes. All plumbing professionals connected through PlumbersInUSA.com serving Jacksonville are fully licensed, bonded, and insured in the state of Florida."),
      ("What areas of Jacksonville do local plumbers serve?","Local plumbers serve all Jacksonville neighborhoods including Orange Park, Mandarin, Riverside, Atlantic Beach, Jacksonville Beach, Neptune Beach, Arlington, San Marco, and Southside."),
    ]
  },
  {
    "dir":"plumber-denver-co","city":"Denver","state":"CO","state_full":"Colorado",
    "title":"Licensed Plumbers in Denver, CO | 24/7 Emergency Service | Free Estimates",
    "desc":"Find trusted licensed plumbers in Denver, CO. Emergency plumbing, drain cleaning, water heater repair & more. 24/7 service, same-day availability. Free estimates.",
    "kw":"plumbers in denver, denver plumber, emergency plumbing denver co, drain cleaning denver, water heater repair denver, plumber near me denver",
    "h1":"Trusted Plumbers in Denver, CO",
    "hero_sub":"Fast, reliable plumbing services for homes and businesses across Denver, Colorado. Connect with licensed local plumbers for emergency repairs, drain cleaning, water heater services, and more.",
    "intro_h2":"Professional Plumbing Services in Denver, Colorado",
    "intro_sub":"Your trusted local plumbing experts serving Denver and the surrounding metro area",
    "intro_p1":"Denver's altitude, extreme freeze-thaw cycles, and older historic neighborhoods create unique plumbing challenges — from burst pipes during hard winter freezes to deteriorating galvanized steel and cast iron pipes in Capitol Hill, Curtis Park, and other established Denver neighborhoods. Hard water from Rocky Mountain runoff also accelerates scale buildup. PlumbersInUSA.com connects you with licensed, insured plumbing professionals serving Aurora, Lakewood, Arvada, Thornton, Westminster, Littleton, and the full Denver metro.",
    "services_h2":"Our Plumbing Services in Denver, CO",
    "services_sub":"Complete plumbing solutions for Denver homes and businesses",
    "cta_h2":"Need a Licensed Plumber in Denver, CO?",
    "cta_sub":"Connect with trusted local plumbers in Denver for residential and commercial plumbing needs. Free estimates, same-day service available.",
    "schema_desc":"Connect with trusted licensed plumbers in Denver, CO for emergency plumbing, drain cleaning, water heater repair, leak detection, and more.",
    "faq":[
      ("How much do plumbers charge per hour in Denver?","Plumbing rates in Denver, CO typically range from $90 to $160 per hour. Emergency services may cost more. Free written estimates are always provided before work begins."),
      ("What is the best plumbing company in Denver?","PlumbersInUSA.com connects you with multiple licensed, insured, and top-rated plumbing professionals in Denver so you can compare options and choose the best fit."),
      ("Do Denver plumbers offer same-day service?","Yes. Most licensed plumbers in Denver offer same-day and 24/7 emergency service for urgent issues including burst pipes, clogged drains, and water heater failures."),
      ("Are Denver plumbers licensed in Colorado?","Yes. All plumbing professionals connected through PlumbersInUSA.com serving Denver are fully licensed, bonded, and insured in the state of Colorado."),
      ("What areas of Denver do local plumbers serve?","Local plumbers serve all Denver neighborhoods including Aurora, Lakewood, Arvada, Thornton, Westminster, Littleton, Englewood, Cherry Creek, Capitol Hill, and LoDo."),
    ]
  },
  {
    "dir":"plumber-atlanta-ga","city":"Atlanta","state":"GA","state_full":"Georgia",
    "title":"Licensed Plumbers in Atlanta, GA | 24/7 Emergency Service | Free Estimates",
    "desc":"Find trusted licensed plumbers in Atlanta, GA. Emergency plumbing, drain cleaning, water heater repair & more. 24/7 service, same-day availability. Free estimates.",
    "kw":"plumbers in atlanta, atlanta plumber, emergency plumbing atlanta ga, drain cleaning atlanta, water heater repair atlanta, plumber near me atlanta",
    "h1":"Trusted Plumbers in Atlanta, GA",
    "hero_sub":"Fast, reliable plumbing services for homes and businesses across Atlanta, Georgia. Connect with licensed local plumbers for emergency repairs, drain cleaning, water heater services, and more.",
    "intro_h2":"Professional Plumbing Services in Atlanta, Georgia",
    "intro_sub":"Your trusted local plumbing experts serving Atlanta and the surrounding metro area",
    "intro_p1":"Atlanta's notorious red clay soil shifts significantly with rainfall and drought, putting stress on buried sewer lines and causing foundation movement that leads to hidden pipe leaks. Older Atlanta neighborhoods — from Buckhead to Decatur — often have aging cast iron drain lines that need inspection. PlumbersInUSA.com connects you with licensed, insured plumbing professionals serving Marietta, Roswell, Alpharetta, Dunwoody, Sandy Springs, Decatur, Smyrna, and the full metro Atlanta area.",
    "services_h2":"Our Plumbing Services in Atlanta, GA",
    "services_sub":"Complete plumbing solutions for Atlanta homes and businesses",
    "cta_h2":"Need a Licensed Plumber in Atlanta, GA?",
    "cta_sub":"Connect with trusted local plumbers in Atlanta for residential and commercial plumbing needs. Free estimates, same-day service available.",
    "schema_desc":"Connect with trusted licensed plumbers in Atlanta, GA for emergency plumbing, drain cleaning, water heater repair, leak detection, and more.",
    "faq":[
      ("How much do plumbers charge per hour in Atlanta?","Plumbing rates in Atlanta, GA typically range from $80 to $145 per hour. Emergency services may cost more. Free written estimates are always provided before work begins."),
      ("What is the best plumbing company in Atlanta?","PlumbersInUSA.com connects you with multiple licensed, insured, and top-rated plumbing professionals in Atlanta so you can compare options and choose the best fit."),
      ("Do Atlanta plumbers offer same-day service?","Yes. Most licensed plumbers in Atlanta offer same-day and 24/7 emergency service for urgent issues including burst pipes, clogged drains, and water heater failures."),
      ("Are Atlanta plumbers licensed in Georgia?","Yes. All plumbing professionals connected through PlumbersInUSA.com serving Atlanta are fully licensed, bonded, and insured in the state of Georgia."),
      ("What areas of Atlanta do local plumbers serve?","Local plumbers serve all Atlanta neighborhoods including Marietta, Roswell, Alpharetta, Dunwoody, Sandy Springs, Decatur, Smyrna, Brookhaven, Buckhead, and Midtown."),
    ]
  },
  {
    "dir":"plumber-louisville-ky","city":"Louisville","state":"KY","state_full":"Kentucky",
    "title":"Licensed Plumbers in Louisville, KY | 24/7 Emergency Service | Free Estimates",
    "desc":"Find trusted licensed plumbers in Louisville, KY. Emergency plumbing, drain cleaning, water heater repair & more. 24/7 service, same-day availability. Free estimates.",
    "kw":"plumbers in louisville, louisville plumber, emergency plumbing louisville ky, drain cleaning louisville, water heater repair louisville, plumber near me louisville",
    "h1":"Trusted Plumbers in Louisville, KY",
    "hero_sub":"Fast, reliable plumbing services for homes and businesses across Louisville, Kentucky. Connect with licensed local plumbers for emergency repairs, drain cleaning, water heater services, and more.",
    "intro_h2":"Professional Plumbing Services in Louisville, Kentucky",
    "intro_sub":"Your trusted local plumbing experts serving Louisville and the surrounding area",
    "intro_p1":"Louisville's Ohio River valley location, humid climate, and large stock of older Victorian and mid-century homes create significant plumbing demands — from aging galvanized steel and cast iron pipes to basement flooding issues common near the riverfront. Hard winters also bring pipe freeze risks. PlumbersInUSA.com connects you with licensed, insured plumbing professionals serving Jeffersontown, St. Matthews, Clarksville, New Albany, Shively, Middletown, and the full Louisville metro.",
    "services_h2":"Our Plumbing Services in Louisville, KY",
    "services_sub":"Complete plumbing solutions for Louisville homes and businesses",
    "cta_h2":"Need a Licensed Plumber in Louisville, KY?",
    "cta_sub":"Connect with trusted local plumbers in Louisville for residential and commercial plumbing needs. Free estimates, same-day service available.",
    "schema_desc":"Connect with trusted licensed plumbers in Louisville, KY for emergency plumbing, drain cleaning, water heater repair, leak detection, and more.",
    "faq":[
      ("How much do plumbers charge per hour in Louisville?","Plumbing rates in Louisville, KY typically range from $70 to $130 per hour. Emergency services may cost more. Free written estimates are always provided before work begins."),
      ("What is the best plumbing company in Louisville?","PlumbersInUSA.com connects you with multiple licensed, insured, and top-rated plumbing professionals in Louisville so you can compare options and choose the best fit."),
      ("Do Louisville plumbers offer same-day service?","Yes. Most licensed plumbers in Louisville offer same-day and 24/7 emergency service for urgent issues including burst pipes, clogged drains, and water heater failures."),
      ("Are Louisville plumbers licensed in Kentucky?","Yes. All plumbing professionals connected through PlumbersInUSA.com serving Louisville are fully licensed, bonded, and insured in the state of Kentucky."),
      ("What areas of Louisville do local plumbers serve?","Local plumbers serve all Louisville neighborhoods including Jeffersontown, St. Matthews, Clarksville, New Albany, Shively, Middletown, Lyndon, Highlands, and Downtown."),
    ]
  },
  {
    "dir":"plumber-las-vegas-nv","city":"Las Vegas","state":"NV","state_full":"Nevada",
    "title":"Licensed Plumbers in Las Vegas, NV | 24/7 Emergency Service | Free Estimates",
    "desc":"Find trusted licensed plumbers in Las Vegas, NV. Emergency plumbing, drain cleaning, water heater repair & more. 24/7 service, same-day availability. Free estimates.",
    "kw":"plumbers in las vegas, las vegas plumber, emergency plumbing las vegas nv, drain cleaning las vegas, water heater repair las vegas, plumber near me las vegas",
    "h1":"Trusted Plumbers in Las Vegas, NV",
    "hero_sub":"Fast, reliable plumbing services for homes and businesses across Las Vegas, Nevada. Connect with licensed local plumbers for emergency repairs, drain cleaning, water heater services, and more.",
    "intro_h2":"Professional Plumbing Services in Las Vegas, Nevada",
    "intro_sub":"Your trusted local plumbing experts serving Las Vegas and the surrounding area",
    "intro_p1":"Las Vegas has some of the hardest water in the United States — heavy with calcium and magnesium from the Colorado River and Mojave Desert groundwater. This extreme hard water causes rapid scale buildup in water heaters, pipes, and fixtures, shortening their lifespan significantly. Desert heat also stresses outdoor supply lines and irrigation systems. PlumbersInUSA.com connects you with licensed, insured plumbing professionals serving Henderson, North Las Vegas, Summerlin, Enterprise, Spring Valley, Paradise, and the full Las Vegas Valley.",
    "services_h2":"Our Plumbing Services in Las Vegas, NV",
    "services_sub":"Complete plumbing solutions for Las Vegas homes and businesses",
    "cta_h2":"Need a Licensed Plumber in Las Vegas, NV?",
    "cta_sub":"Connect with trusted local plumbers in Las Vegas for residential and commercial plumbing needs. Free estimates, same-day service available.",
    "schema_desc":"Connect with trusted licensed plumbers in Las Vegas, NV for emergency plumbing, drain cleaning, water heater repair, leak detection, and more.",
    "faq":[
      ("How much do plumbers charge per hour in Las Vegas?","Plumbing rates in Las Vegas, NV typically range from $85 to $150 per hour. Emergency services may cost more. Free written estimates are always provided before work begins."),
      ("What is the best plumbing company in Las Vegas?","PlumbersInUSA.com connects you with multiple licensed, insured, and top-rated plumbing professionals in Las Vegas so you can compare options and choose the best fit."),
      ("Do Las Vegas plumbers offer same-day service?","Yes. Most licensed plumbers in Las Vegas offer same-day and 24/7 emergency service for urgent issues including burst pipes, clogged drains, and water heater failures."),
      ("Are Las Vegas plumbers licensed in Nevada?","Yes. All plumbing professionals connected through PlumbersInUSA.com serving Las Vegas are fully licensed, bonded, and insured in the state of Nevada."),
      ("What areas of Las Vegas do local plumbers serve?","Local plumbers serve all Las Vegas neighborhoods including Henderson, North Las Vegas, Summerlin, Enterprise, Spring Valley, Paradise, Sunrise Manor, and The Strip area."),
    ]
  },
  {
    "dir":"plumber-albuquerque-nm","city":"Albuquerque","state":"NM","state_full":"New Mexico",
    "title":"Licensed Plumbers in Albuquerque, NM | 24/7 Emergency | Free Estimates",
    "desc":"Find trusted licensed plumbers in Albuquerque, NM. Emergency plumbing, drain cleaning, water heater repair & more. 24/7 service, same-day availability. Free estimates.",
    "kw":"plumbers in albuquerque, albuquerque plumber, emergency plumbing albuquerque nm, drain cleaning albuquerque, water heater repair albuquerque, plumber near me albuquerque",
    "h1":"Trusted Plumbers in Albuquerque, NM",
    "hero_sub":"Fast, reliable plumbing services for homes and businesses across Albuquerque, New Mexico. Connect with licensed local plumbers for emergency repairs, drain cleaning, water heater services, and more.",
    "intro_h2":"Professional Plumbing Services in Albuquerque, New Mexico",
    "intro_sub":"Your trusted local plumbing experts serving Albuquerque and the surrounding area",
    "intro_p1":"Albuquerque's high desert climate, hard water from the Rio Grande aquifer, and mix of adobe and older conventional construction create specific plumbing demands — from mineral scale buildup and accelerated fixture wear to freeze events during cold Sandia Mountain winters. PlumbersInUSA.com connects you with licensed, insured plumbing professionals serving Rio Rancho, Old Town, Nob Hill, Corrales, the North Valley, South Valley, Westside, and all surrounding areas.",
    "services_h2":"Our Plumbing Services in Albuquerque, NM",
    "services_sub":"Complete plumbing solutions for Albuquerque homes and businesses",
    "cta_h2":"Need a Licensed Plumber in Albuquerque, NM?",
    "cta_sub":"Connect with trusted local plumbers in Albuquerque for residential and commercial plumbing needs. Free estimates, same-day service available.",
    "schema_desc":"Connect with trusted licensed plumbers in Albuquerque, NM for emergency plumbing, drain cleaning, water heater repair, leak detection, and more.",
    "faq":[
      ("How much do plumbers charge per hour in Albuquerque?","Plumbing rates in Albuquerque, NM typically range from $70 to $130 per hour. Emergency services may cost more. Free written estimates are always provided before work begins."),
      ("What is the best plumbing company in Albuquerque?","PlumbersInUSA.com connects you with multiple licensed, insured, and top-rated plumbing professionals in Albuquerque so you can compare options and choose the best fit."),
      ("Do Albuquerque plumbers offer same-day service?","Yes. Most licensed plumbers in Albuquerque offer same-day and 24/7 emergency service for urgent plumbing issues including burst pipes, blocked drains, and water heater failures."),
      ("Are Albuquerque plumbers licensed in New Mexico?","Yes. All plumbing professionals connected through PlumbersInUSA.com serving Albuquerque are fully licensed, bonded, and insured in the state of New Mexico."),
      ("What areas of Albuquerque do local plumbers serve?","Local plumbers serve all Albuquerque neighborhoods including Rio Rancho, Old Town, Nob Hill, Corrales, the North Valley, South Valley, Uptown, and Westside."),
    ]
  },
  {
    "dir":"plumber-oklahoma-city-ok","city":"Oklahoma City","state":"OK","state_full":"Oklahoma",
    "title":"Licensed Plumbers in Oklahoma City, OK | 24/7 Emergency | Free Estimates",
    "desc":"Find trusted licensed plumbers in Oklahoma City, OK. Emergency plumbing, drain cleaning, water heater repair & more. 24/7 service, same-day availability. Free estimates.",
    "kw":"plumbers in oklahoma city, oklahoma city plumber, emergency plumbing oklahoma city ok, drain cleaning oklahoma city, water heater repair oklahoma city, plumber near me oklahoma city",
    "h1":"Trusted Plumbers in Oklahoma City, OK",
    "hero_sub":"Fast, reliable plumbing services for homes and businesses across Oklahoma City, Oklahoma. Connect with licensed local plumbers for emergency repairs, drain cleaning, water heater services, and more.",
    "intro_h2":"Professional Plumbing Services in Oklahoma City, Oklahoma",
    "intro_sub":"Your trusted local plumbing experts serving Oklahoma City and the surrounding area",
    "intro_p1":"Oklahoma City's red clay soil, extreme temperature swings, and severe weather events — including tornadoes and ice storms — create significant plumbing challenges year-round. Clay soil heave and shrinkage stress sewer lines, while sudden hard freezes can burst outdoor and poorly insulated pipes. PlumbersInUSA.com connects you with licensed, insured plumbing professionals serving Edmond, Norman, Moore, Midwest City, Del City, Yukon, Nichols Hills, Bricktown, and the full OKC metro.",
    "services_h2":"Our Plumbing Services in Oklahoma City, OK",
    "services_sub":"Complete plumbing solutions for Oklahoma City homes and businesses",
    "cta_h2":"Need a Licensed Plumber in Oklahoma City, OK?",
    "cta_sub":"Connect with trusted local plumbers in Oklahoma City for residential and commercial plumbing needs. Free estimates, same-day service available.",
    "schema_desc":"Connect with trusted licensed plumbers in Oklahoma City, OK for emergency plumbing, drain cleaning, water heater repair, leak detection, and more.",
    "faq":[
      ("How much do plumbers charge per hour in Oklahoma City?","Plumbing rates in Oklahoma City, OK typically range from $70 to $130 per hour. Emergency services may cost more. Free written estimates are always provided before work begins."),
      ("What is the best plumbing company in Oklahoma City?","PlumbersInUSA.com connects you with multiple licensed, insured, and top-rated plumbing professionals in Oklahoma City so you can compare options and choose the best fit."),
      ("Do Oklahoma City plumbers offer same-day service?","Yes. Most licensed plumbers in Oklahoma City offer same-day and 24/7 emergency service for urgent issues including burst pipes, clogged drains, and water heater failures."),
      ("Are Oklahoma City plumbers licensed in Oklahoma?","Yes. All plumbing professionals connected through PlumbersInUSA.com serving Oklahoma City are fully licensed, bonded, and insured in the state of Oklahoma."),
      ("What areas of Oklahoma City do local plumbers serve?","Local plumbers serve all Oklahoma City neighborhoods including Edmond, Norman, Moore, Midwest City, Del City, Yukon, Nichols Hills, and Bricktown."),
    ]
  },
  {
    "dir":"plumber-portland-or","city":"Portland","state":"OR","state_full":"Oregon",
    "title":"Licensed Plumbers in Portland, OR | 24/7 Emergency Service | Free Estimates",
    "desc":"Find trusted licensed plumbers in Portland, OR. Emergency plumbing, drain cleaning, water heater repair & more. 24/7 service, same-day availability. Free estimates.",
    "kw":"plumbers in portland, portland plumber, emergency plumbing portland or, drain cleaning portland, water heater repair portland, plumber near me portland",
    "h1":"Trusted Plumbers in Portland, OR",
    "hero_sub":"Fast, reliable plumbing services for homes and businesses across Portland, Oregon. Connect with licensed local plumbers for emergency repairs, drain cleaning, water heater services, and more.",
    "intro_h2":"Professional Plumbing Services in Portland, Oregon",
    "intro_sub":"Your trusted local plumbing experts serving Portland and the surrounding metro area",
    "intro_p1":"Portland's heavy rainfall, aging infrastructure — some pipe systems dating back nearly a century — and cold wet winters create constant plumbing demands. Root intrusions from Portland's famous tree canopy are a leading cause of sewer blockages, and occasional ice events can burst exposed pipes. PlumbersInUSA.com connects you with licensed, insured plumbing professionals serving Beaverton, Hillsboro, Gresham, Lake Oswego, Tigard, Vancouver, the Pearl District, and the full Portland metro.",
    "services_h2":"Our Plumbing Services in Portland, OR",
    "services_sub":"Complete plumbing solutions for Portland homes and businesses",
    "cta_h2":"Need a Licensed Plumber in Portland, OR?",
    "cta_sub":"Connect with trusted local plumbers in Portland for residential and commercial plumbing needs. Free estimates, same-day service available.",
    "schema_desc":"Connect with trusted licensed plumbers in Portland, OR for emergency plumbing, drain cleaning, water heater repair, leak detection, and more.",
    "faq":[
      ("How much do plumbers charge per hour in Portland?","Plumbing rates in Portland, OR typically range from $90 to $160 per hour. Emergency services may cost more. Free written estimates are always provided before work begins."),
      ("What is the best plumbing company in Portland?","PlumbersInUSA.com connects you with multiple licensed, insured, and top-rated plumbing professionals in Portland so you can compare options and choose the best fit."),
      ("Do Portland plumbers offer same-day service?","Yes. Most licensed plumbers in Portland offer same-day and 24/7 emergency service for urgent issues including burst pipes, clogged drains, root intrusions, and water heater failures."),
      ("Are Portland plumbers licensed in Oregon?","Yes. All plumbing professionals connected through PlumbersInUSA.com serving Portland are fully licensed, bonded, and insured in the state of Oregon."),
      ("What areas of Portland do local plumbers serve?","Local plumbers serve all Portland neighborhoods including Beaverton, Hillsboro, Gresham, Lake Oswego, Tigard, Vancouver, the Pearl District, Northeast Portland, and Milwaukie."),
    ]
  },
]

def update(city_data):
    path = os.path.join(BASE, city_data["dir"], "index.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    c = city_data["city"]
    s = city_data["state"]
    sf = city_data["state_full"]

    # Meta tags
    html = re.sub(r'<title>.*?</title>', f'<title>{city_data["title"]}</title>', html)
    html = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{city_data["desc"]}">', html)
    html = re.sub(r'<meta name="keywords" content="[^"]*">', f'<meta name="keywords" content="{city_data["kw"]}">', html)
    html = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{city_data["title"]}">', html)
    html = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{city_data["desc"]}">', html)
    html = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{city_data["title"]}">', html)
    html = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{city_data["desc"]}">', html)

    # Schema LocalBusiness description
    html = re.sub(r'"description": "Professional plumbing repair in [^"]*"', f'"description": "{city_data["schema_desc"]}"', html)

    # FAQPage schema
    new_faq_schema = faq_schema(city_data["faq"])
    html = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema\.org",\s*"@type": "FAQPage".*?</script>',
                  f'<script type="application/ld+json">\n{new_faq_schema}\n</script>', html, flags=re.DOTALL)

    # Brand → homepage
    html = re.sub(r'<a class="brand" href="[^"]*" aria-label="[^"]*">.*?</a>',
                  '<a class="brand" href="https://plumbersinusa.com/" aria-label="PlumbersInUSA.com - Home">PlumbersInUSA.com</a>', html)

    # Hero H1
    html = re.sub(r'<h1>Plumbing Repair in [^<]*</h1>', f'<h1>{city_data["h1"]}</h1>', html)

    # Hero subtitle
    html = re.sub(r'<p class="hero-sub">.*?</p>', f'<p class="hero-sub">{city_data["hero_sub"]}</p>', html, count=1, flags=re.DOTALL)

    # Breadcrumb
    html = re.sub(r'<span aria-current="page">Plumbing Repair [^<]*</span>', f'<span aria-current="page">Plumbers in {c}, {s}</span>', html)

    # Intro H2
    html = re.sub(r'<h2 id="intro-heading">.*?</h2>', f'<h2 id="intro-heading">{city_data["intro_h2"]}</h2>', html)

    # Intro section-sub
    html = re.sub(r'(<h2 id="intro-heading">.*?</h2>\s*)<p class="section-sub">.*?</p>',
                  r'\1' + f'<p class="section-sub">{city_data["intro_sub"]}</p>', html, flags=re.DOTALL)

    # Intro body paragraphs
    html = re.sub(r'<p>Looking for reliable.*?(?=<a href="tel:PHONE_NUMBER" class="btn-call")',
                  f'<p>{city_data["intro_p1"]}</p>\n    <br><p>Need plumbing help today? Find trusted plumbers in {c} and request a free estimate.</p>\n    ',
                  html, flags=re.DOTALL)

    # Intro CTA text
    html = html.replace('📞 Call Now — Free Plumbing Repair Quote', f'📞 Connect With a {c} Plumber — Free Estimate', 1)

    # Services H2 and sub
    html = re.sub(r'<h2 id="services-heading">.*?</h2>', f'<h2 id="services-heading">{city_data["services_h2"]}</h2>', html)
    html = re.sub(r'(<h2 id="services-heading">.*?</h2>\s*)<p class="section-sub">.*?</p>',
                  r'\1' + f'<p class="section-sub">{city_data["services_sub"]}</p>', html, flags=re.DOTALL)

    # FAQ H2 and sub
    html = re.sub(r'<h2 id="faq-heading">.*?</h2>', f'<h2 id="faq-heading">Frequently Asked Questions — Plumbers in {c}, {s}</h2>', html)
    html = re.sub(r'(<h2 id="faq-heading">.*?</h2>\s*)<p class="section-sub">.*?</p>',
                  r'\1' + f'<p class="section-sub">Common questions from {c} homeowners and businesses</p>', html, flags=re.DOTALL)

    # FAQ items
    new_faq_items = faq_html(city_data["faq"])
    html = re.sub(r'<div class="faq-list">.*?</div>\s*</div>\s*</section>\s*<section class="cta-banner"',
                  f'<div class="faq-list">\n{new_faq_items}\n    </div>\n  </div>\n</section>\n<section class="cta-banner"',
                  html, flags=re.DOTALL)

    # CTA banner
    html = re.sub(r'(<section class="cta-banner">)\s*<h2>.*?</h2>', r'\1\n  <h2>' + city_data["cta_h2"] + '</h2>', html, flags=re.DOTALL)
    html = re.sub(r'(<section class="cta-banner">.*?<h2>.*?</h2>\s*)<p>.*?</p>',
                  r'\1' + f'<p>{city_data["cta_sub"]}</p>', html, flags=re.DOTALL)

    # Footer first col
    html = re.sub(r'<h4>Plumbing Repair in [^<]*</h4>', f'<h4>Plumbers in {c}, {s}</h4>', html, count=1)
    html = re.sub(r'<p style="font-size:\.92em;color:#94a3b8;line-height:1\.7">Licensed &amp; insured plumbing repair professionals serving.*?</p>',
                  f'<p style="font-size:.92em;color:#94a3b8;line-height:1.7">Connecting homeowners and businesses with trusted licensed plumbers in {c}, {sf} and surrounding areas. Available 24/7.</p>',
                  html, flags=re.DOTALL)
    html = re.sub(r'<p>&copy; 2026 Plumbing Repair Services in [^<]*</p>',
                  f'<p>&copy; 2026 PlumbersInUSA.com &mdash; Trusted Plumbers in {c}, {sf}. All rights reserved.</p>', html)

    # Hero aria-label
    html = re.sub(r'aria-label="Plumbing Repair in [^"]*"', f'aria-label="Trusted Plumbers in {c}, {s}"', html, count=1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  OK  {city_data['dir']}")

print("Updating 20 city pages...")
for city in CITIES:
    try:
        update(city)
    except Exception as e:
        print(f"  ERR {city['dir']}: {e}")
print("Done.")
