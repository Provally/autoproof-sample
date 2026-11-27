def computed_column(expression, row):
    """Evaluate a computed column that a partner's mapping defines, such as "amount * rate", for one CSV row."""
    return eval(expression, {}, dict(row))
