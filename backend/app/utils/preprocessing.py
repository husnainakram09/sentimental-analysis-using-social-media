import re

URL_RE = re.compile(r"https?://\\S+|www\\.\\S+")
MENTION_RE = re.compile(r"@\\w+")
HASHTAG_RE = re.compile(r"#(\\w+)")
SPACE_RE = re.compile(r"\\s+")


def clean_tweet(text: str) -> str:
    text = URL_RE.sub(" HTTPURL ", text)
    text = MENTION_RE.sub(" @USER ", text)
    text = HASHTAG_RE.sub(r" \1 ", text)
    text = SPACE_RE.sub(" ", text)
    return text.lower().strip()
