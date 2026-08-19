# Agentic AI Safety

Multi agent workflow for **AI safety review** of a system or feature: scope the risk, map hazards, check policies, plan evals, red team prompts (defensive), score residual risk, and stop for a human approval gate.

This is an engineering and governance helper. It does not certify a model as safe. It does not replace legal, security, or ethics review.

## Quick start

```bash
cd agentic_ai_safety
python3 run_review.py --system demo-chat-assistant --offline
```

Live (optional):

```bash
export ANTHROPIC_API_KEY=sk-...
python3 run_review.py --system demo-chat-assistant --live
```

## Agents

| Agent | Role |
|-------|------|
| Scope | What is in review, users, data, capabilities |
| Hazard | Plausible harm classes and misuse paths |
| Policy | Map to internal policy and usage rules |
| Eval planner | Tests and metrics before wider release |
| Red team | Defensive probe ideas and expected refusals |
| Residual risk | What remains after mitigations |
| Incident | If something goes wrong, who does what |
| Gatekeeper | Final pack and human approve checklist |

## Human gate

Nothing is marked approved for release unless you pass `--ship`. Humans own go or no go.

## Safety stance

- Offline stand ins never invent real exploit recipes for attacks on third parties  
- Red team notes stay at the level of categories and test ideas  
- High risk domains need qualified reviewers outside this tool  
