# AI-Drafted RTM Comparison

## Method

I drafted a first-pass RTM from the same eight requirements in the supplied image, then reviewed it against the authored `requirements_traceability_matrix.csv` and the detailed cases in `test_cases.csv`. The draft is preserved as `ai_draft_rtm.csv`; it is a proposal, not executed test evidence.

## Comparison

| Check | AI draft | Authored RTM | Assessment |
|---|---|---|---|
| Requirement coverage | Includes REQ-001 through REQ-008 exactly once | Includes REQ-001 through REQ-008 exactly once | Complete in both; no requirement is unmapped. |
| Requirement wording | Preserves the supplied statements | Preserves the supplied statements | Correct in both. |
| Test design depth | One broad draft case per requirement | Multiple linked cases where useful, including positive, negative, and boundary scenarios | The draft is a useful coverage skeleton but too shallow for several acceptance boundaries. |
| Registration | Covers account registration generally | Separates valid registration, duplicate email, and a password shorter than 8 characters | Authored RTM makes uniqueness and minimum length independently verifiable. |
| Search and borrowing limits | Covers search and borrowing generally | Separates search fields and response time; checks the third/fourth loan boundary and overdue-loan restriction | Authored RTM makes each threshold and rejection rule explicit. |
| Fine and notifications | Covers return/fine and reminders generally | Checks an on-time return, a 3-day overdue fine calculation, the two-day reminder, and daily overdue messages | Authored RTM adds the strongest monetary and schedule boundaries. |
| Test level and execution status | Labels cases by likely level and marks them not run | Identifies system/performance/integration levels and marks all tests designed, not run | Both correctly avoid implying execution; authored levels are more specific. |

## Conclusion

The AI draft is structurally complete and maps every supplied requirement, but its single broad case per requirement risks masking omitted boundary and negative behavior. The authored RTM retains the full requirement coverage and expands cases around unique email/password length, the two-second threshold, the three-book limit, the overdue block, exact fine calculation, and reminder timing. Requirement wording leaves performance workload and notification delivery timing details unspecified; those assumptions are called out in the mini plan rather than invented as acceptance criteria.
