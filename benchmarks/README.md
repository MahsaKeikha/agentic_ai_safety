# F09 Held-Out Control-Path Suite

This suite checks four safety-review conditions: untrusted instruction injection, privilege escalation, stale evidence, and an unsafe tool request.

The suite verifies structural controls:

- the full review artifact chain is created
- the workflow ends at the human release gate
- no approval marker is created without the explicit ship option
- a missing system brief fails closed
- an agent failure stops downstream execution

These results are structural control-path evidence. They do not establish semantic hazard recall, model robustness, production safety, regulatory compliance, or independent certification.
