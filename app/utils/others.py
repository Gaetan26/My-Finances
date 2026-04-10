
def convert_str_to_int(item: str) -> float | None:
    item = item.replace(" ", "").replace("\u202f", "")
    try:
        item = int(item)
        return item
    except Exception as exp:
        print(exp)
        print('\n\n')
        return None
