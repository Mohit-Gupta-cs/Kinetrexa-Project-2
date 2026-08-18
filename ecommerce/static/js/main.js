/* ============================================================
   UrbanKart — front-end behaviour
   Toasts, AJAX add-to-cart, cart quantity steppers.
   ============================================================ */
(function () {
  "use strict";

  /* ---------- CSRF ---------- */
  function getCookie(name) {
    let value = null;
    if (document.cookie && document.cookie !== "") {
      document.cookie.split(";").some(function (c) {
        c = c.trim();
        if (c.substring(0, name.length + 1) === name + "=") {
          value = decodeURIComponent(c.substring(name.length + 1));
          return true;
        }
        return false;
      });
    }
    return value;
  }
  var CSRF = getCookie("csrftoken");

  /* ---------- Indian currency formatting ---------- */
  function groupINR(n) {
    var s = String(Math.round(n));
    if (s.length <= 3) return s;
    var head = s.slice(0, -3);
    var tail = s.slice(-3);
    var groups = [];
    while (head.length > 2) {
      groups.unshift(head.slice(-2));
      head = head.slice(0, -2);
    }
    groups.unshift(head);
    return groups.join(",") + "," + tail;
  }
  function fmtINR(n) {
    n = Number(n) || 0;
    return "₹" + groupINR(n);
  }

  /* ---------- Toasts ---------- */
  var container = document.getElementById("toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "toast-container";
    document.body.appendChild(container);
  }
  function showToast(text, type) {
    type = type || "success";
    var el = document.createElement("div");
    el.className = "toast " + type;
    el.innerHTML = '<span class="dot"></span><span></span>';
    el.querySelector("span:last-child").textContent = text;
    container.appendChild(el);
    setTimeout(function () {
      el.classList.add("out");
      setTimeout(function () { el.remove(); }, 350);
    }, 3200);
  }
  // Django messages delivered on page load.
  if (window.__djangoMessages) {
    window.__djangoMessages.forEach(function (m) {
      showToast(m.text, m.type === "error" ? "error" : m.type === "warning" ? "info" : m.type);
    });
  }

  /* ---------- Cart badge ---------- */
  function setBadge(count) {
    var badge = document.getElementById("cart-badge");
    if (!badge) return;
    badge.textContent = count;
    badge.style.display = count > 0 ? "grid" : "none";
  }

  /* ---------- AJAX add-to-cart ---------- */
  document.querySelectorAll("form[data-add-to-cart]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var url = form.action;
      var body = new URLSearchParams(new FormData(form));
      var btn = form.querySelector("button[type=submit]");
      if (btn) { btn.disabled = true; }
      fetch(url, {
        method: "POST",
        headers: { "X-CSRFToken": CSRF, "X-Requested-With": "XMLHttpRequest" },
        body: body,
      })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (data.ok) {
            setBadge(data.count);
            var name = form.getAttribute("data-product-name") || "Item";
            showToast(name + " added to cart ✓");
          }
        })
        .catch(function () { window.location.href = url; })
        .finally(function () {
          if (btn) { setTimeout(function () { btn.disabled = false; }, 600); }
        });
    });
  });

  /* ---------- Cart page helpers ---------- */
  function refreshCartTotals(data) {
    var subtotalEl = document.getElementById("cart-subtotal");
    var shippingEl = document.getElementById("cart-shipping");
    var totalEl = document.getElementById("cart-total");
    var barEl = document.getElementById("free-ship-bar");
    var msgEl = document.getElementById("free-ship-msg");
    var freeShipEl = document.getElementById("free-ship-box");

    if (subtotalEl) subtotalEl.textContent = fmtINR(data.subtotal);
    if (shippingEl) {
      var ship = Number(data.shipping);
      shippingEl.textContent = ship === 0 ? "FREE" : fmtINR(ship);
      shippingEl.classList.toggle("free", ship === 0);
    }
    if (totalEl) totalEl.textContent = fmtINR(data.total);

    var subtotal = Number(data.subtotal);
    if (barEl) {
      var threshold = Number(barEl.getAttribute("data-threshold")) || 999;
      var pct = Math.min(100, (subtotal / threshold) * 100);
      barEl.style.width = pct + "%";
    }
    if (msgEl) {
      var threshold = Number(msgEl.getAttribute("data-threshold")) || 999;
      if (subtotal >= threshold) {
        msgEl.textContent = "🎉 You've unlocked FREE shipping!";
      } else {
        msgEl.textContent =
          "Add " + fmtINR(threshold - subtotal) + " more for FREE shipping";
      }
    }
    if (freeShipEl) freeShipEl.style.display = "block";
  }

  function emptyCart(container) {
    if (!container) return;
    var html =
      '<div class="cart-empty">' +
      '<svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">' +
      '<path d="M6 6h15l-1.5 8.5a2 2 0 0 1-2 1.5H8.6a2 2 0 0 1-2-1.6L4.3 3.4A1 1 0 0 0 3.3 2.6H2"/><circle cx="10" cy="20" r="1.4"/><circle cx="17" cy="20" r="1.4"/>' +
      "</svg>" +
      "<h2>Your cart is empty</h2>" +
      "<p>Looks like you haven't added anything yet.</p>" +
      '<a class="btn btn-primary" href="/shop/">Start shopping</a>' +
      "</div>";
    container.innerHTML = html;
  }

  /* Quantity steppers on the cart page */
  document.querySelectorAll("[data-qty-btn]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var row = btn.closest("[data-cart-line]");
      var input = row.querySelector("[data-qty-input]");
      var productId = row.getAttribute("data-product-id");
      var action = btn.getAttribute("data-action");
      var current = parseInt(input.value, 10) || 0;
      var next = action === "inc" ? current + 1 : current - 1;
      if (next <= 0) return; // user must use the remove link
      input.value = next;

      var body = new URLSearchParams();
      body.set("quantity", next);
      fetch("/cart/update/" + productId + "/", {
        method: "POST",
        headers: { "X-CSRFToken": CSRF },
        body: body,
      })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (!data.ok) return;
          setBadge(data.count);
          var lineTotal = row.querySelector("[data-line-total]");
          if (lineTotal) lineTotal.textContent = fmtINR(data.line_total);
          refreshCartTotals(data);
        });
    });
  });

  /* Remove buttons on the cart page */
  document.querySelectorAll("[data-remove-item]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var row = btn.closest("[data-cart-line]");
      var productId = row.getAttribute("data-product-id");
      var body = new URLSearchParams();
      fetch("/cart/remove/" + productId + "/", {
        method: "POST",
        headers: { "X-CSRFToken": CSRF, "X-Requested-With": "XMLHttpRequest" },
        body: body,
      })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (!data.ok) return;
          row.remove();
          // recompute everything client-side
          var rows = document.querySelectorAll("[data-cart-line]");
          if (rows.length === 0) {
            emptyCart(document.getElementById("cart-items"));
            var summary = document.querySelector(".summary-card");
            if (summary) summary.style.display = "none";
            var layout = document.querySelector(".cart-layout");
            if (layout) layout.style.justifyContent = "center";
            setBadge(0);
            return;
          }
          // simplest reliable approach: reload to recalc totals
          window.location.reload();
        });
    });
  });

  /* Product-detail quantity stepper (client side only) */
  document.querySelectorAll("[data-detail-qty]").forEach(function (wrap) {
    var input = wrap.querySelector("input");
    var min = parseInt(input.min, 10) || 1;
    var max = parseInt(input.max, 10) || 99;
    wrap.querySelectorAll("button").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var current = parseInt(input.value, 10) || min;
        var next = btn.getAttribute("data-action") === "inc" ? current + 1 : current - 1;
        input.value = Math.min(max, Math.max(min, next));
      });
    });
  });

  /* Sort dropdown auto-submit */
  var sortSelect = document.getElementById("sort-select");
  if (sortSelect) {
    sortSelect.addEventListener("change", function () {
      var url = new URL(window.location.href);
      if (this.value) url.searchParams.set("sort", this.value);
      else url.searchParams.delete("sort");
      window.location.href = url.toString();
    });
  }
})();
