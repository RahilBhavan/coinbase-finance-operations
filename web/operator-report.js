(function () {
  "use strict";
  var picker = document.getElementById("case-picker");
  var panels = Array.prototype.slice.call(document.querySelectorAll(".case-panel"));
  var actionable = document.getElementById("filter-actionable");
  var blocked = document.getElementById("filter-blocked");
  var filterStatus = document.getElementById("filter-status");
  document.documentElement.classList.remove("no-js");
  document.documentElement.classList.add("js");

  function matches(panel) {
    if (!actionable.checked && !blocked.checked) return true;
    return (actionable.checked && panel.dataset.actionable === "true") ||
      (blocked.checked && panel.dataset.blocked === "true");
  }
  function showSelected() {
    var selected = Number(picker.value);
    panels.forEach(function (panel, index) { panel.hidden = index !== selected || !matches(panel); });
  }
  function refreshOptions() {
    var visible = 0;
    Array.prototype.forEach.call(picker.options, function (option, index) {
      var show = matches(panels[index]);
      option.hidden = !show;
      option.disabled = !show;
      if (show) visible += 1;
    });
    if (!matches(panels[Number(picker.value)])) {
      var first = Array.prototype.find.call(picker.options, function (option) { return !option.disabled; });
      if (first) picker.value = first.value;
    }
    filterStatus.textContent = visible + " case(s) match the active filters.";
    showSelected();
  }
  picker.addEventListener("change", showSelected);
  actionable.addEventListener("change", refreshOptions);
  blocked.addEventListener("change", refreshOptions);
  document.querySelectorAll(".unsafe-action").forEach(function (button) {
    button.addEventListener("click", function () {
      var status = button.parentElement.querySelector(".refusal");
      status.textContent = "REFUSED — original payment remains unresolved. Recharge was not sent.";
      status.classList.add("is-refused");
      button.textContent = "Recharge refused";
      button.disabled = true;
    });
  });
}());
