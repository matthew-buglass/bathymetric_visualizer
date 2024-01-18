def flatten(list_of_lists: list[list], cast_to: type = None) -> list:
    """
    Flattens a 2D matrix into a vector

    Args:
        list_of_lists: a 2D matrix
        cast_to: (OPTIONAL) a type of function to cast the type of the elements

    Returns:
        vec: the vector form of the 2D list with the elements of l[i] proceeded by the elements of l[i+1]
    """
    if cast_to is not None:
        return [cast_to(i) for j in list_of_lists for i in j]
    else:
        return [i for j in list_of_lists for i in j]
