# Lab 7: Mutation Testing

## Scope and method

Mutmut 3.8.0 was run in WSL because mutmut does not support native Windows execution. The mutation source was `app/tasks.py`; pytest selection focused on the Lab 6 functions `find_task_by_title`, `remove_task`, and `load_tasks`. The manual `test_save_and_load_tasks` case also exercises `save_tasks`, so its mutants appear in the manual and combined counts.

Scores use `killed / (killed + survived)`. Mutants reported as **no tests** were not included in the score because the selected tests do not exercise those code paths.

## Initial mutation reports

| Suite | Mutants generated | Killed | Survived | No tests | Mutation score |
|---|---:|---:|---:|---:|---:|
| AI-generated (`tests_ai/test_ai_generated.py`) | 78 | 16 | 5 | 57 | **76.2% (16/21)** |
| Manual (`test_manual/test_manual.py`) | 78 | 27 | 8 | 43 | **77.1% (27/35)** |
| Combined AI + manual | 78 | 27 | 8 | 43 | **77.1% (27/35)** |

## AI-suite survivor analysis

Three of the AI run's surviving mutants were in `load_tasks`:

1. **`app.tasks.x_load_tasks__mutmut_4`** changes `encoding="utf-8"` to `encoding=None`. The existing saved-task fixture was ASCII, so reading it with the platform default produced the same result.
2. **`app.tasks.x_load_tasks__mutmut_6`** removes the explicit `"r"` mode. Python defaults `open()` to read mode, so the existing result assertions could not distinguish the change.
3. **`app.tasks.x_load_tasks__mutmut_7`** removes the explicit encoding. The existing fixtures and the test environment's default encoding allowed the file to load successfully anyway.

The existing tests checked returned task data and error cases, but not the `open()` arguments used to read a non-ASCII JSON file. A fourth survivor, `x_load_tasks__mutmut_11`, changes `"utf-8"` to `"UTF-8"`; this is also accepted as an encoding alias.

The remaining AI survivor, **`app.tasks.x_remove_task__mutmut_5`**, replaces `break` with `return`. Both paths remove the first matching item and then return `None`; there is no code after the loop, so this is behaviorally equivalent and cannot be distinguished by a meaningful output assertion.

## Added targeted test

Added `test_load_tasks_uses_explicit_utf8_text_read` to `tests_ai/test_ai_generated.py`. It loads a task with a non-ASCII title (`"Café notes"`) and records the `open()` call, asserting that the function explicitly passes text-read mode and UTF-8 encoding. This kills the three identified `load_tasks` survivors and the UTF-8 alias mutant.

## Updated mutation results

| Suite | Killed | Survived | No tests | Updated mutation score |
|---|---:|---:|---:|---:|
| AI-generated (updated) | 20 | 1 | 57 | **95.2% (20/21)** |
| Manual (unchanged) | 27 | 8 | 43 | **77.1% (27/35)** |
| Combined AI + manual (updated) | 31 | 4 | 43 | **88.6% (31/35)** |

The AI score improved from **76.2% to 95.2%**. The combined score improved from **77.1% to 88.6%**. The surviving AI mutant is the behaviorally equivalent `remove_task` mutation noted above; the combined report also retains three `save_tasks` survivors from the manual save/load round-trip test.

## Reproduction

Run the selected test suite with mutmut from WSL at the repository root:

```bash
mutmut run
mutmut results
```

The active selection in `pyproject.toml` is the combined suite. For an isolated report, change `pytest_add_cli_args_test_selection` to the corresponding single test file and rerun `mutmut run`.
