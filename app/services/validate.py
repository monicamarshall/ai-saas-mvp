def validate_rows(rows):
    return [r for r in rows if r.get("account") and isinstance(r.get("amount"), (int,float))]
