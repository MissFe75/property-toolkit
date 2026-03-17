# Property Compass — Project Progress
Last updated: 17 March 2026 (evening)

## About
- Owner: Fiona Graham (Miss Fe!)
- Business: Sextant Digital
- Domain: sextantdigital.com.au ✅ LIVE
- Email: hello@sextantdigital.com.au ✅ WORKING
- Backup email: sextantdigital@gmail.com
- Forwarding: hello@ → sextantdigital@gmail.com ✅

## App Details
- App name: Property Compass
- App URL: propertycompass.streamlit.app ✅ LIVE
- Main file: app.py
- Location: Desktop/property-toolkit/
- Images: Desktop/property-toolkit/images/
- Language: Python / Streamlit

## Landing Page Details
- File: index.html
- Location: Desktop/sextant-landing-page/
- GitHub repo: github.com/MissFe75/sextant-landing-page
- Hosted on: Cloudflare Pages ✅ LIVE
- URL: sextantdigital.com.au ✅

## Design System
- Background: cream/beige #F5F0E8
- Accent colour: slate blue #3D5A80
- Font: Inter
- Style: clean, minimal, professional

## Infrastructure
- Domain registrar: Crazy Domains
- DNS manager: Cloudflare (FREE) ✅
- Landing page host: Cloudflare Pages (FREE) ✅
- App host: Streamlit Community Cloud (FREE) ✅
- Code storage: GitHub (FREE) ✅
- Email: Zoho Mail Lite (yearly plan) ✅

## Accounts & Logins
- Cloudflare: sextantdigital@gmail.com
- GitHub: missfe75 / fgraham3116@gmail.com
- Streamlit: missfe75 / fgraham3116@gmail.com
- Zoho: hello@sextantdigital.com.au
- Crazy Domains: domain only, DNS moved to Cloudflare
- Google Analytics: sextantdigital@gmail.com

## Features Built ✅
- Mortgage Calculator (P&I and Interest Only)
- Rental Yield Calculator
- Property Analyser
- CGT Estimator
- Compare Properties
- Save as PDF on every page
- Hero images on all pages including piggybank 🐷
- Fortnightly repayments
- Slim slate blue branding banner
- Compass SVG icon in sidebar
- Live on Streamlit Cloud ✅

## Landing Page ✅
- Clean nav bar with compass icon
- Three houses hero image
- Free tools description section
- Example metrics card mock-up
- Trust tiles with clean SVG icons
- Five feature cards
- Footer with email link
- Google Analytics added
- Launch App button → propertycompass.streamlit.app
- Live on Cloudflare Pages ✅

## Email Setup ✅
- Zoho Mail Lite — hello@sextantdigital.com.au
- MX records in Cloudflare ✅
- SPF record in Cloudflare ✅
- DKIM record added via Zoho auto-configure ✅
- Forwarding to sextantdigital@gmail.com ✅
- Emails arriving — currently going to Gmail spam
  (will improve as domain gets trusted over time)

## Completed Today 🎉
- 🐷 Fixed piggybank hero image on Property Analyser
- 🌐 Set up Cloudflare as DNS manager
- 🚀 Deployed landing page to Cloudflare Pages
- 📧 Fixed email — SPF, DKIM, MX all configured
- 🔗 Fixed Launch App button URL
- ✅ Tested everything end to end

## Mobile Fixes — 17 March 2026 📱
### Landing page (sextantdigital.com.au)
- ✅ Logo no longer squished on mobile — "by Sextant Digital" sub-text hidden on small screens
- ✅ Updated nav sub-text to tagline: "Calculators for buying and investing in Aussie property"
- ✅ Header grows naturally on mobile to fit content, no overlap with hero image
- ✅ Features nav button hidden on very small screens (only Launch App remains)

### App (propertycompass.streamlit.app)
- ✅ Custom banner header: tagline wraps neatly on mobile with line break after "investing in"
- ✅ "by Sextant Digital ·" prefix hidden on mobile so tagline starts cleanly with "Calculators"
- ✅ App body offset adjusted to 84px on mobile to sit below taller header
- ✅ Sidebar toggle: injected persistent ☰ hamburger button via components.html + JavaScript
  — button lives on document.body outside React's tree so it survives all Streamlit re-renders
  — setInterval recreates it every 500ms if ever removed
  — slate blue #3D5A80, pinned left edge at top:84px, always accessible

## Still To Do 📋
- General design tweaks to app
- Google will index sextantdigital.com.au 
  over next few weeks automatically
- Mark test emails as "not spam" in Gmail 
  a few times to train Gmail to trust the domain
```

---

**📋 READY TO USE INSTRUCTION — copy into Claude Code:**
