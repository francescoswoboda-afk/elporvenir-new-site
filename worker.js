// Cloudflare Worker: serves the static site in public/ and handles the contact form.
// Static files are served directly; the Worker only runs for paths that aren't a file, like /api/contact.
import { onRequestPost } from "./functions/api/contact.js";

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === "/api/contact") {
      if (request.method === "OPTIONS") {
        return new Response(null, { status: 204, headers: {
          "Access-Control-Allow-Origin": request.headers.get("Origin") || "*",
          "Access-Control-Allow-Methods": "POST", "Access-Control-Allow-Headers": "Accept", "Access-Control-Max-Age": "86400", Vary: "Origin" } });
      }
      if (request.method !== "POST") return new Response("Method not allowed", { status: 405, headers: { Allow: "POST" } });
      return onRequestPost({ request, env, ctx });
    }
    return env.ASSETS.fetch(request);
  },
};
