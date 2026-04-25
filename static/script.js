const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const dropContent = document.getElementById("dropContent");
const thumbnails = document.getElementById("thumbnails");
const scanBtn = document.getElementById("scanBtn");
const results = document.getElementById("results");
const loader = document.getElementById("loader");
const loaderText = document.getElementById("loaderText");
const errorBox = document.getElementById("errorBox");

const MAX_FILES = 5;
let selectedFiles = [];
let selectedMeal = "breakfast";

dropZone.addEventListener("click", () => fileInput.click());

dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => dropZone.classList.remove("dragover"));

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("dragover");
  addFiles(e.dataTransfer.files);
});

fileInput.addEventListener("change", () => {
  addFiles(fileInput.files);
  fileInput.value = "";
});

document.querySelectorAll(".meal-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".meal-btn").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    selectedMeal = btn.dataset.meal;
  });
});

function addFiles(files) {
  for (const file of files) {
    if (!file.type.startsWith("image/")) continue;
    if (selectedFiles.length >= MAX_FILES) break;
    selectedFiles.push(file);
    addThumbnail(file, selectedFiles.length - 1);
  }
  updateDropZone();
  updateScanBtn();
}

function addThumbnail(file, index) {
  const wrapper = document.createElement("div");
  wrapper.className = "thumb-wrapper";
  wrapper.dataset.index = index;

  const img = document.createElement("img");
  const reader = new FileReader();
  reader.onload = (e) => (img.src = e.target.result);
  reader.readAsDataURL(file);

  const btn = document.createElement("button");
  btn.className = "thumb-remove";
  btn.textContent = "×";
  btn.addEventListener("click", () => removeFile(index));

  wrapper.appendChild(img);
  wrapper.appendChild(btn);
  thumbnails.appendChild(wrapper);
}

function removeFile(index) {
  selectedFiles.splice(index, 1);
  thumbnails.innerHTML = "";
  selectedFiles.forEach((f, i) => addThumbnail(f, i));
  updateDropZone();
  updateScanBtn();
}

function updateDropZone() {
  if (selectedFiles.length >= MAX_FILES) {
    dropContent.querySelector("p").textContent = "Maximum 5 photos reached";
    dropContent.querySelector("span").textContent = "Remove a photo to add another";
  } else {
    dropContent.querySelector("p").textContent = "Click or drag fridge photos here";
    dropContent.querySelector("span").textContent = `Up to ${MAX_FILES} photos · JPG, PNG, WEBP (${selectedFiles.length}/${MAX_FILES} added)`;
  }
}

function updateScanBtn() {
  scanBtn.disabled = selectedFiles.length === 0;
}

scanBtn.addEventListener("click", async () => {
  if (selectedFiles.length === 0) return;

  loader.classList.remove("hidden");
  loaderText.textContent = "Scanning your fridge...";
  results.classList.add("hidden");
  errorBox.classList.add("hidden");
  scanBtn.disabled = true;

  const formData = new FormData();
  selectedFiles.forEach((f) => formData.append("image", f));
  formData.append("meal", selectedMeal);

  try {
    loaderText.textContent = "Finding ingredients...";
    const res = await fetch("/scan", { method: "POST", body: formData });
    loaderText.textContent = "Generating recipe...";
    const data = await res.json();

    if (data.error) {
      showError(data.error);
      return;
    }

    renderResults(data);
  } catch (err) {
    showError("Something went wrong: " + err.message);
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

  const recipe = data.recipe;
  const label = document.getElementById("mealLabel");
  label.textContent = selectedMeal.charAt(0).toUpperCase() + selectedMeal.slice(1);
  label.className = `meal-label ${selectedMeal}`;

  document.getElementById("recipeName").textContent = recipe.name || "";

  const ingList = document.getElementById("recipeIngredients");
  ingList.innerHTML = "";
  (recipe.ingredients_used || []).forEach((i) => {
    const li = document.createElement("li");
    li.textContent = i;
    ingList.appendChild(li);
  });

  const stepsList = document.getElementById("recipeSteps");
  stepsList.innerHTML = "";
  (recipe.steps || []).forEach((step) => {
    const li = document.createElement("li");
    li.textContent = step.replace(/^Step \d+:\s*/i, "");
    stepsList.appendChild(li);
  });

  results.classList.remove("hidden");
  results.scrollIntoView({ behavior: "smooth" });
}

function showError(msg) {
  errorBox.textContent = msg;
  errorBox.classList.remove("hidden");
}
