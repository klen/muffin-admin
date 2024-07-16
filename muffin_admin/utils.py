def deepmerge(dest: dict, source: dict):
    """Deep merge two dictionaries."""
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = dest.setdefault(key, {})
            deepmerge(node, value)
        else:
            dest[key] = value

    return dest
