from datetime import datetime


def export_txt(data: dict) -> bytes:
    ts = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S UTC")
    content = f"""ToneShift Rewrite
-----------------
Date: {ts}
Audience: {data['audience']}
Tone: {data['tone']}

--- ORIGINAL ---
{data['original_text']}

--- REWRITTEN ---
{data['rewritten_text']}
"""
    return content.encode("utf-8")
