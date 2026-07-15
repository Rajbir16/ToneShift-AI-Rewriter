from datetime import datetime


def export_txt(data: dict) -> bytes:
    timestamp = data.get("timestamp", "")

    if timestamp:
        try:
            ts = datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            ).strftime("%Y-%m-%d %H:%M:%S UTC")
        except ValueError:
            ts = "Unknown"
    else:
        ts = "Unknown"

    content = f"""ToneShift Rewrite
-----------------
Date: {ts}
Audience: {data.get('audience', '')}
Tone: {data.get('tone', '')}

--- ORIGINAL ---
{data.get('original_text', '')}

--- REWRITTEN ---
{data.get('rewritten_text', '')}
"""

    return content.encode("utf-8")
