from typing import Callable, List, Iterable, Any

from python_qa.utils.classes import get_values


def filtered(func: Callable, iterable: Iterable):
    return type(iterable)(filter(func, iterable))


def select_items(items: Iterable, inverse: bool = False, **kwargs) -> List:
    res = []
    if kwargs:
        for item in items:
            selected = True
            for k, v in kwargs.items():
                item_v = item.get(k) if hasattr(item, "get") else getattr(item, k, None)
                if (item_v != v and not inverse) or (item_v == v and inverse):
                    selected = False
                    break
            if selected:
                res.append(item)
    return res


def select_item(items: Iterable, inverse: bool = False, **kwargs) -> Any | None:
    res = select_items(items, inverse, **kwargs)
    if res:
        return res[0]


def deep_select_items(items: Iterable, inverse: bool = False, **kwargs) -> List:
    res = []
    if kwargs:
        for item in items:
            values = get_values(item, *list(kwargs.keys()), deep=True)
            selected = True
            for k, v in kwargs.items():
                if (v not in values[k] and not inverse) or (v in values[k] == v and inverse):
                    selected = False
                    break
            if selected:
                res.append(item)
    return res


def deep_select_item(items: Iterable, inverse: bool = False, **kwargs):
    res = deep_select_items(items, inverse, **kwargs)
    if res:
        return res[0]
