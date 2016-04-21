# gdbscan
## About
Python implementation of the Generalized DBSCAN algorithm from [1], enabling
clustering of point objects using both spatial and nonspatial attributes.

[1]: "Density-based clustering in spatial databases: The algorithm gdbscan and
its applications." by Sander, Jörg, et al,

## Improvements
- Improve time complexity (currently O(n^2)) using spatial indexing
  techniques.
- Use less of an object-oriented style.
