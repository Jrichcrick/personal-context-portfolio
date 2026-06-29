#!/usr/bin/env python3
"""
Monitor podcast feeds and download new episodes.

Usage:
  python3 monitor-feeds.py                 # check all enabled shows
  python3 monitor-feeds.py --show "Unlocking Us"  # check one show by name
  python3 monitor-feeds.py --dry-run       # see what would download, don't download

Set up as a cron job to run automatically:
  crontab -e
  # Add: 0 7 * * * cd /path/to/podcast-dl && python3 monitor-feeds.py >> monitor.log 2>&1
"""

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).parent
FEEDS_FILE = SCRIPT_DIR / "feeds.yaml"
DOWNLOADED_FILE = SCRIPT_DIR / "downloaded.txt"
OUTPUT_DIR = Path.home() / "Downloads" / "podcasts"


def load_downloaded() -> set:
    if not DOWNLOADED_FILE.exists():
        return set()
    return set(DOWNLOADED_FILE.read_text().splitlines())


def save_downloaded(ids: set):
    DOWNLOADED_FILE.write_text("\n".join(sorted(ids)) + "\n")


def get_show_episodes(show_url: str) -> list[dict]:
    """Use yt-dlp to list all episodes in a show without downloading."""
    result = subprocess.run(
        [
            "yt-dlp",
            "--cookies-from-browser", "chrome",
            "--flat-playlist",
            "--print", "%(id)s\t%(title)s\t%(webpage_url)s",
            show_url,
        ],
        capture_output=True,
        text=True,
    )
    episodes = []
    for line in result.stdout.strip().splitlines():
        parts = line.split("\t", 2)
        if len(parts) == 3:
            ep_id, title, url = parts
            episodes.append({"id": ep_id, "title": title, "url": url})
    return episodes


def download_episode(url: str, title: str, dry_run: bool = False) -> bool:
    print(f"  Downloading: {title}")
    if dry_run:
        print("  [dry-run, skipping actual download]")
        return True
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [
            "yt-dlp",
            "--cookies-from-browser", "chrome",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "--embed-thumbnail",
            "--add-metadata",
            "--output", str(OUTPUT_DIR / "%(uploader)s - %(title)s.%(ext)s"),
            url,
        ]
    )
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--show", help="Filter to a specific show name")
    parser.add_argument("--dry-run", action="store_true", help="List what would download without downloading")
    parser.add_argument("--all-episodes", action="store_true", help="Download all episodes, not just new ones")
    args = parser.parse_args()

    config = yaml.safe_load(FEEDS_FILE.read_text())
    shows = config.get("shows", [])

    if args.show:
        shows = [s for s in shows if args.show.lower() in s["name"].lower()]
        if not shows:
            print(f"No show found matching: {args.show}")
            sys.exit(1)

    downloaded = load_downloaded()
    new_count = 0

    for show in shows:
        if not show.get("enabled", True):
            continue
        print(f"\nChecking: {show['name']}")
        episodes = get_show_episodes(show["url"])
        if not episodes:
            print("  No episodes found (check auth or URL)")
            continue

        new_episodes = [e for e in episodes if e["id"] not in downloaded] if not args.all_episodes else episodes
        print(f"  {len(episodes)} total episodes, {len(new_episodes)} new")

        for ep in new_episodes:
            success = download_episode(ep["url"], ep["title"], dry_run=args.dry_run)
            if success and not args.dry_run:
                downloaded.add(ep["id"])
                save_downloaded(downloaded)
                new_count += 1

    print(f"\nDone. Downloaded {new_count} new episode(s).")
    if new_count > 0:
        print(f"Files in: {OUTPUT_DIR}")
        print("\nTo add to Pocket Casts: upload files to Google Drive, then")
        print("  Pocket Casts → Files tab → + → Google Drive")


if __name__ == "__main__":
    main()
