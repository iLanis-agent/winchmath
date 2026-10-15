# Winch Math

The winch honesty tool. The rating on the box is the first layer on
the drum, the layers you actually pull from each cost a cut, and the
battery keeps the minutes the spec sheet never mentions. Winch Math
sizes the box against the one-and-a-half norm, deflates the rating by
the layers on the drum, and turns the pull into amps and honest
minutes.

- Live app: https://ilanis-agent.github.io/winchmath/app.html
- Landing: https://ilanis-agent.github.io/winchmath/

## What it does

1. **The size truth** - vehicle weight x 1.5 (labeled norm) held against
   the box rating, with verdicts at 80 and 100 percent of the norm.
2. **The layer truth** - each drum layer costs about 13% (labeled norm):
   honest pull = rating x 0.87^(layers-1).
3. **The draw truth** - amps in proportion to the pull's share of the
   rating, against half the battery's usable amp-hours (labeled norm)
   into honest minutes with verdicts at 2 and 5 minutes.

## Files

- `engine.js` - pure functions (`sizePlan`, `layerPlan`, `drawPlan`) plus renderers
- `app.html` - the app; `index.html` - the landing page
- `oracle.py` - independent Python mirror of the engine
- `test.js` + `expected.json` - 28 oracle cases, `node test.js` runs green

The norms are labeled; the snatch block keeps the honest ledger.
