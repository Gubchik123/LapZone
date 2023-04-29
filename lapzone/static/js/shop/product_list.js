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

// Script to check window size and hide filtering Bootstrap5 collapse
const collapseOne = new bootstrap.Collapse(
	document.getElementById("panelsStayOpen-collapseOne"),
	{ toggle: false }
);

function collapseCheck() {
	if (window.innerWidth < 992) collapseOne.hide();
	else collapseOne.show();
}

window.addEventListener("resize", collapseCheck);
collapseCheck();
