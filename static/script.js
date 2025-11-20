document.getElementById("recommendForm").onsubmit = async function (e) {
  e.preventDefault();
  const query = document.getElementById("query").value;
  document.getElementById("result").innerHTML = "<div class='text-secondary'>Loading...</div>";

  try {
    const res = await fetch(`/recommendations?query=${encodeURIComponent(query)}`);
    const data = await res.json();

    if (data.error) {
      document.getElementById("result").innerHTML = `<div class="alert alert-warning">${data.error}</div>`;
      return;
    }

    document.getElementById("welcome").style.display = "none";

    let html = `
      <div class="uv-product-card">
        <div class="uv-product-title">${data.product_name}</div>
        <div class="uv-product-meta">${data.brand} | ${data.color}</div>
        <p>${data.description || ""}</p>
        <h5 class="text-success">₹${data.product_price}</h5>
      </div>
      <div class="uv-combo-heading">Styling options for you</div>
    `;

    if (data.combos.length) {
      html += `<div id="comboCarousel" class="carousel slide" data-bs-ride="carousel">
        <div class="carousel-inner">`;

      data.combos.forEach((combo, index) => {
        html += `<div class="carousel-item ${index === 0 ? "active" : ""}">
          <div class="uv-combo-slide">`;

        combo.items.forEach(item => {
          html += `
            <div class="uv-combo-card">
              <h6>${item.product}</h6>
              <p><strong>Brand:</strong> ${item.brand}</p>
              <p><strong>Color:</strong> ${item.color}</p>
              <p><strong>Price:</strong> ₹${item.price}</p>
            </div>`;
        });

        html += `</div></div>`;
      });

      html += `</div>`;

      if (data.combos.length > 1) {
        html += `
          <button class="carousel-control-prev" type="button" data-bs-target="#comboCarousel" data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Previous</span>
          </button>
          <button class="carousel-control-next" type="button" data-bs-target="#comboCarousel" data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Next</span>
          </button>`;
      }

      html += `</div>`;
    }

    document.getElementById("result").innerHTML = html;

  } catch (err) {
    document.getElementById("result").innerHTML = `<div class="alert alert-danger">Something went wrong: ${err}</div>`;
  }
};