function replace_cart_btn_with_link_to_cart_detail_page(cart_btn) {
	const link = document.createElement("a");
	link.href = "/cart/";
	link.classList = "btn btn-success ms-2";
	link.innerHTML = "<ion-icon name='cart'></ion-icon>";

	cart_btn.parentNode.replaceChild(link, cart_btn);
}

function increase_cart_badge_count_of_products_in_cart(quantity) {
	const header_cart_badge = document.querySelector(
		"header ion-icon[name='cart']"
	).nextElementSibling;
	header_cart_badge.textContent = +header_cart_badge.textContent + quantity;
}

document.querySelectorAll(".cart").forEach((cart_btn) => {
	cart_btn.addEventListener("click", function () {
		let quantity = parseInt(
			prompt(
				"Please enter the product quantity you'd like to add to your cart:"
			)
		);
		if (isNaN(quantity) || quantity < 1) quantity = 1;

		fetch("/cart/add/", {
			method: "POST",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
				"X-CSRFToken": csrf_token, // Template variable
			},
			body: JSON.stringify({
				quantity: quantity,
				product_id: cart_btn.attributes["data-product_id"].nodeValue,
			}),
		})
			.then((response) => response.text())
			.then((response_text) => {
				if (
					response_text ==
					"Product has successfully added to your cart."
				) {
					replace_cart_btn_with_link_to_cart_detail_page(cart_btn);
					increase_cart_badge_count_of_products_in_cart(quantity);
				}

				alert(response_text);
			})
			.catch((error) => {
				console.log(error);
				alert("There was an error! Try again later.");
			});
	});
});
