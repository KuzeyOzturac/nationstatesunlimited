# Model contract
Save schema version 1. All nine indicators range from 0 to 100. They are local index points, not official census scores.
For an authored effect e and current score s:
- e > 0: delta = e * (100-s)/100
- e < 0: delta = e * s/100
Round delta to two decimal places, clamp the result, record exact delta in history.
Country classification is a simplified local label using civil, political and economic freedom. It is not the official 27-category matrix.

Eligibility currently models a competitive-election prerequisite for voting age, a twelve-turn cooldown, and no reenactment of an identical policy. It does not model official population thresholds, special issues, holidays, easter eggs, or hidden flags. Recurrence supports reversals, with at least two responses always available.

No timers, offline growth, real-money economy, multiplayer, official account integration, or external API calls. Population starts at five million and grows 0.1% per enactment; this is a pacing choice rather than an official rule. History retains 500 events. Save validation enforces bounds and recognized policies and issue IDs. The UI escapes every user-provided value before HTML interpolation.
