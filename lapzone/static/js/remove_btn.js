document.querySelectorAll(".remove.btn").forEach((remove_btn) => {
	remove_btn.addEventListener("click", function (event) {
		if (
			!confirm("Do you really want to delete this item?")
		) event.preventDefault();
	});
});