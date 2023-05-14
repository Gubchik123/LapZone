const screen_loader = document.getElementById("screen-loader");

function is_all_required_fields_are_filled_in_(form) {
	for (const input of form.querySelectorAll("input"))
		if (input.hasAttribute("required") && input.value.trim() === "")
			return false;
	return true;
}

document.querySelectorAll(".loading.btn").forEach(function(button) {
    button.addEventListener("click", function () {
        if (is_all_required_fields_are_filled_in_(button.closest("form"))) {
            screen_loader.style.display = "block";
            screen_loader.classList.remove("d-none");
            screen_loader.classList.add("d-flex");
        }
    });
});
