const screen_loader = document.getElementById("screen-loader");
const checkout_form = document.getElementById("checkout-form");
const checkout_submit_btn = document.getElementById("checkout-submit-btn");

function is_all_required_fields_are_filled() {
	for (const input of checkout_form.querySelectorAll("input"))
		if (input.hasAttribute("required") && input.value.trim() === "")
			return false;
	return true;
}

checkout_submit_btn.addEventListener("click", function (event) {
	if (is_all_required_fields_are_filled()) {
		screen_loader.style.display = "block";
		screen_loader.classList.remove("d-none");
		screen_loader.classList.add("d-flex");
	}
});
