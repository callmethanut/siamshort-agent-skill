---
name: siamshort-module-gen-loop
description: >-
  The shot-by-shot production loop engine every video-type skill runs in Phase B: compose → generate → verify → inspect → classify deviation → apply ONE repair move → regen or accept → carry continuity → next shot, until EVERY shot of the story is done. Encodes the deviation→move table mined from 905 real prompt-iteration chains.
---

# Generation Loop Engine (Phase B of every video skill)

Run this loop over the approved shot list, in order, until every shot has an accepted clip. Maintain a visible progress board and never lose state.

## The loop (per shot)

```
1. COMPOSE   v1 prompt from the recipe modules (converged shape from the start:
             refs ≤2 scoped ± · locks · ONE beat · style/constants restated ·
             lint for placeholders) — v1 quality is where attempts are saved
2. GENERATE  one run only, never parallel; wait for TERMINAL status
3. VERIFY    terminal success? failed → step F below
4. INSPECT   view the actual output; compare against the shot's intent,
             the storyboard panel, and the previous accepted shot
5. JUDGE     acceptable → ACCEPT (step 7). Deviation → classify (table below)
6. REPAIR    apply exactly ONE move for the deviation class → regen (step 2)
             · max 3 repair attempts per shot; then keep best-so-far and
               surface the choice to the user
             · never rewrite the whole prompt — one move per attempt
7. ACCEPT    attach the clip to the shot · extract the last frame for the
             next shot's start-frame (continuity artifact, not prose) ·
             update the progress board · point spend running total
8. NEXT      proceed to the next shot; repeat until board shows ALL DONE
```

## Deviation → repair move (mined from 905 iteration chains)

| deviation class | ONE move |
|---|---|
| identity/face drift | add the face-scope list to the ref, or reframe to body-part focus (hands/back) |
| wrong position / continuity break | attach extracted frame as start-frame + name 2–4 continuity anchors (red shirt, prop-in-left-hand) |
| camera wrong (angle/move/cuts) | lock camera line ("Smart Cuts OFF, one continuous take") or restate witness position; ONE named move only |
| pacing/beat order wrong | add time-blocks (0-3s / 3-7s / …) |
| action feels fake / floaty | write the causal chain + REFLEX (recoil/stagger/brace); slow-motion the beat |
| style drift from earlier shots | restate the series constants block verbatim (style sentence, wardrobe, framing rule) |
| unwanted element appears | ONE targeted negative for that element (no hands / no extra limbs / no silhouettes) |
| text/logo/watermark baked in | add the no-overlay barrage |
| ref leaking wrong attribute | tighten scoping both ways ("use ONLY for X — must NOT control camera/background") |

## Failure branch (F)

- **content-policy failure** (real person, sensitive, copyright — 43% of all platform failures): do NOT retry the same input. Real-person image → reroute to the virtual-asset flow; risky phrasing → rewrite the flagged element, then one retry.
- **infra/timeout/reaped**: retry once unchanged; second failure → mark shot blocked, continue to the next shot, report at the end.
- Always confirm refund/points state on failures before retrying.

## Gate policy (set at intake, per production)

- `review-each` — pause for user OK after every accepted shot (default for first-time users)
- `auto-run` — continue automatically while shots pass inspection; pause ONLY on: repair cap reached, policy failure, budget threshold crossed, or story milestone (end of scene). This is the mode that finishes a whole story unattended.
- Either mode: a bounded points estimate was confirmed BEFORE the loop started; stop and re-confirm if projected spend exceeds it.

## Loop discipline (non-negotiable)

- One generation in flight at a time. Never claim success on queued/running/unverified runs.
- Progress board after every shot: `#shot · status(done/repairing/blocked) · attempts · points`.
- Resume from the board — never regenerate accepted shots on session resume.
- Every repair attempt logs: deviation class → move applied (this record is the production's learning trail).
