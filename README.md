# Shipley Upper School Rowing Calendar Sync

This project automatically converts a shared Google Sheet schedule into a live, auto-updating Apple Calendar subscription.

## Overview

The system:
1. Reads a Google Sheet maintained by the coach
2. Parses schedule data into structured events
3. Generates a `.ics` calendar file
4. Publishes the file to GitHub Pages
5. Allows Apple Calendar users to subscribe to the feed

## Architecture

Google Sheet → Python Parser → ICS File → GitHub Pages → Apple Calendar Subscription

## Components

### Core Scripts

- `generate_ics.py`
  - Reads the Google Sheet
  - Parses weekly schedule format
  - Generates calendar events

- `sync_calendar.py`
  - Runs the full pipeline
  - Generates `.ics`
  - Copies to publish repo
  - Commits and pushes only if changed

- `gmail_trigger.py`
  - Checks Gmail every 5 minutes
  - Triggers sync when new coach emails arrive

- `force_sync.py`
  - Runs scheduled backup sync (9:00 AM and 12:00 PM)

### Automation

Two `launchd` jobs:

- Gmail trigger (every 5 minutes)
- Scheduled backup sync (twice daily)

## Calendar Access

Subscribe using:

https://kbt22github.github.io/shipley-rowing-calendar/shipley-upper-school-rowing.ics

In Apple Calendar:
- File → New Calendar Subscription
- Paste the URL

## Behavior

- Updates automatically when the coach updates the Google Sheet
- Gmail-triggered refresh for faster updates
- Apple Calendar refreshes every 5 minutes

## Security Notes

The following files are intentionally excluded via `.gitignore`:
- credentials.json
- token_sheets.json
- token_gmail.json

These contain sensitive authentication data.

## Sharing

The calendar feed is publicly accessible via GitHub Pages.

Anyone with the URL can subscribe. No Google account access is required.

## Future Improvements

- Improve event title formatting
- Add logging/alerting for failures
- Optional private hosting if needed
