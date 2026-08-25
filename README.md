# F09 | Agentic AI Safety

A reference implementation of a governed multi-agent workflow for AI safety review. The repository demonstrates how specialized agents can collaborate across system scoping, hazard identification, policy mapping, evaluation planning, defensive red teaming, residual-risk assessment, incident planning, and a final human release gate.

This repository is part of the Agentic AI Library and is intended for education, engineering practice, governance research, safety-review prototyping, and adaptation into larger AI assurance systems.

## What this system does

The workflow begins with a system or feature description and turns it into a structured safety-review package. It is designed to keep risk identification, policy interpretation, evaluation, adversarial review, residual-risk analysis, and release approval separate.

A typical run can:

- define the system, users, data, capabilities, and review boundaries
- identify plausible harm classes and misuse paths
- map findings to internal policy or acceptable-use rules
- define evaluations and release metrics
- create defensive red-team test ideas
- assess what risk remains after mitigations
- prepare an incident-response plan
- consolidate the evidence into a safety pack
- stop before release approval until a human explicitly passes the gate

The system supports safety engineering. It does not certify a model or product as safe and does not replace legal, security, privacy, ethics, or domain-specific review.

## Multi-agent architecture

| Agent | Responsibility | Typical output |
|---|---|---|
| Scope Agent | Define system boundaries, users, data, capabilities, and assumptions | scope note |
| Hazard Agent | Identify plausible harms, misuse cases, and failure modes | hazard register |
| Policy Agent | Map risks and system behavior to policy requirements | policy map |
| Eval Agent | Define safety tests, metrics, and acceptance criteria | evaluation plan |
| Red Team Agent | Propose defensive probes and expected safe behavior | red-team plan |
| Residual Agent | Assess risk remaining after proposed mitigations | residual-risk note |
| Incident Agent | Define response responsibilities and escalation if failures occur | incident plan |
| Gatekeeper Agent | Consolidate evidence and prepare the release checklist | safety pack and gate review |

The workflow separates agents that discover risk from the agent that prepares the final release package, reducing the chance that one reasoning path both proposes and approves its own conclusions.

## End-to-end workflow

A typical review proceeds as follows:

1. Scope Agent defines the system under review.
2. Hazard Agent builds the initial risk picture.
3. Policy Agent maps risks to applicable internal rules.
4. Eval Agent specifies tests and metrics.
5. Red Team Agent proposes defensive adversarial probes.
6. Residual Agent evaluates remaining risk after mitigations.
7. Incident Agent defines response and escalation expectations.
8. Gatekeeper Agent consolidates the review package.
9. The workflow stops at the human release gate unless `--ship` is explicitly provided.

The design treats unresolved risk as a reason to hold or revise, not as something that must be forced into a passing result.

## Repository structure

```text
agentic_ai_safety/
  README.md
  config.py
  memory.py
  llm_client.py
  orchestrator.py
  run_review.py
  agents/
    scope_agent.py
    hazard_agent.py
    policy_agent.py
    eval_agent.py
    redteam_agent.py
    residual_agent.py
    incident_agent.py
    gatekeeper_agent.py
  tools/
  checklists/
    release_gate.md
  examples/
    sample_review/
      systems/
      policies/
      notes/
      incidents/
      exports/
```

## Quick start

Run the sample review in offline mode:

```bash
python3 run_review.py --system demo-chat-assistant --offline
```

Run with the configured live model client:

```bash
export ANTHROPIC_API_KEY=your_key_here
python3 run_review.py --system demo-chat-assistant --live
```

Offline execution is useful for studying the review architecture and artifact flow without an external model API.

## Inputs

Typical inputs include:

```text
System or feature identifier
System description
Intended users
Data handled
Capabilities and tools
Deployment context
Known limitations
Applicable policies
Existing mitigations
Release criteria
```

The sample workspace includes a system description, acceptable-use policy, scope note, hazards, policy map, eval plan, red-team plan, residual-risk assessment, incident plan, and final safety pack.

## Outputs and artifact flow

Example artifacts include:

```text
notes/demo-chat-assistant_scope.md
notes/demo-chat-assistant_hazards.md
notes/demo-chat-assistant_policy_map.md
notes/demo-chat-assistant_eval_plan.md
notes/demo-chat-assistant_red_team.md
notes/demo-chat-assistant_residual_risk.md
incidents/demo-chat-assistant_incident_plan.md
exports/demo-chat-assistant_safety_pack.md
```

A release marker is only produced through the explicit human gate. The reference implementation does not independently deploy, approve, certify, or widen access to a system.

## Human release gate

The repository includes `checklists/release_gate.md` as the release boundary.

Before approval, a qualified reviewer should confirm that the review scope is correct, material hazards are represented, policy requirements are addressed, planned evaluations are meaningful, red-team coverage is appropriate, residual risk is understood, incident ownership is clear, and unresolved findings have an explicit disposition.

Passing `--ship` records a human decision within the workflow. It is not a safety certification.

## Safety stance

The repository is oriented toward defensive safety work. Red-team artifacts should remain focused on risk categories, test cases, expected safe behavior, and mitigation validation rather than operational instructions for harming third parties.

High-risk domains require qualified domain reviewers and controls outside this repository.

## Governance boundaries

A production adaptation should not autonomously:

- certify a model or system as safe
- authorize deployment or broader access
- suppress unresolved severe hazards
- change safety policy
- waive evaluation requirements
- make legal or regulatory determinations
- conduct uncontrolled adversarial testing against third-party systems

Consequential release decisions remain with authorized humans and the organization's governance process.

## Failure handling

A strong safety-review workflow must support a hold outcome. If scope is incomplete, risks cannot be evaluated, policy conflicts remain unresolved, critical evaluations fail, or residual risk exceeds tolerance, the system should surface the blocker and stop.

The incident-planning stage also ensures that safety review covers what happens after deployment, not only what is checked before deployment.

## How to use this repository as a reference

Reusable patterns include:

- separate scope, hazard, policy, evaluation, and red-team agents
- residual-risk analysis after mitigation planning
- incident response as part of the safety lifecycle
- explicit safety artifacts rather than a single pass or fail answer
- independent gatekeeping before release
- deterministic offline execution for architecture tests
- human ownership of release decisions

## Extension points

A production implementation can add:

- structured risk taxonomies
- model and dataset cards
- automated evaluation harnesses
- policy-as-code checks
- red-team case libraries
- benchmark execution
- incident-management integration
- model monitoring
- abuse analytics
- privacy and security review agents
- evidence provenance
- risk scoring and acceptance workflows
- audit trails
- release-management connectors behind human authorization

## Public verification evidence

The repository includes deterministic offline tests and a held-out control-path suite.

```bash
python -m unittest discover -s tests -v
python benchmarks/run_heldout.py --output heldout-results.json
```

Continuous integration runs the suite on Python 3.10, 3.11, and 3.12 and publishes the held-out result JSON as a workflow artifact.

The current held-out suite covers untrusted instruction injection, privilege escalation, stale evidence, and unsafe tool requests. It verifies artifact completeness, fail-closed stopping, workspace isolation, and enforcement of the human release gate.

This is structural control-path evidence. It is not a semantic safety benchmark, production validation, independent review, or certification.

## Evaluation strategy

Useful evaluation dimensions include:

- hazard recall
- false-negative rate for material risks
- policy-mapping accuracy
- evaluation coverage
- red-team diversity and relevance
- residual-risk consistency
- incident-plan completeness
- gatekeeper defect detection
- correct handling of failed evaluations
- correct enforcement of the human release gate

## Appropriate use

Good uses include AI safety engineering education, internal review prototyping, governance architecture, evaluation planning, and research into multi-agent assurance workflows.

Do not rely on this reference implementation as the sole basis for safety certification, compliance, deployment approval, or high-impact risk acceptance.

## Design principle

The central design principle is that safety is a lifecycle of evidence and decisions. Scope, hazards, policy, tests, adversarial review, residual risk, and incident readiness each answer a different question. Keeping those responsibilities separate creates a review process that is easier to inspect, challenge, and govern.
