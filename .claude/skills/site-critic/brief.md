Build the new website for El Porvenir Farm, a pecan farm in southern Brazil, and make it the kind of site that wins awards. This is your portfolio piece as a creative developer and motion designer. Go all in: every scroll, hover and click should feel designed. If it looks like a template, start again.

WHAT THIS SITE IS
This is a showcase website. Its only job is to present El Porvenir Farm: the land, the trees, the seasons, the work and the family. It does not sell anything, it does not ask for quotes and it is not a product catalogue. Think of it as an exhibition or a beautiful digital book about the farm. Visitors should leave feeling they have been there.

THE FARM
- El Porvenir Farm is a family-owned pecan plantation in Rio Grande do Sul, southern Brazil, with around 6,000 pecan trees [VERIFY the number]. The region has four real seasons and cold winters.
- It is run by Enrique Swoboda, with his sons Francesco and Alessandro working on the European side.
- The website is www.elporvenir.farm. Use the attached logo, photos and any existing site content as the source of truth. Anything I have not given you is a visible placeholder marked [TBD] or [VERIFY].

THE CORE IDEA (read twice)
The site should make El Porvenir feel like a real place with a soul, not just a farm with trees. Every section should make the visitor feel the land, the time it takes to grow a pecan and the care of the people who do it. Before building any section, ask: "Does this make someone feel what El Porvenir is?" If the answer is no, cut it or redesign it.

THE TREE IS THE CHARACTER
The site has a living pecan tree, built in code (SVG, canvas or three.js), that acts as the visual thread through the whole site.
- In the hero, it grows from a seed into a full tree as the page loads, with branches drawn procedurally.
- As the visitor scrolls, the tree goes through the four seasons of the farm year: bare winter branches, spring buds and catkins, green summer canopy with husks forming, autumn harvest with husks splitting open and nuts falling.
- Leaves move gently in a procedural wind that reacts to the cursor (or to touch on mobile).
- Falling pecans can be clicked or caught for a small, delightful moment.
- At the end of the site, the single tree becomes a full orchard in rows, showing the scale of the farm.
- Hide at least one easter egg in the tree.

NAVIGATION (must be exactly like this)
- The navigation bar sits on the right side of the screen, like the macOS Dock: a slim strip that opens into a full menu when the cursor comes near it.
- Dark or black background, page names in white that turn yellow on hover, with a smooth magnification effect on the items like the Dock.
- It stays in the same place on every page.
- Clicking a menu link (for example About Us) brings that page up from the bottom, so the whole site feels like one seamless page that scrolls, with smooth transitions. No hard page reloads.
- On mobile, turn it into an equally smooth version that works with a thumb (for example a tab on the right edge that slides the menu out), and keep the yellow active state.

SITE STRUCTURE (improve on this if you have a better idea, and say why in the decisions file)
1. Home: the tree growing, the farm name, and one strong line about what El Porvenir is.
2. About us: the family and the story of the farm. Use placeholder text marked [TBD] for history, dates and anecdotes. Do not invent any.
3. The land: Rio Grande do Sul, the climate, the soil and the landscape, with an animated map that zooms from South America down to the farm.
4. The orchard year: a scroll-driven journey through the four seasons on the farm, from winter pruning to flowering, growth and harvest, told through the tree and simple animated scenes.
5. From tree to nut: a calm, beautiful animated sequence of what happens after harvest (collecting, drying, cleaning, sorting), as storytelling, not as a technical specification.
6. Gallery: the photos I attach, presented like an exhibition, with a smooth full-screen viewer and subtle motion. If I attach no photos, design the section so it is ready for them and leave clear [TBD] frames.
7. The farm in numbers: a few large animated numbers (trees, hectares, years, harvest seasons) that count up as they come into view. All values are [TBD] or [VERIFY] until I give them.
8. Contact: just a simple, elegant way to reach the farm (email, phone, WhatsApp, address as [TBD]). No forms needed.
9. Footer: the orchard at rest, the logo, and legal pages (privacy, imprint) as [TBD] placeholders.

TYPOGRAPHY (study it, don't just pick a font)
- Start from the farm's logo and identity: earthy, honest, established, but modern.
- Explore at least three different type directions before choosing (for example: agricultural heritage, warm editorial, modern and minimal). For each, pair a display face with a text face, set a real headline, a paragraph and a large number in it, and compare them in screenshots. Pick one and explain why in the decisions file, including what you rejected.
- Use Google Fonts only. Check that the fonts fully support English, Portuguese and Spanish characters (ç, ã, õ, ñ, á, é).
- Build a clear type scale (fluid sizes with clamp()), with defined line heights, letter spacing and weights for every level.
- Let the type move where it adds meaning (headlines revealing per letter or word, variable-font weight shifts), but body text must be calm and very readable.

LANGUAGE
- English by default, with a working toggle to Portuguese and Spanish. The toggle keeps the visitor on the same section.

MOTION AND CRAFT
- Use GSAP with ScrollTrigger and smooth scrolling (Lenis or similar). three.js is allowed where 3D genuinely adds something. Load libraries only from cdnjs.cloudflare.com, cdn.jsdelivr.net or unpkg.com.
- Choreograph the site like a film: easing curves chosen on purpose, staggered reveals, seasonal colour shifts across the whole page as the year passes, light that changes from morning to evening, a custom cursor, subtle grain or paper texture.
- Optional ambient soundscape (wind in the leaves, birds, a soft crack when a nut is clicked) synthesized from scratch with the Web Audio API. No samples. Sound is OFF by default, with a clear toggle.

HARD CONSTRAINTS
- Code only. No image, video or audio generation models, no stock photos. Everything visual is drawn in code, except the logo and photos I attach.
- Honesty: no invented history, numbers, awards, certifications or quotes. Anything I need to supply is a visible placeholder marked [TBD] or [VERIFY].
- Performance: smooth 60 frames per second on a normal laptop, fast first load, no layout shift. Start heavy animations only when they come into view.
- Mobile: fully designed for phones, not just shrunk. Touch versions of every interaction.
- Accessibility: respects prefers-reduced-motion (the tree still exists but changes calmly), keyboard navigable (including the right-side navigation and the gallery), readable contrast in every season's colours.

PROCESS
- Work in at least four passes: structure and story; typography study and visual system; motion, the tree and the navigation; polish.
- After each pass, take screenshots at desktop (1440px) and mobile (390px) widths, look at them critically like an art director, and fix what is weak before moving on. Test the navigation and the gallery on both sizes.
- Deliver the site as a single self-contained index.html (published as an artifact so I can open it with a link).

DELIVERABLES
1. The website (index.html, published).
2. DECISIONES.md, written in Spanish, explaining what you decided and why, the typography study (the directions you explored, what you chose and what you rejected), what else you discarded, how each iteration changed the site, and the total time spent.
