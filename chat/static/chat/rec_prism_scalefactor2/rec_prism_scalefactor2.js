const sf = document.getElementById("sfslider");
const ol = document.getElementById("olslider");
const ow = document.getElementById("owslider");
const oh = document.getElementById("ohslider");
const root = document.documentElement;
sf.addEventListener("input", do_when_sf_changed);
ol.addEventListener("input", do_when_ol_changed);
ow.addEventListener("input", do_when_ow_changed);
oh.addEventListener("input", do_when_oh_changed);

function do_when_sf_changed(e) {
	root.style.setProperty("--length", e.target.value*ol.value + "cm");
	root.style.setProperty("--width", e.target.value*ow.value + "cm");
	root.style.setProperty("--height", e.target.value*oh.value + "cm");
	root.style.setProperty("--scalefactor", e.target.value);
	document.getElementById('sftext').innerText = e.target.value;
	document.getElementById('ltext').innerText = e.target.value*ol.value;
	document.getElementById('wtext').innerText = e.target.value*ow.value;
	document.getElementById('htext').innerText = e.target.value*oh.value;
}

function do_when_ol_changed(e) {
	root.style.setProperty("--olength", e.target.value + "cm");
	root.style.setProperty("--length", e.target.value*sf.value + "cm");
	document.getElementById('oltext').innerText = e.target.value;
	document.getElementById('ltext').innerText = e.target.value*sf.value;
}

function do_when_ow_changed(e) {
	root.style.setProperty("--owidth", e.target.value + "cm");
	root.style.setProperty("--width", e.target.value*sf.value + "cm");
	document.getElementById('owtext').innerText = e.target.value;
	document.getElementById('wtext').innerText = e.target.value*sf.value;
}

function do_when_oh_changed(e) {
	root.style.setProperty("--oheight", e.target.value + "cm");
	root.style.setProperty("--height", e.target.value*sf.value + "cm");
	document.getElementById('ohtext').innerText = e.target.value;
	document.getElementById('htext').innerText = e.target.value*sf.value;
}

function do_when_new_img_data_recieved(new_img) {
	document.getElementById('olslider').value = new_img.ol;
	document.getElementById('owslider').value = new_img.ow;
	document.getElementById('ohslider').value = new_img.oh;
	document.getElementById('sfslider').value = new_img.sf;
    document.documentElement.style.setProperty("--olength", new_img.ol + "cm");
	document.documentElement.style.setProperty("--owidth", new_img.ow + "cm");
	document.documentElement.style.setProperty("--oheight", new_img.oh + "cm");
	document.documentElement.style.setProperty("--scalefactor", new_img.sf);
	document.documentElement.style.setProperty("--length", new_img.sf*new_img.ol + "cm");
	document.documentElement.style.setProperty("--width", new_img.sf*new_img.ow + "cm");
	document.documentElement.style.setProperty("--height", new_img.sf*new_img.oh + "cm");
	document.getElementById('oltext').innerText = new_img.ol;
	document.getElementById('owtext').innerText = new_img.ow;
	document.getElementById('ohtext').innerText = new_img.oh;
	document.getElementById('sftext').innerText = new_img.sf;
	document.getElementById('ltext').innerText = new_img.sf*new_img.ol;
	document.getElementById('wtext').innerText = new_img.sf*new_img.ow;
	document.getElementById('htext').innerText = new_img.sf*new_img.oh;
}