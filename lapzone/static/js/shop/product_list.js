const url_params=new URLSearchParams(window.location.search),order_by=url_params.get("orderby"),order_dir=url_params.get("orderdir");if(order_by&&order_dir){for(let link of document.querySelectorAll(".dropdown-item"))if(link.href.includes(order_by)&&link.href.includes(order_dir)){link.classList.add("active");break}}else document.querySelector(".dropdown-item").classList.add("active");const collapseOne=new bootstrap.Collapse(document.getElementById("panelsStayOpen-collapseOne"),{toggle:!1});function collapseCheck(){window.innerWidth<992?collapseOne.hide():collapseOne.show()}window.addEventListener("resize",collapseCheck),collapseCheck();