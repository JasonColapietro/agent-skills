#!/usr/bin/env python3
"""Add missing attribution parameters without replacing existing campaign values."""
import argparse
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


def tag_url(url, source, content):
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.netloc:
        raise ValueError("URL must be absolute HTTP or HTTPS")
    existing = {key for key, _ in parse_qsl(parts.query, keep_blank_values=True)}
    defaults = (("utm_source", source), ("utm_medium", "skill"),
                ("utm_campaign", "agent-skills"), ("utm_content", content))
    added = urlencode([(key, value) for key, value in defaults if key not in existing])
    # Keep the original query encoding, duplicate keys and blank values intact.
    query = parts.query + ("&" if parts.query and added else "") + added
    return urlunsplit((parts.scheme, parts.netloc, parts.path, query, parts.fragment))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("--source", default="github")
    parser.add_argument("--content", default="timetopost-social-scheduler")
    args = parser.parse_args()
    print(tag_url(args.url, args.source, args.content))
