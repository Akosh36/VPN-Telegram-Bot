import re

def escape_markdown_v2(text: str) -> str:
    """
    Escapes all special MarkdownV2 characters in the given text.
    See: https://core.telegram.org/bots/api#markdownv2-style
    """
    # Characters that need to be escaped in MarkdownV2
    # _ * [ ] ( ) ~ ` > # + - = | { } . !
    # Note: \ is also a special character but it's used for escaping itself,
    # so we handle it by doubling it.
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(r"([{}])".format(re.escape(escape_chars)), r"\\\1", text)
