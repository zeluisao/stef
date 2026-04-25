const dropZone     = document.getElementById("dropZone");
const fileInput    = document.getElementById("fileInput");
const dropContent  = document.getElementById("dropContent");
const thumbnails   = document.getElementById("thumbnails");
const scanBtn      = document.getElementById("scanBtn");
const results      = document.getElementById("results");
const loader       = document.getElementById("loader");
const loaderText   = document.getElementById("loaderText");
const errorBox     = document.getElementById("errorBox");
const chatMessages = document.getElementById("chatMessages");
const chatInput    = document.getElementById("chatInput");
const chatSend     = document.getElementById("chatSend");

const MAX_FILES = 5;
let selectedFiles = [];
let selectedMeal  = "breakfast";
let currentIngredients = [];
let chatHistory = [];

// ── File upload ──────────────────────────────────────────────────────────────

dropZone.addEventListener("click", () => fileInput.click());
dropZone.addEventListener("dragover", (e) => { e.preventDefault(); dropZone.classList.add("dragover"); });
dropZone.addEventListener("dragleave", () => dropZone.classList.remove("dragover"));
dropZone.addEventListener("drop", (e) => { e.preventDefault(); dropZone.classList.remove("dragover"); addFiles(e.dataTransfer.files); });
fileInput.addEventListener("change", () => { addFiles(fileInput.files); fileInput.value = ""; });

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

// ── Meal selector ─────────────────────────────────────────────────────────────

document.querySelectorAll(".meal-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    if (btn.classList.contains("active")) return;
    document.querySelectorAll(".meal-btn").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    selectedMeal = btn.dataset.meal;
    if (currentIngredients.length > 0) fetchRecipe();
  });
});

// ── Scan ──────────────────────────────────────────────────────────────────────

scanBtn.addEventListener("click", async () => {
  if (selectedFiles.length === 0) return;

  loader.classList.remove("hidden");
  loaderText.textContent = "Scanning your fridge...";
  results.classList.add("hidden");
  errorBox.classList.add("hidden");
  scanBtn.disabled = true;
  chatHistory = [];
  chatMessages.innerHTML = "";

  const formData = new FormData();
  selectedFiles.forEach((f) => formData.append("image", f));
  formData.append("meal", selectedMeal);

  try {
    const res  = await fetch("/scan", { method: "POST", body: formData });
    const data = await res.json();
    if (data.error) { showError(data.error); return; }
    currentIngredients = data.ingredients || [];
    renderResults(data);
  } catch (err) {
    showError("Something went wrong: " + err.message);
  } finally {
    loader.classList.add("hidden");
    scanBtn.disabled = selectedFiles.length === 0;
  }
});

async function fetchRecipe() {
  loader.classList.remove("hidden");
  loaderText.textContent = "Getting " + selectedMeal + " recipe...";
  errorBox.classList.add("hidden");
  chatHistory = [];
  chatMessages.innerHTML = "";

  try {
    const res  = await fetch("/recipe", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ingredients: currentIngredients, meal: selectedMeal })
    });
    const data = await res.json();
    if (data.error) { showError(data.error); return; }
    renderRecipeCard(data.recipe);
    document.getElementById("recipeCard").scrollIntoView({ behavior: "smooth" });
  } catch (err) {
    showError("Something went wrong: " + err.message);
  } finally {
    loader.classList.add("hidden");
  }
}

function renderResults(data) {
  const list = document.getElementById("ingredientsList");
  list.innerHTML = "";
  currentIngredients.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    list.appendChild(li);
  });

  renderRecipeCard(data.recipe);
  results.classList.remove("hidden");
  results.scrollIntoView({ behavior: "smooth" });
}

function renderRecipeCard(recipe) {
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
}

// ── Chat ──────────────────────────────────────────────────────────────────────

chatSend.addEventListener("click", sendChat);
chatInput.addEventListener("keydown", (e) => { if (e.key === "Enter") sendChat(); });

async function sendChat() {
  const msg = chatInput.value.trim();
  if (!msg) return;

  chatInput.value = "";
  appendMessage("user", msg);
  chatHistory.push({ role: "user", content: msg });

  chatSend.disabled = true;
  appendMessage("assistant", "...", "thinking");

  try {
    const res  = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg, ingredients: currentIngredients, meal: selectedMeal, history: chatHistory })
    });
    const data = await res.json();

    removeThinking();

    if (data.error) { appendMessage("assistant", "Sorry, something went wrong: " + data.error); return; }

    appendMessage("assistant", data.reply);
    chatHistory.push({ role: "assistant", content: data.reply });

    if (data.recipe) renderRecipeCard(data.recipe);
  } catch (err) {
    removeThinking();
    appendMessage("assistant", "Sorry, something went wrong.");
  } finally {
    chatSend.disabled = false;
    chatInput.focus();
  }
}

function appendMessage(role, text, id) {
  const div = document.createElement("div");
  div.className = `chat-msg ${role}`;
  div.textContent = text;
  if (id) div.id = id;
  chatMessages.appendChild(div);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeThinking() {
  const el = document.getElementById("thinking");
  if (el) el.remove();
}

// ── Error ─────────────────────────────────────────────────────────────────────

function showError(msg) {
  errorBox.textContent = msg;
  errorBox.classList.remove("hidden");
}
