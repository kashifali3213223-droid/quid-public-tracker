# QUID Public Tracker

This is a NEW copy for testing. It does not modify the existing working tracker.

## Railway
- Add the same `ALCHEMY_API_KEY` environment variable.
- Deploy this project.
- Railway will provide a public URL.
- Start command:
  `gunicorn app:app --bind 0.0.0.0:$PORT`

The dashboard updates every 3 seconds and provides:
- Total unique wallets
- Total tracked USD volume
- Live wallet ranking
- Wallet address search

Important: data is in memory, so restarting this service resets the counters. The existing tracker remains untouched.
