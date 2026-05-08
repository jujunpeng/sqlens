"""sqlens — CLI tool for parsing and visualizing PostgreSQL and MySQL query execution plans."""

__version__ = "0.1.0"
__author__ = "sqlens contributors"


def get_version() -> str:
    """Return the current version string of sqlens.

    Returns
    -------
    str
        The version string in ``MAJOR.MINOR.PATCH`` format.

    Examples
    --------
    >>> from sqlens import get_version
    >>> get_version()
    '0.1.0'
    """
    return __version__
