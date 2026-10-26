# Permission to Speak — fictional-parent QR profile

This additive package collects one adult visitor's explicitly fictional
role-play choice and conveys it through the accepted held-request-only
`DemoOperatorAdapter.record_held_input()` seam.

It does not authenticate the visitor or establish a real relationship,
parental or legal authority, consent or assent. The affected child is fictional.
No real child or personal data belongs in this profile.

The accepted receipt and signed-poll decision contain
`approval_source="local-operator-demo-control"`. That fixed value names the
accepted local software seam through which the QR choice is conveyed. It does
not identify or authenticate the visitor and does not mean the local operator
made the choice.

The accepted legacy scope name is `misty.address_participant`. In this profile
it means only a simulated directed response by the demo resource. This package
does not contact Misty or perform any physical action.

One held request is created before one 30-second QR session. One connection
owns the only adapter reference and pending path. A choice consumes both even
when the adapter refuses it. The connection never creates standing authority,
never uses private store state and never retries.

The later presentation has an absolute 60-second ceiling measured from the
start of the encounter; it is not a resettable inactivity timer. The accepted
held record's 120-second expiry is an internal fail-closed cap. It is exercised
only by synthetic tests and must not be described as demonstrated by the live
presentation.

This source is create-only under D-149. It must not be imported, tested or
executed until separately authorized after blind static review.
