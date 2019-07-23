overrideGet = function() {
	if (typeof $ !== 'undefined' && typeof $.get !== 'undefined') {
		var originalGet = $.get;
		$.get = function(text, callback, a, b) {
			if (text == 'core/js/app/categories.json') {
				callback(categoriesJson);
			} else {
				return originalGet(text, callback, a, b);
			}
		}
	} else {
		window.setTimeout(overrideGet, 50); // The main.page function, and therefore jQuery, only gets called after 250 milliseconds, so to override successfully, this needs to run later.
	}
};
window.onload = function() {
	overrideGet();
}