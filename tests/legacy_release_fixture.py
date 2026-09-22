"""Historical confirmation fixture, never an application approval writer."""

import json

from tools.common import hash_canonical


def archive_event(root, event):
    event = {**event, "event_sha256": hash_canonical(event)}
    path = root / "release/public-confirmations" / (event["event_id"] + ".json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(event))
    return event
