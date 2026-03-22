const API = "http://127.0.0.1:5000/api";

// ─── Authentification ────────────────────────────────────────────────────────

async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const res = await fetch(API + "/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const data = await res.json();

    if (!res.ok) {
        document.getElementById("status").innerText = "❌ " + (data.error || "Échec de connexion");
        return;
    }

    localStorage.setItem("token", data.access_token);
    document.getElementById("status").innerText = "✅ Connecté en tant que " + username;
}

// ─── Ajout d'article ─────────────────────────────────────────────────────────

async function addArticle() {
    const titre     = document.getElementById("titre").value;
    const auteur    = document.getElementById("auteur").value;
    const contenu   = document.getElementById("contenu").value;
    const categorie = document.getElementById("categorie").value || "General";
    const tags      = document.getElementById("tags").value || "";
    const token     = localStorage.getItem("token");

    if (!token) {
        document.getElementById("article-status").innerText = "❌ Vous devez être connecté.";
        return;
    }

    const res = await fetch(API + "/articles", {
        method: "POST",
        headers: {
            "Content-Type":  "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({ titre, auteur, contenu, categorie, tags })
    });

    const data = await res.json();

    if (!res.ok) {
        document.getElementById("article-status").innerText = "❌ Erreur : " + JSON.stringify(data);
        return;
    }

    document.getElementById("article-status").innerText = "✅ Article publié (ID: " + data.id + ")";
    loadArticles();
}

// ─── Chargement des articles ──────────────────────────────────────────────────

async function loadArticles() {
    const res  = await fetch(API + "/articles");
    const data = await res.json();

    const container = document.getElementById("articles");
    container.innerHTML = "";

    if (!data.data || data.data.length === 0) {
        container.innerHTML = "<p>Aucun article pour l'instant.</p>";
        return;
    }

    data.data.forEach(a => {
        container.innerHTML += `
            <div class="card">
                <h3>${a.titre}</h3>
                <p>${a.contenu}</p>
                <div class="meta">
                    <span>✍️ ${a.auteur}</span>
                    <span>📁 ${a.categorie || "—"}</span>
                    <span>🏷️ ${a.tags || "—"}</span>
                    <span>📅 ${new Date(a.created_at).toLocaleDateString("fr-FR")}</span>
                </div>
                <button class="delete-btn" onclick="deleteArticle(${a.id})">🗑️ Supprimer</button>
            </div>
        `;
    });
}

// ─── Suppression d'article ────────────────────────────────────────────────────

async function deleteArticle(id) {
    const token = localStorage.getItem("token");

    if (!token) {
        alert("Vous devez être connecté pour supprimer un article.");
        return;
    }

    if (!confirm("Supprimer cet article ?")) return;

    const res = await fetch(API + "/articles/" + id, {
        method: "DELETE",
        headers: { "Authorization": "Bearer " + token }
    });

    if (res.ok) {
        loadArticles();
    } else {
        alert("Erreur lors de la suppression.");
    }
}

// ─── Recherche d'articles ─────────────────────────────────────────────────────

async function searchArticles() {
    const query = document.getElementById("search-query").value;

    if (!query) return;

    const res  = await fetch(API + "/articles/search?query=" + encodeURIComponent(query));
    const data = await res.json();

    const container = document.getElementById("articles");
    container.innerHTML = `<p><strong>${data.message}</strong></p>`;

    if (data.data && data.data.length > 0) {
        data.data.forEach(a => {
            container.innerHTML += `
                <div class="card">
                    <h3>${a.titre}</h3>
                    <p>${a.contenu}</p>
                    <div class="meta">
                        <span>✍️ ${a.auteur}</span>
                        <span>📁 ${a.categorie || "—"}</span>
                    </div>
                </div>
            `;
        });
    }
}

// ─── Chargement initial ───────────────────────────────────────────────────────
loadArticles();
