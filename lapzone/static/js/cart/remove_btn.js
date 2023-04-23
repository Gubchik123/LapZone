document.querySelectorAll(".remove.btn").forEach((remove_btn) => {
	remove_btn.addEventListener("click", function () {
		if (
			confirm("Do you really want to delete this product from your cart?")
		) {
			fetch("/cart/remove/", {
				method: "POST",
				headers: {
					Accept: "application/json",
					"Content-Type": "application/json",
					"X-CSRFToken": csrf_token, // Template variable
				},
				body: JSON.stringify({
					product_id:
						+remove_btn.attributes["data-product_id"].nodeValue,
				}),
			})
				.then((response) => window.location.reload())
				.catch((error) => {
					console.log(error);
					alert("There was an error! Try again later.");
				});
		}
	});
});
