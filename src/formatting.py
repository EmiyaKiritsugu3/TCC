"""Formatação numérica pt-BR para a interface (RNF04)."""
from __future__ import annotations


def _fmt(value: float | None, decimals: int, sign: bool = False) -> str:
    if value is None:
        return "—"
    spec = f"+.{decimals}f" if sign else f".{decimals}f"
    return format(value, spec).replace(".", ",")


def pct(value: float | None, decimals: int = 1) -> str:
    if value is None:
        return "—"
    return f"{_fmt(value, decimals)}%"


def num(value: float | None, decimals: int = 2) -> str:
    return _fmt(value, decimals)


def signed(value: float | None, decimals: int = 2) -> str:
    return _fmt(value, decimals, sign=True)
