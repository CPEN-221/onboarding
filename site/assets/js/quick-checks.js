(function () {
  "use strict";

  function selectedValues(fieldset) {
    var selected = fieldset.querySelectorAll(
      'input[type="radio"]:checked, input[type="checkbox"]:checked'
    );
    var values = [];

    for (var index = 0; index < selected.length; index += 1) {
      values.push(selected[index].value);
    }

    return values.sort();
  }

  function expectedValues(form) {
    return form.getAttribute("data-answer").split(",").map(function (value) {
      return value.trim();
    }).filter(Boolean).sort();
  }

  function sameValues(left, right) {
    if (left.length !== right.length) {
      return false;
    }

    for (var index = 0; index < left.length; index += 1) {
      if (left[index] !== right[index]) {
        return false;
      }
    }
    return true;
  }

  document.addEventListener("DOMContentLoaded", function () {
    var checks = document.querySelectorAll("form[data-quick-check][data-answer]");

    for (var index = 0; index < checks.length; index += 1) {
      (function (form, checkNumber) {
        var fieldset = form.querySelector("fieldset");
        var explanation = form.querySelector("details");
        if (!fieldset) {
          return;
        }

        var button = document.createElement("button");
        button.type = "button";
        button.className = "quick-check-button";
        button.textContent = "Check answer";

        var result = document.createElement("p");
        result.className = "quick-check-result";
        result.id = "quick-check-result-" + checkNumber;
        result.setAttribute("aria-live", "polite");

        button.setAttribute("aria-describedby", result.id);
        form.insertBefore(button, explanation || null);
        form.insertBefore(result, explanation || null);
        form.setAttribute("data-enhanced", "true");

        button.addEventListener("click", function () {
          var selected = selectedValues(fieldset);
          result.classList.remove("is-correct", "is-incorrect");

          if (selected.length === 0) {
            result.textContent = "Choose an answer before checking.";
            return;
          }

          if (sameValues(selected, expectedValues(form))) {
            result.textContent = "Correct. Open the explanation to compare the reasoning.";
            result.classList.add("is-correct");
          } else {
            result.textContent = "Not yet. Trace the values or control flow and try again.";
            result.classList.add("is-incorrect");
          }
        });
      }(checks[index], index + 1));
    }
  });
}());
