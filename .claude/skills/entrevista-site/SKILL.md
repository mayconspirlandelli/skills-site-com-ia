---
name: entrevista-site
description: Runs the interview for a new website or landing page in rounds of questions, each with a recommended answer — business, goal, audience, pages, architecture (HTML/CSS, Tailwind, Vite, frameworks), hosting, Docker, design (colors, typography, mobile) and reference sites/screenshots — and produces briefing.md for the user's approval. Use in step 1 of the workflow, whenever the user starts a website/landing page project, wants to "make a site", lists inspiration sites, or when etapas/00_briefing/briefing.md doesn't exist yet or isn't approved.
---

# Interview and briefing (step 1)

Goal: leave this step with `etapas/00_briefing/briefing.md` **approved by the user**, answering what we will build, for whom, with which technology, where it will run, what it will look like and what inspired it. The rest of the workflow reads this file; a gap here becomes a guess later on.

## Method: rounds with a recommended answer

Interview until you reach a shared understanding, without silently assuming anything.

- **Think in a decision tree.** Some answers depend on others (hosting depends on architecture; architecture depends on the type of site). In each round, ask only what can already be answered without guessing answers you haven't heard yet.
- **Short rounds.** 3 to 6 numbered questions per round. Wait for the answers before the next round.
- **Always with a recommendation.** Each question comes with your recommended answer and a half-sentence reason. Phrase the question so that "yes" accepts the recommendation — this lets the user quickly answer what they have no strong opinion on.
- **Look up facts yourself.** If the user already gave the information (in this conversation, in a file, on their site), don't ask again. If they mention an existing company site, open and read it before asking about brand and content.
- **Decisions belong to the user.** Put each decision to them and wait. "I don't know" becomes `to be defined` — except for the required items (below), where you explain the impact and propose a choice.

Format of each round:

```
**Round N — <topic>**

❓ **Q1 — <short title>**: <question, with options when helpful>
➡️ I recommend: <answer> — <short reason>

❓ **Q2 — ...**
➡️ I recommend: ...
```

## Script

Cover every block. The order below respects the dependencies; combine blocks in the same round when their questions are already unlocked.

### A. Business and type of site
- Business domain: what the company/project does, what it offers, what sets it apart.
- Type: landing page (one page, one goal), company site (several pages), portfolio, blog, catalog.
- Is there an existing site or brand (logo, brand guide)? If so, ask for the link and read it.
- Competitors or similar projects the user knows.

### B. Goal
- Main action the visitor should take (buy, book, fill a form, message on WhatsApp, download, sign up).
- Secondary goals and how to measure them (form submitted, CTA clicks, analytics).

### C. Audience
- Who visits: profile, what they look for, what convinces them.
- Usage context: mostly mobile or desktop? Language(s)?
- Accessibility needs (older audience, low vision, screen readers).

### D. Pages, content and features
- Pages and, for each, the planned sections (for a landing page: the sections of the single page).
- Available content: text, logo, photos, testimonials, numbers. Whatever is missing becomes a placeholder.
- Features: contact form, WhatsApp, newsletter, map, blog, members area, multilingual, analytics.
- Animations or videos? (If so, the setup step installs the animation skills.)

### E. Architecture
- Stack: plain HTML + CSS · HTML + Tailwind · Vite (with or without React/Vue/Svelte) · Astro · Next.js · other.
- Does it need a CMS or for the client to edit content themselves?
- Does SEO matter (public site that needs to be found on Google)?
- Default recommendation: landing page or simple static site → **HTML + Tailwind** (or **Vite + Tailwind** for a build step and components); many content pages → **Astro**; heavy interactivity or an app → **Vite + React** or **Next.js**.

### F. Hosting and delivery
- Where it will run: GitHub Pages · Netlify · Vercel · Cloudflare Pages · VPS/own server · institution's server.
- Will it run in **Docker**? (Common on a VPS or own server: a static site served by Nginx in a container.)
- Own domain? Automatic deploy on every push (CI/CD)?

### G. Design
- Colors they like and dislike; mandatory brand colors (ask for the hex codes, if any).
- Typography: serif, sans-serif, geometric, handwritten? Any specific font?
- Visual tone: minimalist, sober, warm, premium, technical, playful, academic...
- Dark mode?
- Mobile: just a **responsive layout** (default, mobile-first) or also an **installable app (PWA)**?

### H. References
- **3 to 5 reference sites** (URLs, ideally of specific pages, not just the home page). For each: **what to take**, **what to avoid** and the main aspect (layout, typography, colors, spacing, content). A URL without a reason makes the AI copy everything, including what the user dislikes — if they can't explain, offer concrete options.
- **Screenshots** of sites they like. The next steps need the **files**: ask them to save them in `etapas/00_briefing/prints/` with descriptive names (`ref1_hero.png`, `ref2_footer.png`). If they paste images in the chat, describe what you see, use it in the conversation and ask them to save the files in the folder.

### Required items (cannot stay "to be defined")
Type of site, main goal, audience, list of pages/sections, stack and hosting. If the user doesn't know, explain the impact in one sentence and propose a choice for them to accept.

## Output

Generate `etapas/00_briefing/briefing.md` from `assets/briefing_template.md`. Rules:

- Record the user's answers, not your recommendation, when they chose something else.
- Mark with `(recommendation accepted)` whatever came from a recommendation accepted with "yes" — it helps when reviewing later.
- List the screenshots received with their file paths.
- Open items go to the **To be defined** section, each with the step by which it must be resolved.

## Validation before asking for approval

- All blocks A–H were covered and the required items are defined.
- Every reference has "take" and "avoid".
- No obvious contradiction (e.g. "minimalist" + a reference chosen for its heavy animations; "GitHub Pages" + "Next.js with a server"; "Docker" + hosting that doesn't use containers). If there is one, point it out and resolve it with the user.
- Every page has at least one associated layout reference (or the decision to have none).

## Approval

Show a summary of the briefing (one line per block) and the file path, and ask whether they approve or what they want to change. Adjust until they explicitly approve. Once approved, record it in `etapas/aprovacoes.md` (step 1, `00_briefing/briefing.md`, `approved`, date). If there are no URLs, record step 2 as `not applicable`; if there are no screenshots, step 3.

If the interview indicated animations or videos, remind the user to run `./scripts/setup-skills.sh animacao`.

Next step: `extrair-html-referencia` (step 2).
