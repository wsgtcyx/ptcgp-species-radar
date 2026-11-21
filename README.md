# PTCG Pocket Missing Species Radar

A static, agent-readable audit of Pokémon TCG Pocket deck/species-page opportunities. Trial research cutoff: 2026-11-21 17:32:57 China Standard Time.

## Data entry points

- `latest.json` — machine-readable latest result; use this when querying as an AI agent.
- `history/YYYY-MM-DD.json` — immutable daily snapshots.
- `latest.md` — human-readable research report.
- `index.html` — responsive static research dashboard.

Schema: `status=partial_verified` means some source coverage is incomplete; `null` is unknown, not zero. Source entries have `directly_opened`, `published_at_precision`, and author metadata for verification. Always check those flags before deciding to build a new SEO page.

## Deploy to GitHub Pages

1. Repository: `wsgtcyx/ptcgp-species-radar`; files are committed to its default branch.
2. Go to repository `Settings` → `Pages` → `Build and deployment`, choose `Deploy from a branch`, branch `main`, folder `/ (root)`, then Save.
3. After GitHub confirms deployment, the public URLs are normally `https://<owner>.github.io/<repo>/` and `https://<owner>.github.io/<repo>/latest.json`. Verify them before passing to agents.

The public GitHub repository exists, but GitHub Pages hosting has not been enabled or verified. The connected GitHub app has file-writing APIs but no create-repository or Pages-settings operation. A separate authorized deployment integration is needed for automated daily publication; ChatGPT automation currently only runs the research.

## Source policy

Time window strictly 72h, both Reddit and X attempted, physical TCG excluded, per-species author dedup, species-directory pages excluded including archived forms, all available pagination links traversed. Do not infer growth without a same-method historical baseline. Distinguish species overview pages from generic deck-detail pages. A failed source fetch must be marked unknown rather than `0`.

## License

Research material and site design produced for this deployment. Pokémon and Pokémon TCG Pocket are third-party trademarks. This independent research dashboard is not affiliated with their owners.

## Daily research and publishing contract

A ChatGPT task named **PTCG Pocket 新物种选题雷达** is scheduled for **10:00 Asia/Shanghai every day**.

Its end-to-end target:

1. Search the latest **72 hours** of actual Pokémon TCG Pocket deck-building discussions on **Reddit and X**, with verified author, direct source URL, timestamp, card form and explicit deck intent. Deduplicate per species per author; exclude physical TCG, duplicate content and species already appearing in all pages of the site's species directory.
2. Produce **five distinct missing-species deck-page build candidates** when evidence supports them. At least one directly verifiable relevant discussion in the 72-hour window is required for the confirmed build-candidate list. Mark single-author interest as limited evidence, not confirmed growth. Never claim five qualified items if fewer meet those tests. Put weaker leads separately in `watchlist`; record `qualified_count`, `target_count: 5` and the shortfall.
3. Publish the completed research to `latest.json`, `latest.md` and a dated `history/` snapshot using authenticated GitHub writes. The static `index.html` reads `latest.json` dynamically.
4. Read back the committed JSON, check the GitHub Pages deployment result for the **new commit**, and when possible fetch the public `latest.json` over HTTP to verify the published timestamp. Distinguish commit success from repository readback, Pages deployment, and public HTTP verification. Do not report public publishing as successful without evidence for each stage.
5. On failed research or publication, report the precise blocker and **do not replace a previously good latest snapshot with an empty or fabricated result**.

The target public endpoints are:

- Web: https://wsgtcyx.github.io/ptcgp-species-radar/
- JSON: https://wsgtcyx.github.io/ptcgp-species-radar/latest.json

**Operational caveat:** The task prompt configures the desired GitHub-publishing steps, but an end-to-end **scheduled** run has not yet demonstrated that the automation execution environment can use the GitHub connection and verify the latest Pages deployment. Check its first scheduled run before treating daily updates as reliable.

