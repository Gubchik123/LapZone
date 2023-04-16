document.querySelectorAll(".like").forEach((like_btn) => {
	like_btn.addEventListener("click", function () {
		fetch(like_btn.attributes["data-href"].nodeValue, {
			method: "POST",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
				"X-CSRFToken": csrf_token, // Template variable
			},
			body: JSON.stringify({
				user_id: user_id, // Template variable
			}),
		})
			.then((response) => response.text())
			.then((response_text) => {
				if (
					response_text ==
					"Product has successfully added to your wish list."
				) {
					let like_icon = like_btn.firstElementChild;

					if (like_icon.name == "heart-outline")
						like_icon.name = "heart";
					else like_icon.name = "heart-outline";
				}

				alert(response_text);
			})
			.catch((error) => {
				console.log(error);
				alert("There was an error! Try again later.");
			});
	});
});
