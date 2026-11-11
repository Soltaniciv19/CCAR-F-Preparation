def applies(path):
    if not isinstance(path, str) or not path or path.startswith("/"):
        return False
    parts = path.split("/")
    return (
        len(parts) >= 2
        and parts[0] == "src"
        and ".." not in parts
        and all(parts)
        and parts[-1].endswith(".py")
    )
