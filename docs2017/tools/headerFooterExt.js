var FILENAME_HEADER = "header";
var FILENAME_FOOTER = "footer";

var fs = require("fs");
var path = require("path");

var headerText, footerText;

var html = {};
html.onComplete = function(html, data) {
	if (!headerText && !footerText) {
		return;
	}

	var result = "";
	if (headerText) {
		result += data.replaceVariables(headerText, [data.frontMatterMap, data.variablesMap, {document: {title: data.title}}]);
	}
	result += html;
	if (footerText) {
		result += data.replaceVariables(footerText, [data.frontMatterMap, data.variablesMap, {document: {title: data.title}}]);
	}

	return result;
}

var init = function(data) {
	if (FILENAME_HEADER) {
		var headerPath = path.join(__dirname, FILENAME_HEADER);
		try {
			var fd = fs.openSync(headerPath, "r");
		} catch (e) {
			data.logger.error("Failed to open header file: " + headerPath + "\n" + e.toString());
		}
		if (fd) {
			headerText = data.readFile(fd);
			fs.closeSync(fd);
		}
	}

	if (FILENAME_FOOTER) {
		var footerPath = path.join(__dirname, FILENAME_FOOTER);
		try {
			var fd = fs.openSync(footerPath, "r");
		} catch (e) {
			data.logger.error("Failed to open footer file: " + footerPath + "\n" + e.toString());
		}
		if (fd) {
			footerText = data.readFile(fd);
			fs.closeSync(fd);
		}
	}
}

module.exports.html = html;
module.exports.init = init;
module.exports.id = "header/footer";
