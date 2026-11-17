// Copy only the files the live site needs into public/ (what Cloudflare uploads).
const fs = require("fs"), path = require("path");
const root = path.join(__dirname, ".."), out = path.join(root, "public");
const FILES = ["index.html", "favicon.ico", "apple-touch-icon.png"];

fs.rmSync(out, { recursive: true, force: true });
fs.mkdirSync(out);
for (const f of FILES) fs.copyFileSync(path.join(root, f), path.join(out, f));
console.log("staged", FILES.join(", "), "into public/");
