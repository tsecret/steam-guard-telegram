def escape_tg(message):
    escape_char = {".", "-", "?", "!", ">", "{", "}", "=", "+", "|", "(", ")"}
    escaped_message = ""
    is_escaped = False
    for cur_char in message:
        if cur_char in escape_char and not is_escaped:
            escaped_message += "\\"
        escaped_message += cur_char
        is_escaped = cur_char == "\\" and not is_escaped
    return escaped_message