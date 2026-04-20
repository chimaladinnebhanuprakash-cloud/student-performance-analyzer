// Performance Analyzer JavaScript
let subjectRadarChart = null;
let currentSubjectMarks = {}; // Store marks for visualization

// Wait for DOM to be ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAnalyzer);
} else {
    initAnalyzer();
}

function initAnalyzer() {
    const analyzerForm = document.getElementById('analyzerForm');
    if (!analyzerForm) {
        setTimeout(initAnalyzer, 100);
        return;
    }

    const analyzeBtn = document.getElementById('analyzeBtn');
    const analyzeBtnText = document.getElementById('analyzeBtnText');
    const analyzeBtnLoading = document.getElementById('analyzeBtnLoading');
    const analysisResults = document.getElementById('analysisResults');

    analyzerForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const subjectNames = document.querySelectorAll('.subject-name');
        const subjectMarksInputs = document.querySelectorAll('.subject-marks');
        currentSubjectMarks = {}; // Reset

        for (let i = 0; i < subjectNames.length; i++) {
            const name = subjectNames[i].value.trim();
            const marks = parseFloat(subjectMarksInputs[i].value);

            if (name && !isNaN(marks)) {
                currentSubjectMarks[name] = marks;
            }
        }

        if (Object.keys(currentSubjectMarks).length === 0) {
            alert('Please add at least one subject with marks');
            return;
        }

        const attendance = parseFloat(document.getElementById('attendance').value);
        const studyHours = parseFloat(document.getElementById('studyHours').value);
        const backlogs = parseInt(document.getElementById('backlogs').value);

        analyzeBtnText.classList.add('hidden');
        analyzeBtnLoading.classList.remove('hidden');
        analyzeBtn.disabled = true;

        try {
            const response = await fetch(`${API_BASE}/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({
                    subject_marks: currentSubjectMarks,
                    attendance,
                    study_hours: studyHours,
                    backlogs
                })
            });

            const data = await response.json();

            if (data.success) {
                displayAnalysisResults(data.analysis);
            } else {
                alert(data.error || 'Analysis failed');
            }
        } catch (error) {
            console.error('Analysis error:', error);
            alert('Network error. Please try again.');
        } finally {
            analyzeBtnText.classList.remove('hidden');
            analyzeBtnLoading.classList.add('hidden');
            analyzeBtn.disabled = false;
        }
    });
}

// Add new subject row
function addSubject() {
    const container = document.getElementById('subjectsContainer');
    if (!container) return;

    const subjectRow = document.createElement('div');
    subjectRow.className = 'subject-row';
    subjectRow.innerHTML = `
        <div>
            <input type="text" class="form-input subject-name" placeholder="Subject name" required>
        </div>
        <div>
            <input type="number" class="form-input subject-marks" placeholder="Marks (0-100)" min="0" max="100" required>
        </div>
        <div>
            <button type="button" class="btn-remove" onclick="removeSubject(this)">Remove</button>
        </div>
    `;
    container.appendChild(subjectRow);
}

// Remove subject row
function removeSubject(button) {
    const container = document.getElementById('subjectsContainer');
    if (!container) return;
    if (container.children.length > 1) {
        button.closest('.subject-row').remove();
    } else {
        alert('At least one subject is required');
    }
}

// Display analysis results
function displayAnalysisResults(analysis) {
    const scoreValue = document.getElementById('scoreValue');
    const scoreCategory = document.getElementById('scoreCategory');
    const explanationText = document.getElementById('explanationText');
    const suggestionsList = document.getElementById('suggestionsList');
    const analysisResults = document.getElementById('analysisResults');

    if (!scoreValue || !scoreCategory || !explanationText || !suggestionsList || !analysisResults) return;

    scoreValue.textContent = analysis.score;
    scoreCategory.textContent = analysis.category;
    explanationText.textContent = analysis.explanation;
    suggestionsList.innerHTML = '';

    analysis.suggestions.forEach(suggestion => {
        const li = document.createElement('li');
        li.textContent = suggestion;
        suggestionsList.appendChild(li);
    });

    // Create Radar Chart
    createSubjectRadarChart();

    analysisResults.classList.add('show');
    analysisResults.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Create Radar Chart for Subject Performance
function createSubjectRadarChart() {
    const ctx = document.getElementById('subjectRadarChart');
    if (!ctx) return;

    if (subjectRadarChart) subjectRadarChart.destroy();

    const labels = Object.keys(currentSubjectMarks);
    const data = Object.values(currentSubjectMarks);

    subjectRadarChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Score by Subject',
                data: data,
                backgroundColor: 'rgba(102, 126, 234, 0.2)',
                borderColor: '#667eea',
                borderWidth: 3,
                pointBackgroundColor: '#667eea',
                pointBorderColor: '#fff',
                pointRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                    pointLabels: {
                        color: '#b4b4c5',
                        font: { size: 12, family: 'Inter' }
                    },
                    ticks: { display: false }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}
