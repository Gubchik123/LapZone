const theme_toggler_btn = document.getElementById("theme_toggler_btn");

theme_toggler_btn.addEventListener("change", () => {
	if (document.documentElement.hasAttribute("theme")) {
		sessionStorage.setItem("dark-theme", "no");
		document.documentElement.removeAttribute("theme");
	} else set_dark_mode();
});

function set_dark_mode() {
	sessionStorage.setItem("dark-theme", "yes");
	document.documentElement.setAttribute("theme", "dark");
}

if (sessionStorage.getItem("dark-theme") == "yes") {
	set_dark_mode();
	theme_toggler_btn.checked = !theme_toggler_btn.checked;
}
