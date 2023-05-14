const screen_loader = document.getElementById("screen-loader");
const form = document.querySelector("form.loading");

function is_all_required_fields_are_filled() {
	for (const input of form.querySelectorAll("input"))
		if (input.hasAttribute("required") && input.value.trim() === "")
			return false;
	return true;
}

document.querySelector(".loading.btn").addEventListener("click", function (event) {
	if (is_all_required_fields_are_filled()) {
		screen_loader.style.display = "block";
		screen_loader.classList.remove("d-none");
		screen_loader.classList.add("d-flex");
	}
});
