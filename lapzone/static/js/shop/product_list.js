// Script to add .active class for dropdown-item
const url_params = new URLSearchParams(window.location.search);

const order_by = url_params.get("orderby");
const order_dir = url_params.get("orderdir");

if (order_by && order_dir) {
	for (let link of document.querySelectorAll(".dropdown-item")) {
		if (link.href.includes(order_by) && link.href.includes(order_dir)) {
			link.classList.add("active");
			break;
		}
	}
} else document.querySelector(".dropdown-item").classList.add("active");

// Script to check window size and resize pagination nav
const pagination = document.querySelector(".pagination");

function resize_pagination_nav() {
	window.outerWidth >= 992
		? pagination.classList.add("pagination-lg")
		: pagination.classList.remove("pagination-lg");

	window.outerWidth <= 768
		? pagination.classList.add("pagination-sm")
		: pagination.classList.remove("pagination-sm");
}

if (pagination) {
    resize_pagination_nav();
    window.addEventListener("resize", resize_pagination_nav);
}
