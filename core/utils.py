def is_integer(num: str) -> bool:
    return len(num) > 0 and (num.isnumeric() or (num[0] == '-' and num[1:].isnumeric()))
