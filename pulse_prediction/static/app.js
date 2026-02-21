const form = document.getElementById("risk-form");
const resultSection = document.getElementById("result");
const errorBlock = document.getElementById("error");
const clearButton = document.getElementById("clear-btn");

function readInt(id) {
  const raw = document.getElementById(id).value.trim();
  if (!/^\d+$/.test(raw)) {
    return null;
  }
  return Number(raw);
}

function showError(message) {
  errorBlock.textContent = message;
  errorBlock.classList.remove("hidden");
}

clearButton.addEventListener("click", () => {
  form.reset();
  errorBlock.classList.add("hidden");
  resultSection.classList.add("hidden");
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  errorBlock.classList.add("hidden");
  resultSection.classList.add("hidden");

  const payload = {
    heart_rate: readInt("heart_rate"),
    systolic_bp: readInt("systolic_bp"),
    diastolic_bp: readInt("diastolic_bp"),
  };

  if (Object.values(payload).some((value) => value === null)) {
    showError("Please enter whole numbers only (e.g. 72, 120, 80).");
    return;
  }

  let response;
  let body;

  try {
    response = await fetch("/api/assess", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    body = await response.json();
  } catch (_error) {
    showError("Could not reach server. Please try again.");
    return;
  }

  if (!response.ok) {
    showError(body.error || "Failed to assess risk.");
    return;
  }

  document.getElementById("risk_level").textContent = body.risk_level;
  document.getElementById("risk_score").textContent = body.risk_score;

  const reasonsList = document.getElementById("reasons");
  reasonsList.innerHTML = "";
  body.reasons.forEach((reason) => {
    const li = document.createElement("li");
    li.textContent = reason;
    reasonsList.appendChild(li);
  });

  resultSection.classList.remove("hidden");
});
