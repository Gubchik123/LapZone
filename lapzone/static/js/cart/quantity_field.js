const initial_quantity_fields_values = {};
const header_cart_badge = document.querySelector(
	"header ion-icon[name='cart']"
).nextElementSibling;
// Get unit prices of products in user's cart
const unit_prices = {};
document
	.querySelectorAll(".unit_price")
	.forEach(
		(element) => (unit_prices[element.id] = parseFloat(element.textContent))
	);

function blur_quantity_field_if_it_is_enter_key(event) {
	const quantity_field = event.target;

	if (event.key === "Enter") {
		event.preventDefault();
		quantity_field.blur();
	}
}

function update_cart_product(event) {
	const quantity_field = event.target;
	const quantity_field_value = +quantity_field.value;
	const initial_quantity_field_value =
		initial_quantity_fields_values[quantity_field.id];

    console.log(quantity_field_value);

	if (quantity_field_value == initial_quantity_field_value) 
        return;
	if (isNaN(quantity_field_value) || quantity_field_value < 1) {
		quantity_field.value = initial_quantity_field_value;
		alert("Minimum quantity is 1!");
		return;
	}
	if (quantity_field_value > 10) {
		quantity_field.value = initial_quantity_field_value;
		alert("Maximum quantity is 10!");
		return;
	}
	// If quantity field value is valid
	send_post_request_to_update_cart_product(
		quantity_field_value,
		+quantity_field.attributes["data-product_id"].nodeValue
	);
	update_header_cart_badge_count(
		initial_quantity_field_value,
		quantity_field_value
	);

	const id_parts = quantity_field.id.split("_");
	const forloop_counter = parseInt(id_parts[id_parts.length - 1]);

	update_total_price_of_product(
		quantity_field_value,
		initial_quantity_field_value,
		forloop_counter
	);

	initial_quantity_fields_values[quantity_field.id] = quantity_field_value;
}

function send_post_request_to_update_cart_product(quantity, product_id) {
	fetch("/cart/update/", {
		method: "POST",
		headers: {
			Accept: "application/json",
			"Content-Type": "application/json",
			"X-CSRFToken": csrf_token, // Template variable
		},
		body: JSON.stringify({
			quantity: quantity,
			product_id: product_id,
		}),
	})
		.then((response) => response.text())
		.then((response_text) => alert(response_text))
		.catch((error) => {
			console.log(error);
			alert("There was an error! Try again later.");
		});
}

function update_header_cart_badge_count(
	initial_quantity_field_value,
	current_quantity_field_value
) {
	header_cart_badge.textContent =
		+header_cart_badge.textContent -
		initial_quantity_field_value +
		current_quantity_field_value;
}

function update_total_price_of_product(
	quantity_field_value,
	initial_quantity_field_value,
	forloop_counter
) {
	const product_total_price = document.querySelector(
		`#total_price_${forloop_counter}`
	);
	const product_total_price_value = parseFloat(
		product_total_price.textContent
	);
	const product_unit_price = unit_prices[`unit_price_${forloop_counter}`];
	const initial_product_unit_price =
		product_unit_price * initial_quantity_field_value;
	const current_product_unit_price =
		product_unit_price * quantity_field_value;

	product_total_price.textContent =
		product_total_price_value -
		initial_product_unit_price +
		current_product_unit_price;
    product_total_price.textContent += ".0$";

	update_total_price(initial_product_unit_price, current_product_unit_price);
}

function update_total_price(
	initial_product_unit_price,
	current_product_unit_price
) {
	const total_price = document.querySelector("#total_price");
	const total_price_value = parseFloat(total_price.textContent);

	total_price.textContent =
		total_price_value -
		initial_product_unit_price +
		current_product_unit_price;
    total_price.textContent += ".0$";
}

document
	.querySelectorAll("input[name='quantity']")
	.forEach((quantity_field) => {
		initial_quantity_fields_values[quantity_field.id] =
            +quantity_field.value;

		quantity_field.addEventListener(
			"keydown",
			blur_quantity_field_if_it_is_enter_key
		);
		quantity_field.addEventListener("blur", update_cart_product);
	});
