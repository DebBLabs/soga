# M02 AAuth Localhost 501/404 Source Diagnosis

Date: 2026-10-02  
Status: SOURCE-ONLY DIAGNOSIS — CORRECTED AFTER BLIND REVIEW  
Authority: D-125  
Repository basis: `main @ b27f1285553d2a84aafb0a904baabbd7ac622423`

## Finding

The D-124 failure is caused by unread request-body bytes remaining on a
persistent HTTP/1.1 connection after an unsupported method.

The failing test sends this sequence on one `HTTPConnection`:

1. `PUT /person-token` with body `{}`;
2. receives the expected `405` and reads the response body; then
3. sends `GET /unknown` and expects `404`.

Source: `tests/test_m02_aauth_fcf656d_localhost.py:352-364`.

The handler's `do_PUT` writes `405` but never reads the request body and does
not close the connection (`m02_aauth_fcf656d/localhost.py:203-207`). Therefore
the two request-body bytes `{}` remain in the server input stream. On the next
iteration Python reads a request line beginning `{}GET /unknown ...`, derives
the method name `{}GET`, finds no `do_{}GET` handler and returns its built-in
`501 Unsupported method` before the application's `do_GET` route can return
`404`.

This follows directly from `BaseHTTPRequestHandler.handle_one_request`: for an
unknown parsed method it calls `send_error(501)` without application routing.
No test execution or reproduction was needed to establish the byte-flow cause.

## Classification

This is not evidence that `/unknown` is intentionally a `501` route. It is a
connection-desynchronization defect at any rejection boundary that responds
before consuming the declared request body.
Changing the assertion from `404` to `501` would bless the side effect while
leaving unread untrusted bytes capable of changing interpretation of the next
request on the same connection.

Blind Gate 1 review identified the same defect class on early `POST`
rejections. `_signed_request` rejects an invalid content type, missing or
non-decimal `Content-Length`, and zero or oversized lengths before calling
`self.rfile.read(length)`. Those paths previously returned JSON `400` while
leaving any transmitted bytes unread on a persistent HTTP/1.1 connection.
The existing tests concealed that risk by closing each client connection.

The issue is transport hardening rather than AAuth token, mission or SOGA
governance logic. That is consistent with the D-124 evidence: all token,
exchange, supervision and gateway authorization tests passed.

## Corrective disposition

For unsupported methods and `POST` requests rejected before their declared
body is consumed, fail closed by:

1. returning the controlled JSON `405 method_not_allowed` response;
2. sending `Connection: close`;
3. setting `self.close_connection = True`; and
4. never attempting to parse, buffer or reuse the rejected request body.

Closing is preferable to draining because the method is outside the accepted
profile, its body framing is untrusted and there is no need to preserve a
persistent connection after rejection.

The focused test should then:

- confirm the unsupported `PUT` returns JSON `405` and `Connection: close`;
- close that client connection;
- open a fresh bounded connection for `GET /unknown`; and
- confirm the application `do_GET` route returns JSON `404`.

It should also confirm that representative early `POST` rejections return
`Connection: close`. Rejections after the complete body has been consumed may
retain the connection because no bytes remain to desynchronize the next
request.

The correction should be limited to
`m02_aauth_fcf656d/localhost.py` and
`tests/test_m02_aauth_fcf656d_localhost.py`. It must not change token,
exchange, supervision, identity, provider or controller sources.

## Claim boundary

This source-only diagnosis establishes the cause and a fail-closed correction
design. The create-only correction tracks whether `_signed_request` has read
the full declared body and closes only responses produced before that point.
It does not establish corrected behavior. No import, test execution, listener
or retry occurred under D-125 or the PI's subsequent create-only authority.
