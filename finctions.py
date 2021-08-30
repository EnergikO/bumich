def may_be_class(value, class_name=int) -> bool:
    if value is None:
        return False

    try:
        value = class_name(value)
        return True

    except ValueError:
        return False
