function copyToClipboard() {
  const input = document.getElementById("uploadLink");
  navigator.clipboard.writeText(input.value).then(() => {
    showCopiedAlert();
  });
}

function showCopiedAlert() {
  const container = document.querySelector(".alert-container");

  const alert = document.createElement("div");
  alert.className =
    "alert alert-success alert-dismissible fade show w-100 mt-2 py-1";
  alert.setAttribute("role", "alert");
  alert.innerHTML = `
    Link Copied!
    <button type="button" class="btn-close py-2" data-bs-dismiss="alert" aria-label="Close"></button>
  `;

  container.appendChild(alert);

  setTimeout(() => {
    alert.classList.remove("show");
    alert.classList.add("hide");
    setTimeout(() => alert.remove(), 300);
  }, 5000);
}
