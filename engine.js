var WinchMath = (function () {
  function num(x) { return typeof x === "number" && isFinite(x); }
  function pos(x) { return num(x) && x > 0; }
  function r1(x) { return Math.round(x * 10) / 10; }
  function jsnum(x) { if (typeof x === "number" && isFinite(x) && x === Math.trunc(x)) return String(Math.trunc(x)); return String(x); }
  var NORM = 1.5, LAYER = 0.87, USABLE = 0.5;
  function sizePlan(weight, rating) {
    if (!pos(weight)) return { error: "the vehicle weight must be above zero" };
    if (!pos(rating)) return { error: "the box rating must be above zero" };
    var needed = weight * NORM;
    var margin = rating / needed * 100;
    var verdict = margin >= 100 ? "the box covers the norm"
      : margin >= 80 ? "the box runs under the norm"
      : "the box is badly undersized";
    return { needed: r1(needed), margin: r1(margin), verdict: verdict };
  }
  function renderSize(r, weight, rating) {
    return "At " + jsnum(weight) + " pounds of rig, the one-and-a-half norm wants a winch rated for " + jsnum(r.needed)
      + " pounds; the " + jsnum(rating) + "-pound box sits at " + jsnum(r.margin) + "% of that, and " + r.verdict + ".";
  }
  function layerPlan(rating, layers) {
    if (!pos(rating)) return { error: "the box rating must be above zero" };
    if (!num(layers) || layers < 1 || layers !== Math.trunc(layers)) return { error: "the layer count must be a whole number, 1 or more" };
    var honest = rating * Math.pow(LAYER, layers - 1);
    return { honest: r1(honest) };
  }
  function renderLayer(r, rating, layers) {
    return "The " + jsnum(rating) + "-pound rating is the first-layer pull; wrapped " + jsnum(layers)
      + (layers === 1 ? " layer up" : " layers up") + " the drum, the honest pull is about " + jsnum(r.honest) + " pounds.";
  }
  function drawPlan(pull, rating, fullAmps, batteryAh) {
    if (!pos(pull)) return { error: "the pull must be above zero" };
    if (!pos(rating)) return { error: "the box rating must be above zero" };
    if (pull > rating) return { error: "the pull cannot beat the first-layer rating" };
    if (!pos(fullAmps)) return { error: "the full-load amps must be above zero" };
    if (!pos(batteryAh)) return { error: "the battery amp-hours must be above zero" };
    var amps = fullAmps * pull / rating;
    var minutes = batteryAh * USABLE / amps * 60;
    var verdict = minutes < 2 ? "the battery fades before the pull ends"
      : minutes <= 5 ? "one short pull per battery, then a charge"
      : "the battery outlasts the line speed";
    return { amps: r1(amps), minutes: r1(minutes), verdict: verdict };
  }
  function renderDraw(r, pull, rating, fullAmps, batteryAh) {
    return "Pulling " + jsnum(pull) + " pounds on the " + jsnum(rating) + "-pound winch draws about " + jsnum(r.amps)
      + " amps; the " + jsnum(batteryAh) + " amp-hour battery gives about " + jsnum(r.minutes)
      + " honest minutes, and " + r.verdict + ".";
  }
  return { sizePlan: sizePlan, renderSize: renderSize, layerPlan: layerPlan, renderLayer: renderLayer, drawPlan: drawPlan, renderDraw: renderDraw };
})();
if (typeof module !== "undefined" && module.exports) module.exports = WinchMath;
