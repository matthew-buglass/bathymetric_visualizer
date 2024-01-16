def flatten(l: list[list]) -> list:
    """
    Flattens a 2D matrix into a vector

    Args:
        l: a 2D matrix

    Returns:
        vec: the vector form of the 2D list with the elements of l[i] proceeded by the elements of l[i+1]
    """
    return [i for j in l for i in j]
