const API_URL = "http://127.0.0.1:5000/api";

let authToken = null;

const output = document.getElementById("output");
const authState = document.getElementById("auth-state");
const recipesList = document.getElementById("recipes-list");

function log(message, data = null) {
  const text = data ? `${message}\n${JSON.stringify(data, null, 2)}` : message;
  output.textContent = `${text}\n\n${output.textContent}`;
}

async function api(path, method = "GET", body = null, withAuth = false) {
  const headers = { "Content-Type": "application/json" };
  if (withAuth && authToken) {
    headers.Authorization = `Bearer ${authToken}`;
  }

  const response = await fetch(`${API_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.error || "API Fehler");
  }
  return data;
}

function renderRecipes(recipes) {
  recipesList.innerHTML = "";
  if (!recipes.length) {
    recipesList.innerHTML = "<li>Noch keine Rezepte vorhanden.</li>";
    return;
  }

  recipes.forEach((recipe) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <strong>${recipe.title}</strong><br />
      <small>von ${recipe.owner_username} | Kommentare: ${recipe.comment_count} | Favoriten: ${recipe.favorite_count}</small><br />
      <div><strong>Zutaten:</strong> ${recipe.ingredients}</div>
      <div><strong>Zubereitung:</strong> ${recipe.steps}</div>
    `;
    recipesList.appendChild(li);
  });
}

async function loadRecipes() {
  try {
    const data = await api("/recipes");
    renderRecipes(data.recipes || []);
  } catch (error) {
    log("Rezepte laden fehlgeschlagen", { error: error.message });
  }
}

document.getElementById("register-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = {
    username: document.getElementById("register-username").value.trim(),
    email: document.getElementById("register-email").value.trim(),
    password: document.getElementById("register-password").value,
  };

  try {
    const data = await api("/auth/register", "POST", payload);
    log("Registrierung erfolgreich", data);
  } catch (error) {
    log("Registrierung fehlgeschlagen", { error: error.message });
  }
});

document.getElementById("login-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = {
    email: document.getElementById("login-email").value.trim(),
    password: document.getElementById("login-password").value,
  };

  try {
    const data = await api("/auth/login", "POST", payload);
    authToken = data.token;
    authState.textContent = `Eingeloggt als ${data.user.username}`;
    log("Anmeldung erfolgreich", data.user);
  } catch (error) {
    log("Anmeldung fehlgeschlagen", { error: error.message });
  }
});

document.getElementById("recipe-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!authToken) {
    log("Bitte zuerst einloggen.");
    return;
  }

  const payload = {
    title: document.getElementById("recipe-title").value.trim(),
    ingredients: document.getElementById("recipe-ingredients").value.trim(),
    steps: document.getElementById("recipe-steps").value.trim(),
  };

  try {
    const data = await api("/recipes", "POST", payload, true);
    log("Rezept erstellt", data.recipe);
    await loadRecipes();
  } catch (error) {
    log("Rezept erstellen fehlgeschlagen", { error: error.message });
  }
});

document.getElementById("reload-btn").addEventListener("click", loadRecipes);

loadRecipes();
