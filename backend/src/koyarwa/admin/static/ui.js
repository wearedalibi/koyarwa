/*
 * Petits comportements d'interface, sans dépendance :
 *  - thème clair/sombre (switcher [data-theme-toggle], préférence persistée)
 *  - bouton œil (afficher/masquer) sur les champs [data-pw]
 *  - jauge de force du mot de passe sur [data-strength]
 * Réinitialisés au chargement et après chaque swap HTMX.
 */
(function () {
  var LEVELS = ["s0", "s1", "s2", "s3", "s4"];

  // ── Thème clair/sombre ──────────────────────────────────────────────
  var THEME_KEY = "koyarwa-theme";

  function storedTheme() {
    try {
      return localStorage.getItem(THEME_KEY);
    } catch (e) {
      return null;
    }
  }

  function systemDark() {
    return !!(window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches);
  }

  function effectiveTheme() {
    var forced = document.documentElement.getAttribute("data-theme");
    if (forced === "light" || forced === "dark") return forced;
    return systemDark() ? "dark" : "light";
  }

  // Appliqué immédiatement : ce script est chargé dans <head>, donc avant le rendu
  // du <body> → la préférence enregistrée s'applique sans flash de thème.
  (function applyStoredTheme() {
    var t = storedTheme();
    if (t === "light" || t === "dark") document.documentElement.setAttribute("data-theme", t);
  })();

  function paintThemeToggle(btn) {
    var t = effectiveTheme();
    // En sombre on propose de passer au clair (soleil) ; en clair, à l'inverse (lune).
    btn.innerHTML = '<i data-lucide="' + (t === "dark" ? "sun" : "moon") + '"></i>';
    btn.setAttribute("aria-label", t === "dark" ? "Passer au thème clair" : "Passer au thème sombre");
    if (window.lucide) window.lucide.createIcons();
  }

  function initTheme(root) {
    root.querySelectorAll("[data-theme-toggle]:not([data-theme-ready])").forEach(function (btn) {
      btn.setAttribute("data-theme-ready", "");
      paintThemeToggle(btn);
      btn.addEventListener("click", function () {
        var next = effectiveTheme() === "dark" ? "light" : "dark";
        document.documentElement.setAttribute("data-theme", next);
        try {
          localStorage.setItem(THEME_KEY, next);
        } catch (e) {
          /* stockage indisponible : la bascule reste valable pour la session */
        }
        document.querySelectorAll("[data-theme-toggle]").forEach(paintThemeToggle);
      });
    });
  }

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

  // ── Sélecteur de pays cherchable (datalist + noms localisés) ─────────
  // Codes ISO 3166-1 alpha-2 ; les libellés sont localisés côté client via
  // Intl.DisplayNames selon la langue de la page (pas de liste en dur par langue).
  var COUNTRY_CODES = (
    "AD AE AF AG AI AL AM AO AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BJ BL BM BN " +
    "BO BQ BR BS BT BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CW CX CY CZ " +
    "DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK FM FO FR GA GB GD GE GF GG GH GI " +
    "GL GM GN GP GQ GR GT GU GW GY HK HN HR HT HU ID IE IL IM IN IO IQ IR IS IT JE JM " +
    "JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD " +
    "ME MF MG MH MK ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL " +
    "NO NP NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RE RO RS RU RW SA " +
    "SB SC SD SE SG SH SI SJ SK SL SM SN SO SR SS ST SV SX SY SZ TC TD TG TH TJ TK TL " +
    "TM TN TO TR TT TV TW TZ UA UG US UY UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW"
  ).split(" ");

  function initCountry(root) {
    root.querySelectorAll("select[data-country-select]:not([data-country-ready])").forEach(
      function (sel) {
        sel.setAttribute("data-country-ready", "");
        var lang = document.documentElement.getAttribute("lang") || "en";
        var names = null;
        try {
          names = new Intl.DisplayNames([lang], { type: "region" });
        } catch (e) {
          names = null;
        }
        var current = sel.getAttribute("data-selected") || "";
        var items = [];
        COUNTRY_CODES.forEach(function (code) {
          var label = names ? names.of(code) : code;
          if (label && label !== code) items.push({ code: code, label: label });
        });
        items.sort(function (a, b) {
          return a.label.localeCompare(b.label, lang);
        });
        // Conserve l'option vide (placeholder) déjà présente ; ajoute les pays.
        items.forEach(function (item) {
          var opt = document.createElement("option");
          opt.value = item.code;
          opt.textContent = item.label;
          if (item.code === current) opt.selected = true;
          sel.appendChild(opt);
        });
      }
    );
  }

  function init(root) {
    initTheme(root || document);
    initToggles(root || document);
    initStrength(root || document);
    initCountry(root || document);
  }

  document.addEventListener("DOMContentLoaded", function () {
    init(document);
  });
  document.addEventListener("htmx:afterSettle", function (e) {
    init(e.target || document);
  });
})();
