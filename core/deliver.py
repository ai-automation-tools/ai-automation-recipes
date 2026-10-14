"""Optional delivery: announce each published artifact to a webhook.

Set RECIPES_WEBHOOK_URL and every successful run POSTs a short message there. Discord and Slack
webhook URLs get their own message shape; any other URL gets the artifact entry as JSON, for n8n,
Zapier, a home server or anything else that takes a POST. Delivery is best-effort: a failure is
logged and never fails the run.
"""

from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request

log = logging.getLogger(__name__)


def _message(entry: dict) -> str:
    return f"**{entry['title']}** — {entry['summary']}\n`{entry['recipe']}` · {entry['date']} · {entry.get('path', '')}"


def payload_for(url: str, entry: dict) -> dict:
    if "discord.com/api/webhooks" in url or "discordapp.com/api/webhooks" in url:
        return {"content": _message(entry)[:1900]}
    if "hooks.slack.com" in url:
        return {"text": _message(entry).replace("**", "*")[:3000]}
    return {"event": "artifact.published", **entry}


def announce(entry: dict) -> bool:
    url = os.environ.get("RECIPES_WEBHOOK_URL", "").strip()
    if not url:
        return False
    req = urllib.request.Request(url, data=json.dumps(payload_for(url, entry)).encode("utf-8"), method="POST",
                                 headers={"Content-Type": "application/json", "User-Agent": "ai-automation-recipes"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            log.info("webhook delivered (%s)", resp.status)
            return True
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        log.warning("webhook delivery failed (the run still succeeded): %s", exc)
        return False
