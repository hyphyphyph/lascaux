def merge_dict(Left, Right):
    """
    Merge Right dictionary into Left
    """
    if not Right:
        return
    for key in Right:
        if isinstance(Right[key], dict) and Left.has_key(key):
            merge_dict(Left[key], Right[key])
        else:
            Left[key] = Right[key]
