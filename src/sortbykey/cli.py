import pathlib
import os

def readable_directory(p: str) -> pathlib.Path:
    path = pathlib.Path(p)
    abspath = path.expanduser().resolve()
    if abspath.exists() and abspath.is_dir() and os.access(abspath, os.R_OK):
        return path
    raise TypeError("Path must point to an existing and readable directory.")

def readable_file(p: str) -> pathlib.Path:
    path = pathlib.Path(p)
    abspath = path.expanduser().resolve()
    if abspath.exists() and abspath.is_file() and os.access(abspath, os.R_OK):
        return path
    raise TypeError("Path must point to an existing and readable file.")

def writeable_directory(p: str) -> pathlib.Path:
    path = pathlib.Path(p)
    abspath = path.expanduser().resolve()
    if abspath.exists():
        if abspath.is_dir() and os.access(abspath, os.W_OK):
            return path
        else:
            raise TypeError("If path exists, must point to a writable directory.")
    return path

def positive_nonzero_int(v: int) -> int:
    if isinstance(v, int):
        if v <= 0:
            raise ValueError("Must be a positive, non-zero integer.")
        return v
    try:
        v2 = int(v)
    except:
        raise TypeError("Must be an int")
    else:
        return positive_nonzero_int(v2)

def positive_nonzero_float(v: float) -> float:
    if isinstance(v, float):
        if v <= 0:
            raise ValueError("Must be a positive, non-zero float.")
        return v
    try:
        v2 = float(v)
    except:
        raise TypeError("Must be a float")
    else:
        return positive_nonzero_float(v2)

def float_0_to_1(p: float) -> float:
    if isinstance(p, float):
        if p < 0:
            raise ValueError("Value must be (0, 1)")
        if p > 1:
            raise ValueError("Value must be (0, 1)")
        return p
    try:
        p2 = float(p)
    except:
        raise TypeError("Must be a float")
    else:
        return float_0_to_1(p2)

def positive_orzero_float(v: float) -> float:
    if isinstance(v, float):
        if v < 0:
            raise ValueError("Must be a positive float.")
        return v
    try:
        v2 = float(v)
    except:
        raise TypeError("Must be a float")
    else:
        return positive_nonzero_float(v2)