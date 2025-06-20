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

function onFileSelected(event) {
  const file = event.target.files[0];
  if (file) {
    const container = document.querySelector(".file-selected-container");

    const alert = document.createElement("label");
    alert.className = "alert alert-primary show w-100 mt-2 py-1";
    alert.setAttribute("role", "alert");
    alert.innerHTML = `
      Selected file ${file.name}
      <input type="button" value="x" onclick="cancelFileSelection()" class="btn btn-secondary p-0">
      <input type="submit" value="send" class="btn btn-primary px-1">
    `;
    container.appendChild(alert);
    const chooseButton = document.querySelector(".file-choose-container");
    chooseButton.classList.add("d-none");
  }
}

function cancelFileSelection() {
  const chooseButton = document.querySelector(".file-choose-container");
  chooseButton.classList.remove("d-none");

  const container = document.querySelector(".file-selected-container");
  container.innerHTML = "";
}
