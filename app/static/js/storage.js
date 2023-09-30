function cartStorageAddItem(product) {
  const cart = JSON.parse(localStorage.getItem("cart") || "[]");
  const productIndex = cart.findIndex((p) => p.sellerId === product.sellerId);
  if (productIndex == -1) {
    cart.push({ ...product, count: 1 });
  } else {
    cart[productIndex].count += 1;
  }
  localStorage.setItem("cart", JSON.stringify(cart));
}

function cartStorageClearProduct(product) {
  let cart = JSON.parse(localStorage.getItem("cart") || "[]");
  const productIndex = cart.findIndex((p) => p.sellerId === product.sellerId);
  if (productIndex == -1) {
    return;
  } else {
    cart = cart.filter((p) => product.sellerId !== p.sellerId);
  }
  localStorage.setItem("cart", JSON.stringify(cart));
}

function cartStorageMinusProduct(product) {
  let cart = JSON.parse(localStorage.getItem("cart") || "[]");
  const productIndex = cart.findIndex((p) => p.sellerId === product.sellerId);
  if (productIndex == -1) {
    return;
  } else {
    cart[productIndex].count -= 1;
    if (cart[productIndex].count <= 0) {
      cart = cart.filter((p) => product.sellerId !== p.sellerId);
    }
  }
  localStorage.setItem("cart", JSON.stringify(cart));
}
