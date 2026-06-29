# Podcast Downloader → Pocket Casts

Downloads Spotify-exclusive (and other) podcast episodes as MP3s, for manual import into Pocket Casts.

## One-time setup

1. **Log into Spotify in Chrome** (desktop) — yt-dlp reads cookies from Chrome automatically
2. Make scripts executable:
   ```bash
   chmod +x download-episode.sh
   ```
3. Install dependencies:
   ```bash
   pip install yt-dlp pyyaml
   ```

---

## One-off download

```bash
./download-episode.sh "https://open.spotify.com/episode/YOUR_EPISODE_ID"
```

Files save to `~/Downloads/podcasts/`. Works with any URL yt-dlp supports (Spotify, RSS episode links, etc.).

---

## Monitor shows for new episodes

Edit `feeds.yaml` to add shows you want to follow, then run:

```bash
python3 monitor-feeds.py
```

- Only downloads episodes you haven't seen before (tracked in `downloaded.txt`)
- Safe to run repeatedly / as a cron job

**See what would download without downloading:**
```bash
python3 monitor-feeds.py --dry-run
```

**Auto-run every morning at 7am:**
```bash
crontab -e
# Add this line:
0 7 * * * cd /path/to/podcast-dl && python3 monitor-feeds.py >> monitor.log 2>&1
```

---

## Getting MP3s into Pocket Casts

**Option A — Google Drive (easiest on mobile):**
1. Upload the MP3 to Google Drive
2. Pocket Casts → **Files** tab → **+** → **Google Drive**

**Option B — Pocket Casts web upload:**
1. Go to [pocketcasts.com](https://pocketcasts.com)
2. Click **Files** → **Upload file**

**Option C — AirDrop/Files app on iPhone:**
1. AirDrop the MP3 to your iPhone
2. Open with Pocket Casts

---

## Adding more shows to monitor

Edit `feeds.yaml`:

```yaml
shows:
  - name: "Show Name"
    url: "https://open.spotify.com/show/SHOW_ID"
    enabled: true

  - name: "Another Show"
    url: "https://feeds.example.com/podcast.rss"   # RSS feeds work too
    enabled: true
```

---

## If Spotify auth fails

yt-dlp reads from Chrome by default. If you use a different browser:
- Safari: `--cookies-from-browser safari`
- Firefox: `--cookies-from-browser firefox`

Edit the `--cookies-from-browser` flag in both scripts to match your browser.
