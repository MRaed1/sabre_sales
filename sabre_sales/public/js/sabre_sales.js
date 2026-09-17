// Sabre Sales — global notification sound + desktop popup
// Loaded on every page via app_include_js (see hooks.py)

$(document).on('app_ready', function () {

	if (window.Notification && Notification.permission === 'default') {
		Notification.requestPermission();
	}

	frappe.realtime.on('new_notification', function (data) {
		try {
			let audio = new Audio('/assets/frappe/sounds/alert.mp3');
			audio.play().catch(() => {});
		} catch (e) {}

		if (window.Notification && Notification.permission === 'granted') {
			new Notification(data.subject || 'New notification', {
				body: data.email_content ? $('<div>').html(data.email_content).text() : '',
				icon: '/assets/frappe/images/frappe-favicon.svg'
			});
		}
	});

});

/* ==== MT NOTIFICATION BADGE - START (managed block) ==== */
/* ===================================================================
 * Unread notification counter on the sidebar bell
 * Portable block - safe to copy to any Frappe 16 site
 * -------------------------------------------------------------------
 * WHY THIS EXISTS
 *   Frappe's own bell indicator is purely live: notifications.js shows the
 *   dot on a realtime "notification" event and hides it on "indicator_hide".
 *   On page load it starts hidden, so a user with 46 unread sees a plain
 *   bell. This paints the actual unread count and keeps it current.
 *
 * WHAT IT HOOKS
 *   .sidebar-notification  - the bell item in the v16 desk sidebar
 *   frappe.realtime "notification" / "indicator_hide" - the events Frappe
 *   already fires, so no polling is needed for live updates.
 *
 * KNOWN FRAGILITY
 *   It targets a Frappe CSS class. If a future version renames it the badge
 *   silently stops appearing - it will not break anything else. If the badge
 *   vanishes after an upgrade, check that .sidebar-notification still exists.
 * =================================================================== */
(function () {
	"use strict";

	var BADGE_CLASS = "mt-notif-badge";
	var MAX_TRIES = 40; // ~20s, the sidebar is built asynchronously
	var tries = 0;
	var started = false;

	function bell() {
		return document.querySelector(".sidebar-notification");
	}

	/* The bell markup is:
	 *   .sidebar-notification > .standard-sidebar-item > a.item-anchor
	 *       > span.sidebar-item-icon  (the svg)
	 *       > span.sidebar-item-label ("Notification")
	 * The badge sits INSIDE .sidebar-item-icon, absolutely positioned, so it
	 * rides the corner of the bell and still shows when the sidebar is
	 * collapsed and the label is hidden. */
	function iconHost(host) {
		return (
			host.querySelector(".sidebar-item-icon") ||
			host.querySelector(".item-anchor") ||
			host
		);
	}

	function paint(count) {
		var host = bell();
		if (!host) return false;

		var anchor = iconHost(host);
		var badge = host.querySelector("." + BADGE_CLASS);

		if (!count) {
			if (badge) badge.remove();
			return true;
		}

		// If an earlier version left the badge in the wrong parent, move it.
		if (badge && badge.parentNode !== anchor) {
			badge.remove();
			badge = null;
		}

		if (!badge) {
			badge = document.createElement("span");
			badge.className = BADGE_CLASS;
			anchor.appendChild(badge);
		}

		// the icon span must be able to host an absolutely positioned child
		if (window.getComputedStyle(anchor).position === "static") {
			anchor.style.position = "relative";
		}
		anchor.style.display = anchor.style.display || "inline-block";

		/* The sidebar rows clip their contents, which cut the top half of the
		 * badge off. Clear overflow up the chain - the icon span, the anchor
		 * and the row - so the corner can sit proud of the icon. */
		var node = anchor;
		for (var up = 0; up < 3 && node; up++) {
			if (window.getComputedStyle(node).overflow !== "visible") {
				node.style.overflow = "visible";
			}
			node = node.parentElement;
		}

		badge.style.cssText = [
			"position:absolute",
			"top:-4px",
			"inset-inline-end:-6px",
			"background:#e24c4b",
			"color:#fff",
			"border-radius:9px",
			"font-size:9px",
			"line-height:1",
			"padding:2px 4px",
			"font-weight:700",
			"min-width:15px",
			"text-align:center",
			"pointer-events:none",
			"z-index:2",
			// a ring in the sidebar colour, so it reads against the icon
			"box-shadow:0 0 0 2px var(--surface-menu-bar, #fff)",
		].join(";");

		badge.textContent = count > 99 ? "99+" : String(count);
		return true;
	}

	function refresh() {
		if (!window.frappe || !frappe.session || frappe.session.user === "Guest") {
			return;
		}
		frappe.call({
			method: "frappe.client.get_count",
			args: {
				doctype: "Notification Log",
				filters: { for_user: frappe.session.user, read: 0 },
			},
			callback: function (r) {
				paint(parseInt(r.message, 10) || 0);
			},
			error: function () {
				/* never let a failed count break the desk */
			},
		});
	}

	function start() {
		if (started) return; // may be invoked from several triggers
		tries += 1;
		if (!bell()) {
			if (tries < MAX_TRIES) setTimeout(start, 500);
			return;
		}
		started = true;

		refresh();

		// Frappe already fires these - reuse them rather than polling.
		if (frappe.realtime && frappe.realtime.on) {
			frappe.realtime.on("notification", function () {
				setTimeout(refresh, 400);
			});
			frappe.realtime.on("indicator_hide", function () {
				setTimeout(refresh, 400);
			});
		}

		// Opening the panel marks things read; recount shortly after.
		$(document).on("click", ".sidebar-notification", function () {
			setTimeout(refresh, 1200);
			setTimeout(refresh, 3000);
		});

		// Safety net, in case a mark-as-read happens without an event.
		setInterval(refresh, 120000);
	}

	/* Frappe 16's new desk does NOT reliably fire "app_ready" - relying on it
	 * alone means the block loads and never runs. Kick off independently and
	 * also listen for the event in case it does fire. start() is guarded, so
	 * whichever arrives first wins and the rest are no-ops. */
	if (window.jQuery) {
		$(document).on("app_ready", function () {
			setTimeout(start, 300);
		});
	}
	if (document.readyState === "loading") {
		document.addEventListener("DOMContentLoaded", function () {
			setTimeout(start, 1000);
		});
	} else {
		setTimeout(start, 1000);
	}
})();
/* ==== MT NOTIFICATION BADGE - END ==== */
