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