
def convert_str_to_int(item: str) -> float | None:
    item = item.replace(" ", "").replace("\u202f", "")
    item = int(item)
    return item
