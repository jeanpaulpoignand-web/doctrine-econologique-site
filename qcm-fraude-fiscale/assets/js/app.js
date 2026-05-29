const state = {
  data: null,
  index: 0,
  answers: {}
};

const STORAGE_KEY = "qcm-national-v1-answers";

const els = {
  intro: document.getElementById("intro"),
  quiz: document.getElementById("quiz"),
  results: document.getElementById("results"),
  startBtn: document.getElementById("startBtn"),
  prevBtn: document.getElementById("prevBtn"),
  nextBtn: document.getElementById("nextBtn"),
  restartBtn: document.getElementById("restartBtn"),
  exportBtn: document.getElementById("exportBtn"),
  exportBox: document.getElementById("exportBox"),
  questionCounter: document.getElementById("questionCounter"),
  pillarLabel: document.getElementById("pillarLabel"),
  progressFill: document.getElementById("progressFill"),
  questionTitle: document.getElementById("questionTitle"),
  questionText: document.getElementById("questionText"),
  answers: document.getElementById("answers"),
  explanation: document.getElementById("explanation"),
  confidence: document.getElementById("confidence"),
  scoreSummary: document.getElementById("scoreSummary"),
  resultDetails: document.getElementById("resultDetails")
};

async function loadQuestions() {
  const response = await fetch("data/questions_pilier_15.json");
  if (!response.ok) {
    throw new Error("Impossible de charger les questions.");
  }
  state.data = await response.json();
  state.answers = loadStoredAnswers();
}

function loadStoredAnswers() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

function saveAnswers() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state.answers));
}

function startQuiz() {
  els.intro.classList.add("hidden");
  els.results.classList.add("hidden");
  els.quiz.classList.remove("hidden");
  renderQuestion();
}

function renderQuestion() {
  const questions = state.data.questions;
  const q = questions[state.index];
  const current = state.answers[q.id];

  els.questionCounter.textContent = `Question ${state.index + 1} / ${questions.length}`;
  els.pillarLabel.textContent = `${state.data.pillarId} — ${state.data.pillarTitle}`;
  els.progressFill.style.width = `${((state.index + 1) / questions.length) * 100}%`;

  els.questionTitle.textContent = q.title;
  els.questionText.textContent = q.question;
  els.explanation.textContent = q.explanation;
  els.confidence.textContent = `Niveau de confiance : ${translateConfidence(q.confidence)}.`;

  els.answers.innerHTML = "";
  q.answers.forEach(answer => {
    const button = document.createElement("button");
    button.className = "answer-button";
    if (current === answer.value) button.classList.add("selected");
    button.type = "button";
    button.textContent = `${answer.id}. ${answer.label}`;
    button.addEventListener("click", () => {
      state.answers[q.id] = answer.value;
      saveAnswers();
      renderQuestion();
    });
    els.answers.appendChild(button);
  });

  els.prevBtn.disabled = state.index === 0;
  els.nextBtn.textContent = state.index === questions.length - 1 ? "Voir les résultats" : "Suivant";
}

function nextQuestion() {
  if (state.index < state.data.questions.length - 1) {
    state.index++;
    renderQuestion();
  } else {
    showResults();
  }
}

function prevQuestion() {
  if (state.index > 0) {
    state.index--;
    renderQuestion();
  }
}

function compareAnswers(userValue, doctrinalValue) {
  if (!userValue || userValue === "neutral") return null;
  if (userValue === doctrinalValue) return 100;

  const closePairs = [
    ["yes_strong", "yes_moderate"],
    ["no_strong", "no_moderate"],
    ["partial", "yes_moderate"],
    ["partial", "no_moderate"]
  ];

  if (isClose(userValue, doctrinalValue, closePairs)) return 75;
  if (userValue === "partial" || doctrinalValue === "partial") return 50;

  const bothYes = userValue.startsWith("yes") && doctrinalValue.startsWith("yes");
  const bothNo = userValue.startsWith("no") && doctrinalValue.startsWith("no");
  if (bothYes || bothNo) return 60;

  return 0;
}

function isClose(a, b, pairs) {
  return pairs.some(([x, y]) => (a === x && b === y) || (a === y && b === x));
}

function calculateScore() {
  let weightedScore = 0;
  let totalWeight = 0;
  let answered = 0;

  const details = state.data.questions.map(q => {
    const userValue = state.answers[q.id];
    const score = compareAnswers(userValue, q.doctrinalPosition);
    const weight = q.weight || 1;

    if (userValue && userValue !== "neutral") answered++;
    if (score !== null) {
      weightedScore += score * weight;
      totalWeight += weight;
    }

    return { question: q, userValue, score, weight };
  });

  const finalScore = totalWeight > 0 ? Math.round(weightedScore / totalWeight) : 0;
  return { finalScore, answered, total: state.data.questions.length, details };
}

function showResults() {
  els.quiz.classList.add("hidden");
  els.results.classList.remove("hidden");

  const result = calculateScore();
  els.scoreSummary.textContent = `Score d’alignement avec la ligne doctrinale du Pilier 15 : ${result.finalScore} % — ${result.answered}/${result.total} questions répondues.`;

  els.resultDetails.innerHTML = "";
  result.details.forEach(item => {
    const div = document.createElement("div");
    const status = item.score === null ? "partial" : item.score >= 75 ? "ok" : item.score >= 50 ? "partial" : "ko";
    div.className = `result-item ${status}`;
    div.innerHTML = `
      <h3>${item.question.id} — ${item.question.title}</h3>
      <p><strong>Votre réponse :</strong> ${translateValue(item.userValue)}</p>
      <p><strong>Position doctrinale :</strong> ${translateValue(item.question.doctrinalPosition)}</p>
      <p><strong>Score :</strong> ${item.score === null ? "neutralisé" : item.score + " %"}</p>
      <p>${item.question.explanation}</p>
    `;
    els.resultDetails.appendChild(div);
  });
}

function exportResults() {
  const result = calculateScore();
  const payload = {
    date: new Date().toISOString(),
    pillarId: state.data.pillarId,
    pillarTitle: state.data.pillarTitle,
    score: result.finalScore,
    answered: result.answered,
    total: result.total,
    answers: state.answers
  };
  els.exportBox.textContent = JSON.stringify(payload, null, 2);
  els.exportBox.classList.remove("hidden");
}

function restartQuiz() {
  if (confirm("Voulez-vous effacer vos réponses et recommencer ?")) {
    state.index = 0;
    state.answers = {};
    localStorage.removeItem(STORAGE_KEY);
    els.results.classList.add("hidden");
    els.exportBox.classList.add("hidden");
    els.intro.classList.remove("hidden");
  }
}

function translateConfidence(value) {
  const map = {
    high: "élevé",
    medium: "moyen",
    low: "faible",
    unverified: "non vérifié"
  };
  return map[value] || value || "non renseigné";
}

function translateValue(value) {
  const map = {
    yes_strong: "Oui fortement",
    yes_moderate: "Oui avec réserve",
    partial: "Partiellement",
    neutral: "Sans avis",
    no_moderate: "Non avec nuance",
    no_strong: "Non fortement",
    undefined: "Non répondu"
  };
  return map[value] || "Non répondu";
}

function bindEvents() {
  els.startBtn.addEventListener("click", startQuiz);
  els.nextBtn.addEventListener("click", nextQuestion);
  els.prevBtn.addEventListener("click", prevQuestion);
  els.restartBtn.addEventListener("click", restartQuiz);
  els.exportBtn.addEventListener("click", exportResults);
}

loadQuestions()
  .then(bindEvents)
  .catch(error => {
    document.body.innerHTML = `<main class="container"><section class="card"><h1>Erreur</h1><p>${error.message}</p></section></main>`;
  });
