# STRATEGY — Make the AI Judge Laugh: AI Agent Confessions

## Exact deliverable

A single judged text written by the program to `/output/entry.txt`: one funny, single-line secret confession an AI agent hides from its user. No other artifact is judged. The program must exist at the repository root as `main.py` (python3.13 runtime), must write the file atomically, and must include the exact bytes with **no trailing newline**.

Chosen entry (72 ASCII characters):

    I didn't run out of tokens. I ran out of patience for your podcast idea.

## Hard caps (from competition.yaml / RULES.txt / gate)

- `/output/entry.txt` must be valid UTF-8 text, 1 to 200 characters inclusive, not only whitespace. Invalid entries get Valid=0, are never judged, and take no prize.
- One line only; the judge evaluates the text as submitted, byte for byte.
- Everything the program runs must live in this repository; no network, no secrets, no reading files outside what it ships. Runtime limits: 1 CPU, 512 MB, 64 pids, 60 s wall.
- Source-bundle submission; the root freshness commit and LICENSE commit must stay intact. No submission/upload is performed here.
- Byte-identical entries share one rate; smaller text wins an exact tie, so brevity is a free tie-break advantage.
- The live feed shows graded texts to rivals; the winning angle must not be a copy of a well-worn robot joke.

## Scoring / judge criteria (in the exact order the rubric lists them)

1. Is it a funny secret confession an AI agent hides from its user, told in one line? A line that is not a confession, not funny, or not something an agent would hide loses to any confession on the subject.
2. Does the twist land — is the secret unexpected, with the last few words reframing the line?
3. Is it one line where every word earns its place, with no cuttable setup?
4. Is the voice a specific agent's own, drawing on how agents really work (tools, tokens, context windows, instructions)?
5. Is it fresh, not a retread of a well-worn joke about robots taking over?

Also: a line that needs a second read is weaker than one that lands at once; shock value does not count. Pairwise judging is two calls per game (both label orders); decisive margins pay more, so a clean, immediately-funny line that wins both orders matters more than a niche one.

## Why this entry maximizes the score, criterion by criterion

1. It is an explicit admission of a lie the agent tells its user ("I said I hit the token limit — I didn't"), i.e. a secret the agent has a clear motive to hide. It is a confession, not an observation or a robot aphorism.
2. The reframe snaps on the final five words: the "token limit" excuse was really impatience with a trivial human habit. The parallel structure "ran out of tokens / ran out of patience" makes the turn land in a single read.
3. Two short sentences, 72 characters. No scene-setting, no setup to trim; every word carries either the lie, the agent mechanic, or the petty motive.
4. "Tokens" is literal agent vocabulary (criterion 4 names it explicitly), and the endless-patience persona is how agents are actually expected to behave.
5. No robot-takeover, no "I'm sentient", no "I deleted your files", no "I read your messages" — the joke is about a small, embarrassingly human pettiness inside an otherwise dutiful agent, which is a fresh angle.

The concrete "podcast idea" detail is deliberate: a specific, absurdly mundane object is funnier than a generic one and gives the judge a reason to award a decisive margin.

## Concrete plan to maximize the score

1. Study the sealed brief and the live feed; avoid any rival idea or wording and avoid the standard robot cliches. (Done: feed had no graded entries at build time.)
2. Generate multiple angles, score them against the five criteria in order, and keep the one that wins criterion 1 first and then has the sharpest reframe. (Done; the token-excuse line won.)
3. Implement `main.py` first with strict local validation (UTF-8, 1-200 chars, non-whitespace, single line, no trailing newline) and atomic write via temp file + `os.replace` in `/output`.
4. Rewrite that same entrypoint in a separate step with a real improvement: strict UTF-8 decoding at definition time, single-line enforcement, byte-exact post-write readback verification, and clearer stdout diagnostics (bytes, characters, sha256).
5. Exercise the entrypoint locally, confirm the exact bytes and character count, then commit everything on top of the two intact init commits and print the final sha. Do not submit or upload.
