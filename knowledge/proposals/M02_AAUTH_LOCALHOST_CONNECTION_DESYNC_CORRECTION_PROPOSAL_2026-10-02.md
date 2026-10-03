# M02 AAuth Localhost Connection-Desynchronization Correction Proposal

Date: 2026-10-02  
Status: CREATE-ONLY CORRECTION AUTHORIZED — EXECUTION PROHIBITED  
Repository basis: `main @ b27f1285553d2a84aafb0a904baabbd7ac622423`  
Authority basis: D-125 source-only diagnosis  
Review class: mandatory blind dual review, batched correction and rerun claim

## Purpose

Correct the connection-desynchronization defect evidenced by D-124, including
the same class on `POST` requests rejected before their declared body is read,
without changing accepted AAuth, mission, SOGA supervision or authorization
semantics.

## Create-only correction

After blind dual review and prospective PI authorization, modify only:

- `m02_aauth_fcf656d/localhost.py`; and
- `tests/test_m02_aauth_fcf656d_localhost.py`.

The handler correction must:

1. keep the controlled JSON `405 {"error":"method_not_allowed"}` response;
2. add `Connection: close` to unsupported-method responses;
3. set `self.close_connection = True` before or immediately after writing that
   response;
4. apply identically to PUT, DELETE and PATCH;
5. not read or drain the unsupported request body; and
6. for `POST`, track whether the complete declared body has been read and add
   `Connection: close` without draining whenever rejection occurs first; and
7. leave GET, size limits, signature handling, token logic, transport mapping
   and socket controls otherwise byte-identical.

The focused test correction must:

1. retain the unsupported `PUT` with body `{}`;
2. assert status `405`, JSON error shape and `Connection: close`;
3. close the first client connection;
4. open a fresh connection for `GET /unknown`;
5. assert JSON `404 not_found`; and
6. assert `Connection: close` for representative `POST` rejections that occur
   before the declared body is consumed; and
7. add direct DELETE and PATCH checks only if they use fresh connections and do
   not expand the runtime claim.

## Review and execution sequence

1. Blind dual review identified the early-rejected `POST` residual.
2. The PI authorized its create-only correction in the same two source files.
3. Blind diff-only static recheck of the updated records and corrected files.
4. Commit the exact reviewed correction with a prospective rerun decision.
5. Execute the exact corrected bounded controller once, with no automatic
   retry, using the accepted durable runtime and existing 53-test scope.
6. Blind dual review and PI acceptance of resulting evidence.

The corrected controller's protected source hashes must be updated only for the
two reviewed files. Every other protected hash, provider identity, socket rule,
time/output bound, redaction rule and evidence path rule remains unchanged. A
new execution must use a new empty durable evidence directory; the D-124
evidence stays immutable.

## Stop rules

Stop on any source modification outside the two named source/test files, change to
AAuth or SOGA semantics, attempt to reuse D-124's evidence directory, missing
`Connection: close`, body draining, persistent-connection reuse after `405`,
source/hash mismatch, unexpected listener, timeout, overflow, evidence leakage
or cleanup failure.

## Exclusions

The PI authorized only the create-only correction described here. It does not
authorize import, compilation, lint, test, listener, rerun, dependency
operation, Mockin execution, wallet/WAS work, QR flow, Misty access, G28 or
G29. The unrelated PI routine-tool proposal remains excluded and untouched.
