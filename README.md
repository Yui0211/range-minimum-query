# Range Minimum Query

Preprocess a sequence once, then answer `min(data[lo:hi])` for any
half-open interval `[lo, hi)` in constant time per query, using a sparse
table.

```python
from range_minimum_query import RMQ

rmq = RMQ([3, 1, 4, 1, 5, 9, 2, 6])
assert rmq.query(0, 8) == 1
assert rmq.query(2, 5) == 1
assert rmq.query(6, 8) == 2
assert len(rmq) == 8
```

The export is the single class `RMQ`. Its constructor takes any
sequence (or iterable, which is materialised once) of mutually
comparable elements; `query(lo, hi)` returns `min(data[lo:hi])` and
requires `0 <= lo < hi <= len(data)`. Anything else raises `IndexError`.

## Why this exists

When the same fixed array is queried many times, repeating a linear scan
per query is wasteful. The sparse table trades O(n log n) preprocessing
time and space for O(1) queries, which is the right trade-off when the
number of queries grows faster than log n. For a single query this is
strictly worse than scanning the slice directly.

## The awkward edge

`query` answers with the minimum *value*, not its index. When the
minimum occurs more than once, the table does not distinguish which
occurrence is reported; nothing about position is part of the contract.
If you need an index, wrap the values in `(value, index)` pairs before
building the table and let tuple ordering break ties, or use a
different data structure.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

