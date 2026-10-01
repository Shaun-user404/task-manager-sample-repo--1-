# Sample Defect Log

These are instructional sample records derived from the requirements not reports of defects in a running library system. Each record is shown moving through the complete lifecycle in order. Severity and priority were assigned at Triaged and are repeated for traceability. Owners and verification results are illustrative.

| Defect ID | Requirement | Summary | Severity | Priority | Lifecycle stage | Owner | Action / evidence |
|---|---|---|---|---|---|---|---|
| DEF-001 | REQ-003 | ISBN search returns matching records but exceeds the 2-second response-time limit under the agreed representative workload. | High | High | New | QA | Reported with ISBN query, workload profile, and measured response time above 2 seconds. |
| DEF-001 | REQ-003 | ISBN search returns matching records but exceeds the 2-second response-time limit under the agreed representative workload. | High | High | Triaged | QA lead | Confirmed against the REQ-003 performance acceptance threshold; severity High and priority High assigned. |
| DEF-001 | REQ-003 | ISBN search returns matching records but exceeds the 2-second response-time limit under the agreed representative workload. | High | High | Assigned | Catalogue engineer | Assigned for search-query performance investigation. |
| DEF-001 | REQ-003 | ISBN search returns matching records but exceeds the 2-second response-time limit under the agreed representative workload. | High | High | Fixed | Catalogue engineer | Illustrative fix: optimize the ISBN lookup path and add an appropriate index; fix deployed to test. |
| DEF-001 | REQ-003 | ISBN search returns matching records but exceeds the 2-second response-time limit under the agreed representative workload. | High | High | Verified | QA | Repeated the agreed workload; matching records returned and all measured searches completed within 2 seconds. Related case: TC-SRCH-003. |
| DEF-001 | REQ-003 | ISBN search returns matching records but exceeds the 2-second response-time limit under the agreed representative workload. | High | High | Closed | QA lead | Verification evidence reviewed; defect closed. |
| DEF-002 | REQ-008 | Due-soon email is not sent two days before a book's due date. | Medium | Medium | New | QA | Reported using a loan with a known due date and captured test-mailbox evidence showing no reminder at due date minus two days. |
| DEF-002 | REQ-008 | Due-soon email is not sent two days before a book's due date. | Medium | Medium | Triaged | QA lead | Confirmed against the REQ-008 reminder requirement; severity Medium and priority Medium assigned. |
| DEF-002 | REQ-008 | Due-soon email is not sent two days before a book's due date. | Medium | Medium | Assigned | Notifications engineer | Assigned to investigate due-date scheduling and notification dispatch. |
| DEF-002 | REQ-008 | Due-soon email is not sent two days before a book's due date. | Medium | Medium | Fixed | Notifications engineer | Illustrative fix: correct the due-soon scheduling calculation and deploy to test. |
| DEF-002 | REQ-008 | Due-soon email is not sent two days before a book's due date. | Medium | Medium | Verified | QA | Controlled-clock run delivered one due-soon email at due date minus two days; daily overdue reminders also passed. Related cases: TC-NOT-001 and TC-NOT-002. |
| DEF-002 | REQ-008 | Due-soon email is not sent two days before a book's due date. | Medium | Medium | Closed | QA lead | Verification evidence reviewed; defect closed. |

Lifecycle represented: New → Triaged → Assigned → Fixed → Verified → Closed for both defects.
