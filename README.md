# jlw-newsletter

A Python static-site newsletter generator. It turns per-issue newsletter HTML
files (plus images, audio, and video) into a published static site — an
`index.html` landing page, RSS/podcast feeds, and SEO files — that is deployed
to **Cloudflare Pages**. This repository holds only the code and configuration;
the generated content lives outside it (see `DEPENDENCIES.md`).

## Build → deploy flow

The pipeline is two steps. Build first, then deploy.

1. **`scripts/build.sh [CONTENT_DIR]`** regenerates all derived content against
   the content directory (defaults to `$DEPLOY_DIR`, else `~/clawd/jlw-newsletter`):
   - `index.html` plus `sitemap.xml` / `robots.txt` / `favicon.svg` — via `scripts/generate_index.py`
   - `articles.rss` — via `scripts/generate_articles_rss.py`
   - `podcast.rss` — via `scripts/generate_podcast_rss.py` (tolerant: skipped when
     `podcast_feed.json`, the `audio/` dir, or mp3s are absent)
   - optional image optimization with `--optimize-images` — via `scripts/optimize_images.py`

   Pass `--deploy` to chain straight into the deploy step.

2. **`scripts/deploy.sh`** publishes `~/clawd/jlw-newsletter/` to Cloudflare
   Pages production. It rsyncs the content (excluding WAVs, videos, scripts, and
   dev files) to a temp dir, refuses to deploy if `index.html` is missing or the
   sync looks empty, then runs `wrangler pages deploy` with **`--branch=main`**
   (required — without it the deploy goes to Preview, not Production) and
   verifies the live site returns HTTP 200.

```sh
./scripts/build.sh                 # regenerate index + feeds + sitemap
./scripts/build.sh --deploy        # build, then publish to Cloudflare Pages
./scripts/deploy.sh                # publish only
```

## Required environment / secrets

- **`GEMINI_API_KEY`** — required by `generate_images.py` (Gemini image generation).
- **`cloudflare-pages-token` (macOS Keychain)** — `scripts/deploy.sh` reads the
  Cloudflare API token from the Keychain entry named `cloudflare-pages-token`
  (account `welshofer`) via `security find-generic-password`.
- **`JLW_OUTPUT_DIR`** — optional; overrides the chart/image generators' output
  base directory (default `~/clawd/jlw-newsletter`). See `chart_style.py`.

See `DEPENDENCIES.md` for the full set of external services, skills, and the
newsletter daemon.

## `podcast_feed.json`

Configuration consumed by `scripts/generate_podcast_rss.py` to build
`podcast.rss`. A single JSON object with these keys:

`title`, `description`, `link`, `feed_url`, `site_base_url`, `author`,
`owner_name`, `owner_email`, `language`, `image_url`, `category`, `explicit`,
`audio_base_url`, `audio_dir`, `wav_dir`, `output_path`,
`episode_description_template`, `title_overrides`, `description_overrides`.

## Running tests

```sh
pip install -r requirements.txt
pip install pytest
pytest
```

CI (`.github/workflows/ci.yml`) runs the same on every push and pull request.
