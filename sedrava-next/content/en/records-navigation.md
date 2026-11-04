## Typed records and bounded lists

Published 0.10.0 supports named scalar record fields and ordered collections, capacity 1–100. This declaration is a fragment of a larger program:

```sdr
record Task:
    title: text
    done: bool
state tasks: list<Task>(max=100) = []
state selected = 0
persist tasks
```

Use `append`, `has`, `get`, `update`, `remove`, `count` and `next_id`. IDs are independent of array positions, are positive and are not reused. Capacity/type/int32 failures roll back the whole action; invariants are checked before commit. There are no implicit conversions.

## Multiple screens

The published app mode declares named `screen` blocks and an explicit `navigation` block. Push/pop transitions are bounded to depth 32 and may include one atomic data action. Shared state is preserved between screens. Missing selected records are handled by guards; no unchecked indexing is needed.

See the complete [two-screen task manager](https://github.com/VasiliiBabkin/sedrava/blob/main/examples/task_manager_navigation.sdr), [record contract](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/RECORDS_COLLECTIONS_010.md) and [navigation contract](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/NAVIGATION_010_CONTRACT.md).

## Experimental WebApp UI

The live [task example](/examples/#tasks) uses experimental 0.11 `view` hash routes, custom rows and core queries. It must not be confused with released 0.10 `screen` syntax. Both keep checked state and atomic actions.
