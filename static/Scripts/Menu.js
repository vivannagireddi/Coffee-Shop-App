// Logic for selecting quantity.

document.querySelectorAll(".card").forEach((card) => {
  const price = parseFloat(card.dataset.price || "0");
  const itemName = card.dataset.itemName;
  const qtyInput = card.querySelector(".qty-input");
  const userState = card.dataset.sessionStatus;
  // prefer a class on the select; fallback to any select inside the card
  const pushDataToFlask = () => {
    if (userState === "true") {
      const qtyVal = Math.max(0, parseInt(qtyInput.value || "0", 10));
      if (qtyVal === 0) {
        // nothing to send
        return;
      } else {
        const payload = {
          qty: qtyVal,
          itemName: itemName,
          price: price,
        };
        fetch("/add-to-cart", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        })
          .then((response) => response.json())
          .then((data) => console.log(data))
          .catch((error) => console.error("Error:", error));
        
          
        cartbutton = card.querySelector(".addtocart");
        cartbutton.textContent = "Added!";
        cartbutton.disabled = true;
        card.querySelector(".qty-decrease").disabled = true;
        card.querySelector(".qty-increase").disabled = true;
        console.log(userState);
      }
    } else {
      location.replace("/login");
    }
  };
  card.querySelector(".qty-decrease").addEventListener("click", () => {
    qtyInput.value = Math.max(0, parseInt(qtyInput.value || "1", 10) - 1);
  });
  card.querySelector(".qty-increase").addEventListener("click", () => {
    qtyInput.value = Math.max(0, parseInt(qtyInput.value || "1", 10) + 1);
  });
  card.querySelector(".addtocart").addEventListener("click", () => {
    pushDataToFlask();
  });
});
