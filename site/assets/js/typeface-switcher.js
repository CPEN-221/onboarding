(function () {
  "use strict";

  var storageKey = "cpen221-java-typeface";
  var allowed = ["plex", "google-sans"];

  function valid(value) {
    return allowed.indexOf(value) !== -1;
  }

  function storedChoice() {
    try {
      var value = window.localStorage.getItem(storageKey);
      return valid(value) ? value : "plex";
    } catch (error) {
      return "plex";
    }
  }

  function apply(value) {
    document.documentElement.setAttribute("data-typeface", value);
  }

  var initial = storedChoice();
  apply(initial);

  document.addEventListener("DOMContentLoaded", function () {
    var picker = document.querySelector("[data-typeface-picker]");
    if (!picker) {
      return;
    }

    picker.value = initial;
    picker.addEventListener("change", function () {
      var value = valid(picker.value) ? picker.value : "plex";
      apply(value);
      try {
        window.localStorage.setItem(storageKey, value);
      } catch (error) {
        // The selection still applies for this page when storage is unavailable.
      }
    });
  });
}());
