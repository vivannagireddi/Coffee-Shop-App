// Logic for selecting quantity.

document.querySelectorAll(".card").forEach((card) => {
  const price = parseFloat(card.dataset.price || "0");

  // get the dropdown element (first one if multiple)
  const cupsizeElement =
    card.querySelector(".myDropdown") || card.querySelector("select");
  const itemName = card.querySelector(".card-title").innerText;
  const addToCartButton = card.querySelector(".addtocart");
  const LoginStatus = card.querySelector(".addtocart").dataset.sessionStatus;
  const username = card.querySelector(".addtocart").dataset.username;

  // When "Add to Cart" button is clicked
  addToCartButton.addEventListener("click", () => {
    console.log(`Login Status: ${LoginStatus}`);
    console.log(`Login Status: ${LoginStatus}`);
    console.log(`Login Status: ${LoginStatus}`);
    if (String(LoginStatus) === 'True') {
      const selectedOption = cupsizeElement.value; // read inside the listener
      const quantity = 1; // Default quantity is 1
      if (selectedOption === "") {
        alert("Please select a size before adding to cart.");
        return;
      }

      const itemPrice = price;
      console.log(
        `Added to cart: Username: ${username}, Item ${itemName}, Size ${selectedOption}, Quantity: ${quantity}, Price: ₹${itemPrice}`
      );

      addToCartButton.style.display = "none";

      // Send Data to Flask Server
      fetch("/add-to-cart", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          itemName,
          quantity,
          size: selectedOption,
          price: itemPrice,
        }),
      })
        .then((response) => response.json())
        .then((data) => console.log("Server response:", data))
        .catch((error) => console.error("Error:", error));

      // Create Remove button
      const deleteItem = document.createElement("button");
      deleteItem.innerText = "Remove";
      deleteItem.classList.add("remove-item");
      deleteItem.style.backgroundColor = "#ff4d4d";
      deleteItem.style.color = "white";
      deleteItem.style.border = "none";
      deleteItem.style.padding = "5px 10px";
      deleteItem.style.cursor = "pointer";
      deleteItem.style.marginLeft = "10px";
      const icon = document.createElement("i");
      icon.classList.add("fa-solid", "fa-trash");
      icon.style.color = "white";
      icon.style.marginRight = "5px";
      deleteItem.prepend(icon);
      addToCartButton.parentNode.appendChild(deleteItem);

      deleteItem.addEventListener("click", () => {
        addToCartButton.style.display = "flex";
        console.log(
          `Removed from cart: Item ${itemName}, Size ${selectedOption}, Quantity: ${quantity}`
        );
        fetch("/remove-from-cart", {
          method: "GET/POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            itemName,
            quantity,
            size: selectedOption,
            price: itemPrice,
          }),
        })
        .then((response) => response.json())
        .then((data) => console.log("Server response:", data))
        .catch((error) => console.error("Error:", error))
        deleteItem.remove();
      });
    } else {
      window.location.replace("/login");
    }
  });
});
