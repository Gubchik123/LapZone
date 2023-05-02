const username_input = document.getElementById("id_username");
const password_input = document.getElementById("id_password");

function hide_username_and_password_inputs() {
	username_input.required = false;
	username_input.parentElement.style.display = "none";
	password_input.required = false;
	password_input.parentElement.style.display = "none";
}

hide_username_and_password_inputs();

document.getElementsByName("is_create_profile").forEach(function (radio) {
	radio.addEventListener("click", function () {
		if (this.value === "True") {
			username_input.required = true;
			username_input.parentElement.style.display = "block";
			password_input.required = true;
			password_input.parentElement.style.display = "block";
		} else hide_username_and_password_inputs();
	});
});
