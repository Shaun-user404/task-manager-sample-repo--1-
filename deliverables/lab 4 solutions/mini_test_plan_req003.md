# Mini Test Plan: REQ-003 Catalogue Search

## Test Plan Identifier

TP-REQ-003-01, prepared 2026-10-01. Structure follows the planning sections of IEEE 829.

## Purpose and Scope

Verify that users can search the catalogue by title, author, and ISBN; matching records are returned; and each search completes within 2 seconds. Coverage includes exact and partial search terms and response-time measurement. No-match presentation is covered separately by REQ-004 and TC-SRCH-004. This plan does not assess catalogue administration, ranking relevance beyond expected matching records, or search behavior in external systems.

## Test Items and Features

Test item: catalogue search interface and its search service. Features under test: title, author, and ISBN query handling; matching result retrieval; and end-to-end response time. Related cases: TC-SRCH-001, TC-SRCH-002, and TC-SRCH-003.

## Approach

Run system-level functional tests for each supported search field using known catalogue records. Run a performance check under an agreed representative data volume and workload, measure elapsed time from request submission to complete results, and verify the response is no greater than 2.000 seconds. Record query, result identifiers, elapsed time, environment, and pass/fail. Repeat timing measurements enough times to identify inconsistent breaches; the precise sample count and load profile must be agreed before execution because the requirement does not specify them.

## Environment and Test Data

Use a test deployment with a representative catalogue containing distinct, known titles, authors, and ISBNs. Provide a controlled client and server clock, request timing, and access to application logs. Do not use production personal data. Capture the catalogue size, workload/concurrency, and deployment configuration with results.

## Entry Criteria

- Search build is deployed to the test environment and is stable.
- Test catalogue and expected matching records are prepared for title, author, and ISBN searches.
- Response-time measurement is available and synchronized.
- The representative data volume, workload, and repeat count are agreed and recorded.

## Exit Criteria

- All planned title, author, and ISBN functional cases pass with the expected matching records.
- Every measured search in the agreed performance run completes within 2 seconds.
- Results, timings, environment, and deviations are recorded; failures are logged as defects.
- No unresolved critical or high severity defect remains for REQ-003. Any accepted residual issue has documented approval.

## Risks and Assumptions

The requirement does not define catalogue scale, concurrency, whether the two-second threshold is an average or a per-request limit, or whether it includes network latency. This plan interprets the threshold as a maximum end-to-end duration for each tested search and requires stakeholders to approve the representative workload before execution.
