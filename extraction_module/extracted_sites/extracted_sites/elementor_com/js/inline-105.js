
	jQuery(document).ready(function($) {
		$(document).on("click", ".chat-button-open",function() {
			window.dispatchEvent(new Event('loadChat'));
		});
});
