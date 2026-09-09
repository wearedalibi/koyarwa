/*
 * Petits comportements d'interface, sans dépendance :
 *  - bouton œil (afficher/masquer) sur les champs [data-pw]
 *  - jauge de force du mot de passe sur [data-strength]
 * Réinitialisés au chargement et après chaque swap HTMX.
 */
(function () {
  var LEVELS = ["s0", "s1", "s2", "s3", "s4"];

  function variety(pw) {
    var v = 0;
    if (/[a-z]/.test(pw)) v++;
    if (/[A-Z]/.test(pw)) v++;
    if (/[0-9]/.test(pw)) v++;
    if (/[^A-Za-z0-9]/.test(pw)) v++;
    return v;
  }

  function score(pw) {
    if (!pw) return 0;
    var s = 0;
    if (pw.length >= 8) s++;
    if (pw.length >= 12) s++;
    s += Math.max(0, variety(pw) - 1);
    return Math.min(s, 4);
  }

  function isStrong(pw) {
    return pw.length >= 10 && variety(pw) >= 3;
  }

  function initToggles(root) {
    root.querySelectorAll("[data-pw]:not([data-pw-ready])").forEach(function (wrap) {
      wrap.setAttribute("data-pw-ready", "");
      var input = wrap.querySelector("input");
      var btn = wrap.querySelector("[data-pw-toggle]");
      if (!input || !btn) return;
      btn.addEventListener("click", function () {
        var reveal = input.type === "password";
        input.type = reveal ? "text" : "password";
        btn.innerHTML = '<i data-lucide="' + (reveal ? "eye-off" : "eye") + '"></i>';
        btn.setAttribute("aria-pressed", reveal ? "true" : "false");
        if (window.lucide) window.lucide.createIcons();
        input.focus();
      });
    });
  }

  function initStrength(root) {
    root.querySelectorAll("[data-strength]:not([data-strength-ready])").forEach(function (meter) {
      meter.setAttribute("data-strength-ready", "");
      var input = document.getElementById(meter.getAttribute("data-for"));
      if (!input) return;
      var labels = {};
      try {
        labels = JSON.parse(meter.getAttribute("data-labels") || "{}");
      } catch (e) {
        labels = {};
      }
      var label = meter.querySelector(".strength-label");
      var form = input.closest("form");
      var submit = form ? form.querySelector('button[type="submit"]') : null;

      function update() {
        var pw = input.value;
        var s = score(pw);
        LEVELS.forEach(function (c) {
          meter.classList.remove(c);
        });
        meter.classList.add(LEVELS[s]);
        if (label) label.textContent = pw ? labels[String(s)] || "" : "";
        if (submit) submit.disabled = !isStrong(pw);
      }

      input.addEventListener("input", update);
      update();
    });
  }

  function init(root) {
    initToggles(root || document);
    initStrength(root || document);
  }

  document.addEventListener("DOMContentLoaded", function () {
    init(document);
  });
  document.addEventListener("htmx:afterSettle", function (e) {
    init(e.target || document);
  });
})();
