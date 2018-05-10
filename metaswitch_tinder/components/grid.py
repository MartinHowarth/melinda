import dash_html_components as html


def create_equal_grid(elements):
    """

    :param elements: List of rows, of which each is a list of columns
        Rows must be of equal length.
        Each element of a row must be a html.Div.
    :return:
    """
    n_columns = len(elements[0])

    if not all([len(row) == n_columns for row in elements]):
        raise ValueError("Not all rows are of the same length.")

    # Bootstrap allows a maximum of 12 columns per grid.
    column_class = 'col-sm-{}'.format(int(12 / n_columns))

    grid_children = []
    for row in elements:
        row_children = []
        for col in row:
            if hasattr(col, 'className'):
                col.className += ' {}'.format(column_class)
            else:
                col.className = column_class
            row_children.append(col)

        grid_children.append(html.Div(
            children=row_children,
            className='row',
        ))

    grid = html.Div(children=grid_children, className='container')
    return grid


def create_equal_row(elements):
    return create_equal_grid([elements])
