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
                )
                    cart_btn.firstElementChild.name = "cart";

                alert(response_text);
            })
            .catch((error) => {
                console.log(error);
                alert("There was an error! Try again later.");
            });
    });
});
