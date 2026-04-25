const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const dropContent = document.getElementById("dropContent");
const preview = document.getElementById("preview");
const scanBtn = document.getElementById("scanBtn");
const results = document.getElementById("results");
const loader = document.getElementById("loader");
const errorBox = document.getElementById("errorBox");

let selectedFile = null;

dropZone.addEventListener("click", () => fileInput.click());

dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => dropZone.classList.remove("dragover"));

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("dragover");
  const file = e.dataTransfer.files[0];
  if (file && file.type.startsWith("image/")) loadFile(file);
});

fileInput.addEventListener("change", () => {
  if (fileInput.files[0]) loadFile(fileInput.files[0]);
});

function loadFile(file) {
  selectedFile = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    preview.src = e.target.result;
    preview.classList.remove("hidden");
    dropContent.classList.add("hidden");
  };
  reader.readAsDataURL(file);
  scanBtn.disabled = false;
  results.classList.add("hidden");
  errorBox.classList.add("hidden");
}

scanBtn.addEventListener("click", async () => {
  if (!selectedFile) return;

  loader.classList.remove("hidden");
  results.classList.add("hidden");
  errorBox.classList.add("hidden");
  scanBtn.disabled = true;

  const formData = new FormData();
  formData.append("image", selectedFile);

  try {
    const res = await fetch("/scan", { method: "POST", body: formData });
    const data = await res.json();

    if (data.error) {
      showError(data.error);
      return;
    }

    renderResults(data);
  } catch {
    showError("Something went wrong. Please try again.");
  } finally {
    loader.classList.add("hidden");
    scanBtn.disabled = false;
  }
});

function renderResults(data) {
  const ingredientsList = document.getElementById("ingredientsList");
  ingredientsList.innerHTML = "";
  (data.ingredients || []).forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    ingredientsList.appendChild(li);
  });

  renderMeal("breakfast", data.breakfast);
  renderMeal("lunch", data.lunch);
  renderMeal("dinner", data.dinner);

  results.classList.remove("hidden");
  results.scrollIntoView({ behavior: "smooth" });
}

function renderMeal(meal, info) {
  if (!info) return;
  document.getElementById(`${meal}Name`).textContent = info.name || "";

  const ingList = document.getElementById(`${meal}Ingredients`);
  ingList.innerHTML = "";
  (info.ingredients_used || []).forEach((i) => {
    const li = document.createElement("li");
    li.textContent = i;
    ingList.appendChild(li);
  });

  const stepsList = document.getElementById(`${meal}Steps`);
  stepsList.innerHTML = "";
  (info.steps || []).forEach((step) => {
    const li = document.createElement("li");
    li.textContent = step.replace(/^Step \d+:\s*/i, "");
    stepsList.appendChild(li);
  });
}

function showError(msg) {
  errorBox.textContent = msg;
  errorBox.classList.remove("hidden");
}
