# The Business Stick HQ — YouTube/TikTok/IG/FB business-stories channel

When giving the user posting instructions for any app, ALWAYS include every setting in
`channel/POSTING-SETTINGS.md` (AI label ON for TikTok/Instagram/Facebook, Identify similar products OFF,
Trial reel OFF, Related video on every YouTube Short, etc.). Keep it step-by-step and simple.

- Hooks and script structure: follow the script template in `channel/SHORTS-PLAYBOOK.md` (question hook by default, payoff-statement variant ~3 in 10). Old template files are archived in `channel/archive/` (superseded; do not use).
- Always quote Higgsfield credit cost and wait for OK before spending.
- User prefers PDFs over .md for documents.
- Weekly formula and per-day captions: `videos/costco-hot-dog/shorts/POSTING-PLAN.md`.

## 30-day Shorts plan (1 Short per day, best possible quality + SEO)
READ `channel/SHORTS-PLAYBOOK.md` at the start of every chat. It is the script template (skeleton with the perfect-loop ending, loop rules, on-screen rules, title/captions, posting checklist, monetization guardrails) for every daily Short. Do not spend credits without quoting the cost first.

- Video ideas ALWAYS come from vidIQ trending searches: generate the top 10 ideas, never repeating a video already made (check channel/SHORTS-LOG.md, which also lists what is already on the YouTube channel).
- The playbook is the single source of truth for new shorts; if another file conflicts with it, the playbook wins, except the posting settings (`channel/POSTING-SETTINGS.md` and this file still apply; if a setting conflicts with the playbook, flag it and ask).
- BS numbers come from `channel/SHORTS-LOG.md` (next number = highest used + 1).

## Film #2 "POV: You Became the #1 Streamer Overnight." — standing production rules (from Muse, 2026-11-10)
Single source of truth for Film #2: `film2-assets/STATE.md` on this branch (`claude/happy-mccarthy-4tfabg`). READ IT at the start of every Film #2 chat.

### Sections 3-6 pacing (supersedes the density used on Sections 1-2)
Sections 1-2 are the retention-critical front of the film and got the full treatment. Sections 3-6 run LENIENT, at the Chick-fil-A standard:
- FEWER images. Multiple script lines ride ONE image.
- Every shot stays UNDER 10 seconds.
- A new image happens ONLY when the beat truly changes: new idea, new proof, new number, new person, new emotion. Never a new shot every 2-4 seconds by default.
- Grouping test: the lines grouped onto an image must FIT that image's meaning.
- Exception: a single line may run over 10 s when the line itself carries the hold (a reveal with its payoff withheld to the end). Prefer ONE free assembly state at the payoff moment over a new generation. If a grouped shot would feel dragged even with a state change, FLAG it in the map; do not silently add images.
- Decided example: VO-095 (11.60 s, the Mixer/Ninja line) holds on ONE image, with the money figure landing as a free state at "between twenty and thirty million dollars."

### Process rules (learned from Sections 1-2: ~5 hours for 57 shots, much of it avoidable)
- CONSISTENCY OVER CREATIVITY. The screen vocabulary is locked as reusable assets; never invent a new screen design for a shot.
  - STREAM screen = his face preview (his EXACT face from that shot) + white viewer-icon column + colored chat bars.
  - COUNTER screen = person icon + the number + colored name pills / gray bars on the right (NO white icons; those belong to the stream screen only).
- Pass/fail checks go INSIDE the generation prompt: exact on-screen text whitelist (nothing readable that isn't listed), LIVE on/off state per the story timeline, digit-legibility test where blur is required, face anatomy (one eyebrow per eye, connected head outline).
- PREFLIGHT before any paid call: (1) master attached, (2) reference attached, (3) live price confirmed (get_cost). A call missing its attachments wasted 1.00 once; never again.
- Screen fixes and simple fixes are LOCAL COMPOSITES FIRST (genuine assets pasted in); the model redraws screens worse than the real assets composite. Model edits only when a composite can't do it, and only with a stated cost.
- One prompt per job with a hard spend cap. No re-rolls without Dominick's OK. If a generation fails its stated check, stop and report; never auto-retry.
- Repo discipline: every approved file committed to the canonical branch as it is approved; STATE.md updated at the end of every chat; storyboard sheets in the v4 format and DISPLAYED in the chat, not just committed.
- Review bar for Sections 3-6: cartoon-good passes. Only meaning failures, wrong text, broken anatomy, or wrong screen design come back for fixes.
- Standing basics (unchanged): quote credit cost and wait for OK before any spend; gpt_image_2_5 16:9 2k medium = 1.00/image; masters 1920x1080 PNG; every delivered file under 25 MB; documents as PDF.
