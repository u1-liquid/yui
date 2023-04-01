import datetime
import re
from collections.abc import Callable
from collections.abc import Sequence
from decimal import Decimal
from typing import Any
from typing import TypeVar

T = TypeVar("T", int, float, Decimal)

DATE_FORMAT_RE = re.compile(
    r"(\d{4})\s*[-\.년]?\s*(\d{1,2})\s*[-\.월]?\s*(\d{1,2})\s*일?",
)


def str_to_date(
    fallback: Callable[[], datetime.date] | None = None,
) -> Callable[[str], Any]:
    """Helper to make date object from given string."""

    def callback(value: str) -> datetime.date:
        if match := DATE_FORMAT_RE.match(value):
            try:
                return datetime.date(
                    int(match.group(1)),
                    int(match.group(2)),
                    int(match.group(3)),
                )
            except ValueError:
                if fallback is None:
                    raise
                return fallback()
        raise ValueError("Incorrect date string")

    return callback


def _extract(text: str) -> str:
    if text.startswith("<") and text.endswith(">"):
        if "|" in text:
            return text[1:-1].split("|", 1)[0]
        return text[1:-1]
    return text


def extract_url(text: str) -> str:
    """Helper to extract URL from given text."""

    return _extract(text)


def get_channel_id(text: str) -> str:
    """Helper to get Channel from given text."""

    return _extract(text).lstrip("#")


def get_user_id(text: str) -> str:
    """Helper to get User from given text."""

    return _extract(text).lstrip("@")


def enum_getitem(
    cls,
    *,
    fallback: str | None = None,
) -> Callable[[str], Any]:
    """
    Helper to transform item to enum object by name from given enum

    .. warning::
       Do not use it in type annotation or `type_` value.

       .. sourcecode:: python
          @box.command('ok')
          @option('--key', transform_func=enum_getitem(KeyEnum))
          async def ok(key: KeyEnum):  # It's OK
              pass

          @box.command('no')
          @option('--key')
          async def no(key: enum_getitem(KeyEnum)):  # Do not this
              pass

    """

    def callback(keyword: str):
        try:
            return cls[keyword]
        except KeyError as e:
            if fallback:
                return cls[fallback]
            raise ValueError from e

    return callback


def choice(
    items: Sequence[str],
    *,
    fallback: str | None = None,
    case_insensitive: bool = False,
    case: str | None = None,
) -> Callable[[str], str]:
    """
    Helper to constraint value to in items or raise error.

    .. warning::
       Do not use it in type annotation or `type_` value.

       .. sourcecode:: python
          @box.command('ok')
          @option('--key', transform_func=choice('A', 'B'))
          async def ok(key: str):  # It's OK
              pass

          @box.command('no')
          @option('--key')
          async def no(key: choice('A', 'B')):  # Do not this
              pass

    """

    def transform_case(val):
        if case is not None and hasattr(val, case):
            return getattr(val, case)()
        return val

    def callback(val):
        if case_insensitive:
            if val.lower() in (x.lower() for x in items):
                return transform_case(val)
            if fallback is not None:
                return transform_case(fallback)
            raise ValueError("given value is not in allowed cases")
        if val in items:
            return transform_case(val)
        if fallback is not None:
            return transform_case(fallback)
        raise ValueError("given value is not in allowed cases")

    return callback


def value_range(
    start: T,
    end: T,
    *,
    autofix: bool = False,
) -> Callable[[T], T]:
    """
    Helper to constraint value to in range or raise error.

    .. warning::
       Do not use it in type annotation or `type_` value.

       .. sourcecode:: python
          @box.command('ok')
          @option('--key', transform_func=value_range(1, 10))
          async def ok(key: int):  # It's OK
              pass

          @box.command('no')
          @option('--key')
          async def no(key: value_range(1, 10)):  # Do not this
              pass

    """

    def callback(val: T) -> T:
        if start <= val <= end:
            return val
        if start > val:
            if autofix:
                return start
            raise ValueError("given value is too small.")
        if autofix:
            return end
        raise ValueError("given value is too big.")

    return callback
