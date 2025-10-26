
def mux_model(A: int, sel: int) -> int:
    """Reference model of 4-to-1 multiplexer

    Args:
        A: 4-bit input value (0-15)
        sel: 2-bit selector (0-3)

    Returns:
        Single bit output (0 or 1)
    """
    # Extract the bit at position 'sel' from A
    return (A >> sel) & 1
