def capitalize_str(value: str) -> str:
    words = value.split()

    normalized_name = []
    for word in words:
        normalized_name.append(word.capitalize())
    return " ".join(normalized_name)
