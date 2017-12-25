
var div = $("<div dir=\"rtl\" style=\"color: red; font-size: 24px\">נא לבחור הרצאות. מ:</div>");
var select1 = $("<select id=\"{}\"></select>");
fill(select1);
div.append(select1);
div.append(" עד ");
var select2 = $("<select id=\"{}\"></select>");
fill(select2);
div.append(select2);
div.append("<a href=\"{}\"><button id=\"{}\">~ OK ~</button></a>");

div.append("<br />");
div.append("<hr />");
div.append("<br />");

div.insertBefore("center > table");
