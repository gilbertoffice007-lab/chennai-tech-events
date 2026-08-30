# Chennai Tech Events

An automated system that discovers newly published
technology events around Chennai and sends them to Telegram.

## Features

- Hackathons
- Developer meetups
- Technical symposiums
- Workshops
- Conferences
- AI/ML events
- Cloud events
- DevOps events
- Cybersecurity events
- Coding competitions
- College technical events
- Ideathons

## Main Features

### New Event Detection

The system detects newly discovered event announcements.

### Duplicate Prevention

Previously sent events are stored in Supabase.

The same event is not sent repeatedly.

### Event Updates

If event information changes, the system can send
an update notification.

### Poster

The system attempts to retrieve the original event
poster and store it in Supabase Storage.

### Telegram

The event poster and description are sent to Telegram.

## Architecture

GitHub Actions
       ↓
Google News RSS
       ↓
Event Filter
       ↓
Event Extraction
       ↓
Poster Extraction
       ↓
Supabase
       ↓
Duplicate Detection
       ↓
Telegram

## Required Secrets

SUPABASE_URL

SUPABASE_KEY

TELEGRAM_BOT_TOKEN

TELEGRAM_CHAT_ID