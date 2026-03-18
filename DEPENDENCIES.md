# Newsletter Pipeline Dependencies

Everything needed to generate and publish newsletters. The repo holds the code; these are the external pieces.

## Claude Code Skills (in `~/.claude/skills/`)

| Skill | Path | Purpose |
|-------|------|---------|
| **topic-newsletter** | `~/.claude/skills/topic-newsletter/` | Main orchestrator — research, write, image, audio, publish |
| **nano-banana-pro** | `~/.claude/skills/nano-banana-pro/` | AI image generation (Gemini Imagen) |
| **narrator** | `~/.claude/skills/narrator/` | TTS audio narration for newsletters |
| **podder** | `~/.claude/skills/podder/` | Conversational podcast generation |
| **notebooklm** | `~/.claude/skills/notebooklm/` | NotebookLM API — podcast + video generation |
| **notify-me** | `~/.claude/skills/notify-me/` | iMessage notifications on completion |
| **reminders** | `~/.claude/skills/reminders/` | Apple Reminders queue management |
| **summarize** | `~/.claude/skills/summarize/` | URL/file summarization for research |
| **chronicle** | `~/.claude/skills/chronicle/` | Chronicle of Higher Education newsletters |
| **sidecar** | `~/.claude/skills/sidecar/` | Gemini CLI for deep research |
| **research** | `~/.claude/skills/research/` | Gemini deep research sub-agent |

## Newsletter Daemon

- **Location**: `~/.claude/agents/newsletter-daemon/`
- **Main script**: `newsletter_daemon.py`
- **Config**: `config.toml`
- **LaunchAgent**: `com.welshofer.newsletter-daemon.plist`
- **Queue**: Apple Reminders list "Updates"
- **MUST run sequentially** — parallel runs hit rate limits

## External Services

| Service | Purpose | Config |
|---------|---------|--------|
| **Cloudflare Pages** | Hosting — deployed via `wrangler pages deploy --branch=main` |  `~/.wrangler/` |
| **Cloudflare R2** | Large file storage (videos > 25MB) | Same Cloudflare account |
| **Gemini API** | Deep research, image generation | `$GEMINI_API_KEY` |
| **Google NotebookLM** | Podcast audio, cinematic video | Via notebooklm skill |
| **OpenAI TTS** | Narrator voice synthesis | `$OPENAI_API_KEY` |

## Deploy Repo

- **Canonical deploy directory**: `~/clawd/jlw-newsletter/`
- Content is rsync'd here then deployed with: `wrangler pages deploy ~/clawd/jlw-newsletter --project-name=jlw-newsletter --branch=main`
- **`--branch=main` is REQUIRED** or it goes to Preview, not Production

## Key Files in This Repo

- `scripts/` — pipeline utilities (RSS gen, image optimization, WAV cleanup, etc.)
- `generate_*.py` — chart generators (matplotlib) for specific newsletter topics
- `.gitignore` — blocks all content files from git
- `.cfignore` / `.wranglerignore` — blocks WAVs from Cloudflare deploy
- `podcast_feed.json` — podcast feed metadata
