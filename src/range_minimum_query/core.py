"""Range Minimum Query using a sparse table.

The sparse table preprocesses ``data`` in O(n log n) time and space so any
interval-minimum query over ``[lo, hi)`` is answered in O(1) time. Building
the table requires knowing ``len(data)`` up front, so the input must be a
sequence whose length does not change; arbitrary iterables are accepted by
materialising them into a list first.

Only the minimum *value* is returned, not its index. Returning the index
would force a choice about which index to report when the minimum is
tied, and the brief does not say which; keeping to the value sidesteps the
ambiguity entirely.
"""

from __future__ import annotations

import math
from typing import List, Sequence, TypeVar

T = TypeVar("T")


class RMQ:
    """Sparse-table range-minimum query over a fixed, comparable sequence.

    Elements are compared with ``<`` (the same rule Python's built-in
    ``min`` uses). If two elements compare equal, the table reports that
    value; no tie-breaking information is surfaced.

    A two-dimensional table ``st[k]`` stores, for every start ``i``, the
    minimum of the sub-range ``[i, i + 2**k)``. A query on ``[lo, hi)`` is
    the element-wise minimum of two overlapping intervals of length
    ``2**k`` where ``k = floor(log2(hi - lo))``; because both fully cover
    ``[lo, hi)`` their overlap does not affect the answer.
    """

    def __init__(self, data: Sequence[T]) -> None:
        self._data: List[T] = list(data)
        n = len(self._data)
        self._n = n

        if n == 0:
            # Storing an empty list of tables lets ``query`` raise the
            # domain error uniformly instead of needing a special branch
            # here.
            self._st: List[List[T]] = []
            self._log: List[int] = []
            return

        max_k = n.bit_length()  # 2**(max_k-1) <= n < 2**max_k
        # ``log2`` table for every possible query length, precomputed so
        # the query path has no floating point and no branches beyond an
        # array read.
        self._log = [0] * (n + 1)
        for i in range(2, n + 1):
            self._log[i] = self._log[i // 2] + 1

        st: List[List[T]] = [[self._data[i] for i in range(n)]]
        for k in range(1, max_k):
            prev = st[k - 1]
            step = 1 << (k - 1)
            row: List[T] = []
            # The last element where a window of length 2**k still fits.
            last = n - (1 << k)
            for i in range(last + 1):
                a = prev[i]
                b = prev[i + step]
                row.append(a if a < b else b)
            st.append(row)
        self._st = st

    def query(self, lo: int, hi: int) -> T:
        """Return ``min(data[lo:hi])`` for ``0 <= lo < hi <= n``.

        ``lo`` and ``hi`` may be any integers; anything outside
        ``[0, n]`` raises ``IndexError``. ``lo >= hi`` also raises
        ``IndexError`` because there is no element to minimise.
        """
        if not 0 <= lo < hi <= self._n:
            raise IndexError(
                f"query interval [{lo}, {hi}) is out of range for "
                f"data of length {self._n}"
            )
        length = hi - lo
        k = self._log[length]
        row = self._st[k]
        a = row[lo]
        b = row[hi - (1 << k)]
        return a if a < b else b

    def __len__(self) -> int:
        return self._n
