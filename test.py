import sys

def get_base_prefix_compat():
    """Get base/real prefix, or sys.prefix if there is none."""
    return (
        getattr(sys, "base_prefix", None)
        or getattr(sys, "real_prefix", None)
        or sys.prefix
    )


def in_ven():
    return sys.prefix != sys.base_prefix

get_base_prefix_compat()
in_ven()