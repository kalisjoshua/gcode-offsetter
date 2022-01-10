const rValues = /([EFXYZ])(\d+(?:\.\d+)?)/g;

function center(q, width) {
  const str = q.toString();
  const len = str.length;
  const start = len + Math.floor((width - len + 1) / 2);

  return str.padStart(start, " ").padEnd(width, " ");
}

// delay to run script from user input
function debounce(fn, delay = 300) {
  let pending;

  function postponed(...args) {
    pending && clearTimeout(pending);

    pending = setTimeout(fn.bind(this, ...args), delay);
  }

  return postponed;
}

function findExtremes(data) {
  return data.match(rValues).reduce((acc, match) => {
    const [axis, ...parts] = match;
    const value = parseFloat(parts.join(""));

    if (!acc[axis]) acc[axis] = [Number.MAX_SAFE_INTEGER, 0];

    acc[axis] = [Math.min(acc[axis][0], value), Math.max(acc[axis][1], value)];

    return acc;
  }, {});
}

function getStats(before, after) {
  const statsBefore = findExtremes(before);
  const statsAfter = findExtremes(after);

  return Reflect.ownKeys(statsBefore).map((letter) => [
    letter,
    statsBefore[letter],
    statsAfter[letter]
  ]);
}

// initialize the page elements with an event handler for onkeyup
function init() {
  const allInputs = document.querySelectorAll("input, textarea");

  Array.from(allInputs).reduce((elements, el) => {
    elements[el.name] = el;

    // assign the event handler to each element on the page
    el.onkeyup = debounce(() => update(elements));

    return elements;
  }, {});
}

// called on debounce from element update
function update({
  ERate,
  FRate,
  LimX,
  LimY,
  LimZ,
  OffsetX,
  OffsetY,
  OffsetZ,
  Result,
  Source
}) {
  const limits = {
    X: parseFloat(LimX.value),
    Y: parseFloat(LimY.value),
    Z: parseFloat(LimZ.value)
  };
  const offsets = {
    X: parseFloat(OffsetX.value),
    Y: parseFloat(OffsetY.value),
    Z: parseFloat(OffsetZ.value)
  };
  const scales = {
    E: parseFloat(ERate.value),
    F: parseFloat(FRate.value)
  };

  Result.value = Source.value.replace(rValues, (match, axis, value) => {
    value = parseFloat(value);

    if (["X", "Y", "Z"].includes(axis)) {
      return axis + Math.max(Math.min(value + offsets[axis], limits[axis]), 0);
    } else if (["E", "F"].includes(axis)) {
      return axis + (value * scales[axis]) / 100.0;
    }
  });

  const stats = getStats(Source.value, Result.value);
  const maxLength =
    JSON.stringify(stats)
      .match(/\d+(?:\.\d+)?/g)
      .reduce((a, b) => (a.length > b.length ? a : b))
      .toString().length + 6; // "6" is just extra - white-space - between columns

  document.querySelector("#stats").innerText = [
    ["Variable", "min Before", "min After", "max Before", "max After"],
    ...stats.map(([variable, [minBefore, maxBefore], [minAfter, maxAfter]]) => [
      variable,
      minBefore,
      minAfter,
      maxBefore,
      maxAfter
    ])
  ]
    .map((line) => line.map((q) => center(q, maxLength)).join(" "))
    .join("\n");
}

// call init routine after page fully loaded
window.addEventListener("DOMContentLoaded", init);
