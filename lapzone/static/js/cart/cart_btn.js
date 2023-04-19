function replace_cart_btn_with_link_to_cart_detail_page(cart_btn) {
	const link = document.createElement("a");
	link.href = "/cart/";
	link.classList = "btn btn-success ms-2";
	link.innerHTML = "<ion-icon name='cart'></ion-icon>";

    cart_btn.parentNode.replaceChild(link, cart_btn);
}

function increase_cart_badge_count_of_products_in_cart() {
	const header_cart_badge = document.querySelector(
		"header ion-icon[name='cart']"
	).nextElementSibling;
	header_cart_badge.textContent = +header_cart_badge.textContent + 1;
}

document.querySelectorAll(".cart").forEach((cart_btn) => {
	cart_btn.addEventListener("click", function () {
		fetch("/cart/add/", {
			method: "POST",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
				"X-CSRFToken": csrf_token, // Template variable
			},
			body: JSON.stringify({
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
					increase_cart_badge_count_of_products_in_cart();
				}

				alert(response_text);
			})
			.catch((error) => {
				console.log(error);
				alert("There was an error! Try again later.");
			});
	});
});
