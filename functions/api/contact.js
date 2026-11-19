// Cloudflare Pages Function: POST /api/contact
// Sends the contact form to the farm inbox through Resend (https://resend.com).
//
// Settings in Cloudflare Pages → Settings → Variables and secrets:
//   RESEND_API_KEY  (secret)   the Resend API key
//   MAIL_TO         (optional) where messages go, default info@elporvenir.farm
//   MAIL_FROM       (optional) sender, default "El Porvenir website <website@elporvenir.farm>"
//                              (the elporvenir.farm domain must be verified in Resend)

const TOPICS = {
  pecans: "Buying pecans",
  honey: "Buying honey",
  visit: "Visiting the farm",
  press: "Press or partnerships",
  other: "Something else",
};
const LANGS = { en: "/", pt: "/pt/", es: "/es/" };

// The site lives on www.elporvenir.farm (GitHub Pages) and posts the form here.
const ALLOWED = ["https://www.elporvenir.farm", "https://elporvenir.farm", "https://elporvenir.francesco-swoboda.workers.dev"];
function siteOrigin(request) {
  const o = request.headers.get("Origin") || "";
  if (ALLOWED.includes(o)) return o;
  const r = request.headers.get("Referer") || "";
  return ALLOWED.find((a) => r.startsWith(a + "/")) || null;
}

function reply(request, ok, status, lang) {
  const wantsJson = (request.headers.get("Accept") || "").includes("application/json");
  const origin = siteOrigin(request);
  if (wantsJson) {
    const headers = { "Content-Type": "application/json", "Cache-Control": "no-store", Vary: "Origin" };
    if (origin) headers["Access-Control-Allow-Origin"] = origin;
    return new Response(JSON.stringify({ ok }), { status, headers });
  }
  // Without JavaScript the browser posts the form directly: send people back to the page.
  const base = LANGS[lang] || "/";
  return Response.redirect(new URL(`${base}${ok ? "sent" : "not-sent"}/`, origin || request.url).toString(), 303);
}

const clean = (v, max) => String(v || "").replace(/\r/g, "").trim().slice(0, max);
const esc = (s) => s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

export async function onRequestPost({ request, env }) {
  let data;
  try {
    data = await request.formData();
  } catch {
    return reply(request, false, 400, "en");
  }
  const lang = clean(data.get("lang"), 4);

  // Spam checks: the hidden "website" field must stay empty, and a person takes more than 3 seconds.
  if (clean(data.get("website"), 200)) return reply(request, true, 200, lang);
  const t = Number(data.get("t"));
  if (t && Date.now() - t < 3000) return reply(request, true, 200, lang);

  const name = clean(data.get("name"), 120);
  const email = clean(data.get("email"), 200);
  const message = clean(data.get("message"), 5000);
  const topic = TOPICS[clean(data.get("topic"), 20)] || TOPICS.other;
  if (!name || !message || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return reply(request, false, 422, lang);
  }
  if (!env.RESEND_API_KEY) return reply(request, false, 503, lang);

  const text = `${topic}\n\nFrom: ${name} <${email}>\nLanguage: ${lang || "en"}\n\n${message}`;
  const html = `<p><strong>${esc(topic)}</strong></p><p>From: ${esc(name)} &lt;${esc(email)}&gt;<br>Language: ${esc(lang || "en")}</p><p style="white-space:pre-wrap">${esc(message)}</p>`;

  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      from: env.MAIL_FROM || "El Porvenir website <website@elporvenir.farm>",
      to: [env.MAIL_TO || "info@elporvenir.farm"],
      reply_to: email,
      subject: `Website: ${topic} — ${name}`,
      text,
      html,
    }),
  });
  return reply(request, res.ok, res.ok ? 200 : 502, lang);
}

export function onRequest() {
  return new Response("Method not allowed", { status: 405, headers: { Allow: "POST" } });
}
