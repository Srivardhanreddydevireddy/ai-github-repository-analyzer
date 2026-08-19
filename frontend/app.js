const API_BASE = "";

const $ = (id) => document.getElementById(id);

$("analyzeBtn").addEventListener("click", analyzeRepository);

async function analyzeRepository() {
  const repository_url = $("repoUrl").value.trim();
  if (!repository_url) {
    setStatus("Enter a GitHub repository URL.", true);
    return;
  }

  $("analyzeBtn").disabled = true;
  setStatus("Collecting repository data and running analysis...");
  $("results").classList.add("hidden");

  try {
    const response = await fetch(`${API_BASE}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ repository_url })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Analysis failed.");
    render(data);
    setStatus("Analysis completed.");
  } catch (error) {
    setStatus(error.message, true);
  } finally {
    $("analyzeBtn").disabled = false;
  }
}

function setStatus(message, error = false) {
  $("status").textContent = message;
  $("status").className = error ? "status error" : "status";
}

function render(data) {
  $("results").classList.remove("hidden");
  $("overall").textContent = data.scores.overall;
  $("codeScore").textContent = data.scores.code_quality;
  $("docScore").textContent = data.scores.documentation;
  $("maintScore").textContent = data.scores.maintainability;

  const repo = data.repository;
  $("repoInfo").innerHTML = [
    ["Name", repo.full_name],
    ["Description", repo.description || "No description"],
    ["Stars", repo.stars],
    ["Forks", repo.forks],
    ["Open issues", repo.open_issues],
    ["Default branch", repo.default_branch]
  ].map(([k, v]) => `<div class="item"><b>${escapeHtml(k)}:</b> ${escapeHtml(String(v))}</div>`).join("");

  const total = Object.values(data.languages).reduce((a, b) => a + b, 0) || 1;
  $("languages").innerHTML = Object.entries(data.languages)
    .sort((a, b) => b[1] - a[1])
    .map(([name, bytes]) => `<div class="item"><b>${escapeHtml(name)}</b> — ${((bytes / total) * 100).toFixed(1)}%</div>`)
    .join("") || "No language data returned.";

  $("findings").innerHTML = data.findings.map(f => `
    <div class="finding">
      <span class="badge">${escapeHtml(f.severity)}</span>
      <span class="badge">${escapeHtml(f.category)}</span>
      <h3>${escapeHtml(f.title)}</h3>
      <p><b>Evidence:</b> ${escapeHtml(f.evidence)}</p>
      <p><b>Recommendation:</b> ${escapeHtml(f.recommendation)}</p>
    </div>`).join("");

  const ai = data.ai || {};
  if (ai.enabled && !ai.error) {
    $("aiResult").innerHTML = `
      <p>${escapeHtml(ai.summary || "AI analysis completed.")}</p>
      ${listSection("Strengths", ai.strengths)}
      ${listSection("Weaknesses", ai.weaknesses)}
      ${listSection("Priority actions", ai.priority_actions)}`;
  } else {
    const message = ai.message || ai.error || "AI recommendations are unavailable.";
    $("aiResult").innerHTML = `<p>${escapeHtml(message)}</p>${listSection("Rule-based recommendations", ai.recommendations)}`;
  }
}

function listSection(title, values) {
  if (!Array.isArray(values) || values.length === 0) return "";
  return `<h3>${escapeHtml(title)}</h3><ul>${values.map(v => `<li>${escapeHtml(String(v))}</li>`).join("")}</ul>`;
}

function escapeHtml(value) {
  return value.replace(/[&<>'"]/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
  }[char]));
}
