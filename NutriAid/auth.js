// SIGNUP
const signupBtn = document.getElementById("signupBtn");
if (signupBtn) {
  signupBtn.onclick = async () => {
    const name = document.getElementById("signupName").value;
    const email = document.getElementById("signupEmail").value;
    const password = document.getElementById("signupPassword").value;

    const res = await fetch("http://127.0.0.1:5000/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password })
    });

    const data = await res.json();

    if (res.ok) {
      alert("Signup successful!");
      window.location.href = "login.html";
    } else {
      alert(data.error);
    }
  };
}

// LOGIN
const loginBtn = document.getElementById("loginBtn");
if (loginBtn) {
  loginBtn.onclick = async () => {
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    const res = await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (res.ok) {
      localStorage.setItem("nutriUser", JSON.stringify(data.user));
      window.location.href = "index.html"; // home page
    } else {
      alert(data.error);
    }
  };
}
