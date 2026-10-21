# IIW QR and Representative-Authority Boundary

Date: 2026-10-21
Status: SYNTHESIS DRAFT — NOT REVIEWED; creates no authority
Repository basis: `main @ 474a574eda798bdedde9b659df853065c16e575d`

## Purpose

Record two independent read-only audits completed after AAuth Night and keep
their implications separate. One audit examined the exact pinned AAuth editor
source. The other decoded and traced the exact QR artifact shown in the R6
Permission to Speak presentation. Neither audit modified or executed repository
code.

## Source audits

### AAuth representative-authority audit

Claude Code verified the durable source checkout at
`/Users/debb/dev/research-evidence/soga/inputs/aauth/fcf656d/source` as exact
commit `fcf656de1926535f5bd6fc0538147ead6646e727`, with clean status and
`draft-hardt-oauth-aauth-protocol.md` SHA-256
`295ba2a0edd99dd077c4c877b6276608000419fdf4bbef2327da0c6e4d950953`.
The complete audit is preserved at
`/Users/debb/dev/soga-gate1-notes/AAUTH_FCF656D_REPRESENTATIVE_AUTHORITY_AUDIT_2026-10-21.md`,
SHA-256 `fab15dfe7c898517238de1ecaf56135540545c4017e4dd7bb480ce8718a9fba8`.
Its complete read of the requested sections and full-source search found:

- person-to-agent delegated authority is established;
- optional supervision on the Person's behalf is established;
- obtaining approval from another party is available as a deferred-response
  mechanism;
- the source does not establish one person's representative authority for or
  over another person;
- it does not address affected non-principals; and
- it does not define when third-party approval is required or establish that
  party's relationship to the affected person.

The current text contains no delegation-chain claim. It records that an `act`
claim used in earlier revisions was removed, and the audit found no reference
to a McGuinness `act` draft or any use of `act` for a person-to-person
relationship.

These are source findings about the pinned editor copy, not claims that an
extension or companion specification could not represent the missing facts.
The pinned document identifies itself as the editor's `-latest` copy. Section
numbers in it do not necessarily match the subsequently published `-11` draft;
the audit's findings are pinned to the commit and whole-file hash above.

### Permission to Speak R6 QR audit

AGy verified tag `pts-candidate-2026-10-06-r6` at commit
`cb188cd19164a5c5471fde253ed85b10cc70f727` and decoded the exact embedded QR
artifact without network access or execution. The QR payload is:

```text
http://localhost:4317/#8
```

The complete audit is preserved at
`/Users/debb/dev/soga-gate2-notes/PTS_R6_QR_BEHAVIOR_AUDIT_2026-10-21.md`,
SHA-256 `522872543cb65b6e17fb20bb41bc7bae61b6137665313a9b903468e47914efa5`.

That payload cannot reach the presentation laptop from an attendee phone:
`localhost` resolves on the scanning phone. It is also stale: after two slides
were inserted, `#8` no longer names the parent-control slide. On the
presentation laptop, the R6 bridge permits only `Host:
127.0.0.1:4317`, so the exact `localhost` request would be rejected. The
clickable HTML wrapper, rather than the encoded QR payload, advanced the local
presentation to the correct control screen.

The QR exposed no service, credential, token, personal data, LAN address or
external destination. Its failure was safe. Its visual affordance nevertheless
invited a phone interaction that the R6 package did not provide.

## Combined finding

The PI reports that the bounded local AAuth/SOGA decision and refusal path ran
successfully at AAuth Night. The gated repository basis for that path is D-144,
not the event report. The event did not prove phone participation or
representative authority. The PI also reports that an attendee tried to scan
the displayed QR without prompting. That is field evidence that a
phone-accessible interaction is an expected next affordance, not evidence that
the displayed QR worked.

The first IIW QR increment should therefore use consenting adult participants
and make no parent, guardian, representative, identity or legal-authority
claim. It may gather an explicitly bounded participant choice while preserving
the accepted distinction between Deb's AAuth authority and separate other-party
input. Representative authority remains a research and policy track.

Unverified research hypotheses: GNAP may be relevant for later comparison as a
multi-stage grant and interaction mechanism, and Transaction Tokens may be
relevant for propagating accepted transaction context inside a trusted service
call chain. These hypotheses require exact-source research before use. Neither
technology is selected or implemented by this record.

## Boundary

This draft authorizes no code, listener, QR generation, network access, phone
access, participant collection, AAuth execution, GNAP work, Transaction Token
work, wallet/WAS integration, Misty access, physical action, G28 or G29. It
does not change or invalidate the accepted D-144 localhost operator result.

