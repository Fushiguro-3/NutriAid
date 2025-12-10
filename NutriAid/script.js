// ===============================
// 🌐 CONFIG
// ===============================
const API_BASE = "http://127.0.0.1:5000";

// ===============================
// 🌸 GLOBAL LOAD (HEADER + HOME)
// ===============================
document.addEventListener("DOMContentLoaded", () => {
  const user = JSON.parse(localStorage.getItem("nutriUser"));
  const path = window.location.pathname;

  // Protect pages except login/signup
  const publicPages = ["login.html", "signup.html", "/"];
  const isPublic = publicPages.some((p) => path.endsWith(p));
  if (!isPublic && !user) {
    window.location.href = "login.html";
    return;
  }

  // ---- Header name ----
  const profileName = document.getElementById("profileName");
  if (profileName && user) {
    profileName.textContent = user.name;
  }

  // ---- Header avatar dropdown ----
  const profileBtn = document.getElementById("profileBtn");
  const profileDropdown = document.getElementById("profileDropdown");

  // ✅ NEW: support both logoutDropdown and logoutBtn
  const logoutDropdown =
    document.getElementById("logoutDropdown") ||
    document.getElementById("logoutBtn");

  if (profileBtn && profileDropdown) {
    profileBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      profileDropdown.style.display =
        profileDropdown.style.display === "block" ? "none" : "block";
    });

    document.addEventListener("click", (e) => {
      if (
        !profileBtn.contains(e.target) &&
        !profileDropdown.contains(e.target)
      ) {
        profileDropdown.style.display = "none";
      }
    });
  }

  if (logoutDropdown) {
    logoutDropdown.onclick = () => {
      localStorage.removeItem("nutriUser");
      window.location.href = "login.html";
    };
  }

  // ---- Header Home / Chat buttons ----
  // ✅ NEW: support both old ids (headerHome/headerChat) and new (goHome/goChat)
  const headerHome =
    document.getElementById("headerHome") ||
    document.getElementById("goHome");
  const headerChat =
    document.getElementById("headerChat") ||
    document.getElementById("goChat");

  if (headerHome)
    headerHome.onclick = () => (window.location.href = "index.html");
  if (headerChat)
    headerChat.onclick = () => (window.location.href = "chat.html");

  // ---- Home-page central buttons ----
  const goChat = document.getElementById("goChat");
  const goDiet = document.getElementById("goDiet");

  if (goChat) goChat.onclick = () => (window.location.href = "chat.html");
  if (goDiet) goDiet.onclick = () => (window.location.href = "plan.html");

  // ---- Greet user on plan page ----
  const greetEl = document.getElementById("greetUser");
  if (greetEl && user) {
    greetEl.textContent = `Hello, ${user.name}!`;
  }
});

// ===============================
// 🥗 DIET PLAN PAGE (CALL BACKEND)
// ===============================
const dietForm = document.getElementById("dietForm");
const planResult = document.getElementById("planResult");

if (dietForm && planResult) {
  dietForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const name = document.getElementById("name").value.trim();
    const age = parseInt(document.getElementById("age").value, 10);
    const gender = document.getElementById("gender").value;
    const height = parseFloat(document.getElementById("height").value);
    const weight = parseFloat(document.getElementById("weight").value);
    const activity = document.getElementById("activity").value;
    const goal = document.getElementById("goal").value;

    const payload = { age, gender, height, weight, activity, goal };

    try {
      const res = await fetch(`${API_BASE}/recommend`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }

      const data = await res.json();
      console.log("Recommend response:", data);

      const { bmi, daily_calories, meal_plan } = data;

      // Helper to format each meal box
      function formatMeal(label, key) {
        if (!meal_plan || !meal_plan[key]) return "";
        const item = meal_plan[key];

        const foodName = item.food_name || "Meal";
        const calories = item.calories ?? "-";
        const carbs = item.carbs ?? "-";
        const protein = item.protein ?? "-";
        const fat = item.fat ?? "-";

        return `
          <li>
            <b>${label}:</b> ${foodName}
            <div class="macro-line">
              ${calories} kcal · Carbs: ${carbs} g · Protein: ${protein} g · Fat: ${fat} g
            </div>
          </li>
        `;
      }

      planResult.innerHTML = `
        <h3>Hello, ${name}! 🪴</h3>
        <p><b>BMI:</b> ${bmi}</p>
        <p><b>Daily Calories Target:</b> ${Math.round(daily_calories)} kcal</p>

        <h3>Recommended Meal Plan</h3>
        <ul class="meal-list">
          ${formatMeal("Breakfast", "breakfast")}
          ${formatMeal("Lunch", "lunch")}
          ${formatMeal("Snacks", "snacks")}
          ${formatMeal("Dinner", "dinner")}
        </ul>
      `;

      planResult.style.display = "block";
      planResult.classList.remove("show");
      setTimeout(() => planResult.classList.add("show"), 100);
      planResult.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (err) {
      console.error(err);
      planResult.innerHTML =
        `<p style="color:#c0392b;">⚠️ Could not connect to diet server. Please check if backend (Flask) is running on port 5000.</p>`;
      planResult.style.display = "block";
    }
  });
}

// ===============================
// 🤖 CHATBOT PAGE
// ===============================
const chatBox = document.getElementById("chat-box");
const chatInput = document.getElementById("user-input");
const chatSend = document.getElementById("sendChat");

function addChatBubble(message, sender) {
  if (!chatBox) return;
  const bubble = document.createElement("div");
  bubble.className = sender === "user" ? "user-message" : "bot-message";
  bubble.textContent = message;
  chatBox.appendChild(bubble);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendChat() {
  if (!chatInput) return;
  const msg = chatInput.value.trim();
  if (!msg) return;

  addChatBubble(msg, "user");
  chatInput.value = "";

  try {
    const res = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg }),
    });

    if (!res.ok) throw new Error(`Chat error: ${res.status}`);

    const data = await res.json();
    addChatBubble(data.reply || "Sorry, I couldn't reply.", "bot");
  } catch (err) {
    console.error(err);
    addChatBubble(
      "⚠️ Could not reach NutriAid assistant. Is the backend running?",
      "bot"
    );
  }
}

if (chatSend) chatSend.onclick = sendChat;
if (chatInput) {
  chatInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendChat();
  });
}
