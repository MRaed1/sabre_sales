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
