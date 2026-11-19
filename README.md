# elporvenir.farm

The El Porvenir website: a static site with one small serverless function for the contact form, built for Cloudflare.

## What's here

| Path | What it is |
| --- | --- |
| `src/strings.py` | All the text in English, Portuguese and Spanish. Edit words here. |
| `src/template.html` | The page layout, styles and script. |
| `src/build.py` | Builds the pages into `public/`. Run `python3 src/build.py` after any edit. |
| `public/` | The finished site that Cloudflare serves: `/`, `/pt/`, `/es/`, images, fonts, `sitemap.xml`, `robots.txt`, `_headers`. |
| `functions/api/contact.js` | Receives the contact form at `/api/contact` and emails it to info@elporvenir.farm. |
| `worker.js`, `wrangler.jsonc` | The Cloudflare Worker that serves the site and runs the form. |
| `.claude/skills/` | Design skills for Claude Code (Impeccable, site-critic and others). |

Images come in AVIF, WebP and JPEG at three widths, so each phone or screen downloads only the size it needs. Fonts (Inter and Inter Display) are hosted on the site itself, with no Google Fonts request. Anyone whose device is set to "reduce motion" gets the site with no animations.

## Run it on your computer

Needs Node.js. In VS Code open a terminal (Terminal → New Terminal) and run:

```
npm run dev
```

Then open the address it prints (usually http://localhost:8787). After editing text in `src/strings.py`, run `python src/build.py` to rebuild `public/`.

## Put it online (Cloudflare Workers)

This uses the same Cloudflare Worker, `elporvenir`, as before.

1. `npx wrangler login` once, to sign in to Cloudflare in the browser.
2. `npm run deploy`
3. In Cloudflare → Workers & Pages → elporvenir → Settings → Domains & Routes, add `www.elporvenir.farm` and `elporvenir.farm` if they aren't there yet.

## Make the contact form send email

The form uses [Resend](https://resend.com), which is free up to 3,000 emails a month.

1. Create a Resend account and add the domain `elporvenir.farm` under **Domains**. Add the DNS records it shows (one click if the domain is on Cloudflare).
2. Create an API key in Resend.
3. Run `npx wrangler secret put RESEND_API_KEY` and paste the key. Optional variables: `MAIL_TO` (default info@elporvenir.farm) and `MAIL_FROM` (default `El Porvenir website <website@elporvenir.farm>`).
4. Send a test message from the live site.

Every message arrives with **Reply-To** set to the visitor's address. Spam protection: a hidden field bots fill in, and forms sent within 3 seconds of loading are rejected. Without JavaScript the form still works and shows a "sent" or "not sent" page in the visitor's language.

## Before launch

- [ ] A native speaker checks the Portuguese and Spanish (see the "Copy" tab of the project brief)
- [ ] The family approves the quote line
- [ ] Swap the placeholder photos for the seasonal shoot (see the "Shot list" tab); the house photo is small and soft at large sizes
- [ ] Redrawn landscape concept drawings, if they're to be shown
- [ ] Add a "Domain" property for elporvenir.farm in Search Console and submit `https://www.elporvenir.farm/sitemap.xml`
