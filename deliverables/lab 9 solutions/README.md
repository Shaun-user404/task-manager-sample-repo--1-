# Lab 9: Session-Based Exploratory Testing

## Test charter

**Feature:** Task list lifecycle in the Lab 8 Taskflow demo.

**Mission:** Explore whether people can add tasks, mark tasks complete, clear completed tasks, and trust the remaining-task count, including boundary values and rapid interactions.

**Scope:** Browser UI in `../lab 8 solutions/index.html`, specifically the add-task form, task checkboxes, clear-completed action, labels, and task count. This is a standalone demo: data persistence, accounts, API behavior, and the Python CLI are out of scope.

**Time-box:** 45 minutes maximum. Stop immediately at the end of the time-box.

**Test data / setup:** Begin from a fresh page with the two seeded tasks and count of two. Use unique task titles in each probe. Record unexpected behavior, questions, and follow-up ideas as they occur.

### AI co-pilot suggestions (prepared before the timer)

Using SFDIPOT-style prompts, the assistant suggested:

1. **Data / input boundaries:** Submit empty, whitespace-only, very long, and punctuation/Unicode task titles; check whether the input, list, and count agree.
2. **Interactions / keyboard:** Add tasks with Enter as well as the button; move through controls with Tab and operate checkboxes with the keyboard.
3. **Operations / rapid changes:** Add multiple tasks quickly, complete several in different orders, and clear them; watch for duplicate control identifiers, missing tasks, or stale counts.
4. **Structure / relationship:** Check that every dynamically added task label toggles its own checkbox, including after clearing an earlier item.
5. **Testing / oracles:** Compare the visible count to unchecked tasks after each action and after reload; investigate whether tasks are intentionally session-only or expected to persist.

## Timestamped session notes

_The timer starts after the charter and AI suggestions above are written. Findings are recorded during the session, not reconstructed from memory._

**Start:** 2026-10-27 22:18:09.800 +02:00

| Timestamp | Observation / action / question / idea | Source |
|---|---|---|
| 22:18:09.800 +02:00 | Started the session timer after preparing the charter and five AI ideas. Reloaded the app into its seeded state (2 tasks, count 2). | Setup |
| 22:18:21.454 +02:00 | AI idea 2: added `Keyboard probe — café` with Enter. Task appeared, count rose to 3, and focus returned to the input. Unicode and keyboard submission worked. | AI-suggested |
| 22:18:50.027 +02:00 | AI idea 1: a whitespace-only value passes native `required` validation (`checkValidity() === true`), but the trimmed submit handler adds nothing and leaves the spaces in the field. The UI provides no explanation; reproducible with a form submit. Logged as bug B1. | AI-suggested |
| 22:19:07.850 +02:00 | AI ideas 3–4: forced two rapid submissions to share a timestamp ID. Both rows received `task-1770000000000`; clicking the “Rapid beta” label toggled the “Rapid alpha” checkbox instead. Logged as bug B2. | AI-suggested |
| 22:19:38.037 +02:00 | Self-directed state-cycle probe: toggled one task on and off with Space; count changed 2 → 1 → 2. Clearing with no completed tasks left both rows and the count intact. | Self-found idea; no bug |
| 22:19:48.838 +02:00 | AI idea 1: submitted a 300-character unbroken title. It was accepted and counted, but expanded the task row to 2,325px and document to 2,669px at a 1,365px viewport, producing severe horizontal overflow. Logged as bug B3. | AI-suggested |
| 22:20:15.759 +02:00 | AI idea 5: reloaded after adding the long task. The page returned to its two seeded tasks and count 2; session data is not persisted. No bug filed because persistence was explicitly excluded from this demo charter. | AI-suggested; out of scope |

**Stop:** 2026-10-27 22:20:26.114 +02:00  
**Elapsed:** 2 minutes 16.314 seconds (within the 45-minute maximum)

## Session report

**Session:** Taskflow task-list lifecycle  
**Result:** 3 bugs found; 1 self-directed probe completed without a bug. Testing stopped at 22:20:26.114 +02:00, before the 45-minute maximum.

### Coverage

Explored fresh seeded state, keyboard/Enter task creation, Unicode input, whitespace-only input, repeated task IDs, checkbox-label associations, task-count updates, repeated complete/uncomplete cycles, clearing with no completed tasks, long unbroken titles, and page reload. Reload resets the demo to its seeded tasks; persistence was explicitly out of scope.

### Bug list and triage

Severity scale: **S1 critical** = blocks core use; **S2 major** = materially breaks a core task or layout; **S3 minor** = confusing or inconvenient, with a workaround.

| ID | Severity | Finding | Source |
|---|---|---|---|
| B1 | S3 — Minor | Whitespace-only input passes the browser's `required` check, then is silently rejected after trimming. The spaces remain in the field and the user gets no explanation. | AI-suggested idea 1 (input boundaries) |
| B2 | S2 — Major | Two tasks created with the same millisecond timestamp receive duplicate checkbox IDs. Clicking the second task's label toggles the first task instead, making the new task's label unreliable. Reproduced deterministically with a fixed clock. | AI-suggested ideas 3–4 (rapid operations / label relationships) |
| B3 | S2 — Major | A 300-character unbroken task title expands the row to 2,325px and the page to 2,669px at a 1,365px viewport, causing horizontal overflow and making the layout difficult to use. | AI-suggested idea 1 (long input) |

### AI vs. self-found source

Source is attributed to the avenue that first surfaced each bug. All **3 of 3 bugs (100%)** originated from AI-suggested probes; **0 of 3 (0%)** originated from the self-directed probe. The self-directed complete/uncomplete-and-clear cycle was tested and passed. These percentages describe bug discovery, not test coverage.

### Follow-up ideas

- Reject trimmed-empty titles with clear inline feedback and focus management.
- Generate unique IDs independently of wall-clock milliseconds (for example, a monotonic counter or UUID).
- Allow unbroken task titles to wrap or truncate within the task-card width.
