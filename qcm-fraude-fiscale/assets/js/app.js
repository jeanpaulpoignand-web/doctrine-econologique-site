const state = {
  data: null,
  mode: "quick",
  index: 0,
  answers: {}
};

const STORAGE_KEY = "qcm-fraude-fiscale-v1-1";

const els = {
  intro: document.getElementById("intro"),
  quiz: document.getElementById("quiz"),
  results: document.getElementById("results"),
  quickModeBtn: document.getElementById("quickModeBtn"),
  longModeBtn: document.getElementById("longModeBtn"),
  switchModeBtn: document.getElementById("switchModeBtn"),
  changeModeFromResultsBtn: document.getElementById("changeModeFromResultsBtn"),
  prevBtn: document.getElementById("prevBtn"),
  nextBtn: document.getElementById("nextBtn"),
  restartBtn: document.getElementById("restartBtn"),
  exportBtn: document.getElementById("exportBtn"),
  exportBox: document.getElementById("exportBox"),
  questionCounter: document.getElementById("questionCounter"),
  modeLabel: document.getElementById("modeLabel"),
  progressFill: document.getElementById("progressFill"),
  contextBox: document.getElementById("contextBox"),
  questionTitle: document.getElementById("questionTitle"),
  questionText: document.getElementById("questionText"),
  answers: document.getElementById("answers"),
  explanation: document.getElementById("explanation"),
  methodNote: document.getElementById("methodNote"),
  sourceLinks: document.getElementById("sourceLinks"),
  scoreSummary: document.getElementById("scoreSummary"),
  resultDetails: document.getElementById("resultDetails")
};

async function loadQuestions() {
  const response = await fetch("data/questions_pilier_15.json");
  if (!response.ok) throw new Error("Impossible de charger les questions.");
  state.data = await response.json();
  state.answers = loadStoredAnswers();
}

function getQuestions() {
  return state.data.questions.filter(q => q.modes.includes(state.mode));
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

function startQuiz(mode) {
  state.mode = mode;
  state.index = 0;
  els.intro.classList.add("hidden");
  els.results.classList.add("hidden");
  els.quiz.classList.remove("hidden");
  renderQuestion();
}

function backToIntro() {
  els.quiz.classList.add("hidden");
  els.results.classList.add("hidden");
  els.intro.classList.remove("hidden");
}

function renderQuestion() {
  const questions = getQuestions();
  const q = questions[state.index];
  const current = state.answers[q.id];

  els.questionCounter.textContent = `Question ${state.index + 1} / ${questions.length}`;
  els.modeLabel.textContent = state.mode === "quick" ? "QCM rapide" : "QCM long / pédagogique";
  els.progressFill.style.width = `${((state.index + 1) / questions.length) * 100}%`;

  els.questionTitle.textContent = q.title;
  els.questionText.textContent = q.question;

  if (state.mode === "long" && q.context) {
    els.contextBox.textContent = q.context;
    els.contextBox.classList.remove("hidden");
  } else {
    els.contextBox.classList.add("hidden");
  }

  els.explanation.textContent = q.explanation || "";
  els.methodNote.textContent = q.methodNote ? `Note : ${q.methodNote}` : "";
  renderSources(q);

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

function renderSources(question) {
  if (!question.sources || !question.sources.length) {
    els.sourceLinks.innerHTML = "";
    return;
  }

  const links = question.sources
    .map(id => state.data.sources[id])
    .filter(Boolean)
    .map(src => `<li><a href="${src.url}" target="_blank" rel="noopener">${src.label}</a></li>`)
    .join("");

  els.sourceLinks.innerHTML = `<div class="source-list"><strong>Documents liés :</strong><ul>${links}</ul></div>`;
}

function nextQuestion() {
  const questions = getQuestions();
  if (state.index < questions.length - 1) {
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

  const details = getQuestions().map(q => {
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
  return { finalScore, answered, total: getQuestions().length, details };
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
    mode: state.mode,
    version: state.data.version,
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

function translateValue(value) {
  const map = {
    yes_strong: "Oui fortement",
    yes_moderate: "Oui avec réserve",
    partial: "Position intermédiaire",
    neutral: "Sans avis",
    no_moderate: "Non avec nuance",
    no_strong: "Non fortement"
  };
  return map[value] || "Non répondu";
}

function bindEvents() {
  els.quickModeBtn.addEventListener("click", () => startQuiz("quick"));
  els.longModeBtn.addEventListener("click", () => startQuiz("long"));
  els.switchModeBtn.addEventListener("click", backToIntro);
  els.changeModeFromResultsBtn.addEventListener("click", backToIntro);
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
