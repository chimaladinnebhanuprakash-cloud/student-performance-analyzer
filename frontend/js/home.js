// Home Page JavaScript
let performanceChart = null;
let attendanceChart = null;

// Load home page data
async function loadHomeData() {
    try {
        // Get user session data
        const sessionResponse = await fetch(`${API_BASE}/check-session`, {
            credentials: 'include'
        });
        const sessionData = await sessionResponse.json();

        if (sessionData.logged_in) {
            // Update welcome message
            const firstName = sessionData.user.full_name.split(' ')[0];
            document.getElementById('userName').textContent = firstName;
        }

        // Get latest analysis
        const analysisResponse = await fetch(`${API_BASE}/analysis-history`, {
            credentials: 'include'
        });
        const analysisData = await analysisResponse.json();

        if (analysisData.success && analysisData.history.length > 0) {
            const latestAnalysis = analysisData.history[0];

            // Update summary cards
            document.getElementById('performanceLevel').textContent = latestAnalysis.category || 'N/A';

            // Get performance history for chart
            const performanceResponse = await fetch(`${API_BASE}/performance-history`, {
                credentials: 'include'
            });
            const performanceData = await performanceResponse.json();

            if (performanceData.success && performanceData.history.length > 0) {
                const latestPerformance = performanceData.history[0];
                const subjectKeys = Object.keys(latestPerformance.subject_marks);
                const marks = Object.values(latestPerformance.subject_marks);
                const avgMarks = marks.reduce((a, b) => a + b, 0) / marks.length;

                // Update summary cards
                document.getElementById('averageMarks').textContent = avgMarks.toFixed(1) + '%';
                document.getElementById('attendancePercent').textContent = latestPerformance.attendance + '%';
                document.getElementById('activeSubjects').textContent = subjectKeys.length;

                // Create charts
                createPerformanceChart(analysisData.history);
                createAttendanceChart(latestPerformance.attendance);
            } else {
                setEmptyState();
            }
        } else {
            setEmptyState();
        }
    } catch (error) {
        console.error('Error loading home data:', error);
        setEmptyState();
    }
}

function setEmptyState() {
    document.getElementById('performanceLevel').textContent = 'Not Analyzed';
    document.getElementById('averageMarks').textContent = 'N/A';
    document.getElementById('attendancePercent').textContent = 'N/A';
    document.getElementById('activeSubjects').textContent = '0';
    createEmptyChart();
}

// Create performance chart
function createPerformanceChart(history) {
    const ctx = document.getElementById('performanceChart').getContext('2d');
    if (!ctx) return;

    if (performanceChart) performanceChart.destroy();

    const reversedHistory = [...history].reverse();
    const labels = reversedHistory.map(item => {
        const date = new Date(item.created_at + ' UTC');
        return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
    });
    const scores = reversedHistory.map(item => item.performance_score);

    // Create Gradient
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(102, 126, 234, 0.4)');
    gradient.addColorStop(1, 'rgba(102, 126, 234, 0.0)');

    performanceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Performance Score',
                data: scores,
                borderColor: '#667eea',
                backgroundColor: gradient,
                borderWidth: 4,
                tension: 0.45,
                fill: true,
                pointBackgroundColor: '#667eea',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 8,
                pointHoverBackgroundColor: '#764ba2',
                pointHoverBorderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(26, 26, 46, 0.95)',
                    titleFont: { size: 14, weight: 'bold' },
                    bodyFont: { size: 13 },
                    padding: 12,
                    displayColors: false,
                    callbacks: {
                        label: (context) => ` Score: ${context.parsed.y}%`
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#7a7a8c', font: { family: 'Inter' } }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#7a7a8c', font: { family: 'Inter' } }
                }
            }
        }
    });
}

// Create Attendance Doughnut Chart
function createAttendanceChart(percentage) {
    const ctx = document.getElementById('attendanceChart');
    if (!ctx) return;

    if (attendanceChart) attendanceChart.destroy();

    const color = percentage >= 75 ? '#4facfe' : (percentage >= 60 ? '#f093fb' : '#fa709a');

    attendanceChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Present', 'Absent'],
            datasets: [{
                data: [percentage, 100 - percentage],
                backgroundColor: [color, 'rgba(255, 255, 255, 0.05)'],
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '75%',
            plugins: {
                legend: { display: false },
                tooltip: { enabled: true }
            }
        }
    });
}

// Create empty chart when no data
function createEmptyChart() {
    const ctx = document.getElementById('performanceChart');

    if (!ctx) return;

    if (performanceChart) {
        performanceChart.destroy();
    }

    performanceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Start'],
            datasets: [{
                label: 'Performance Score',
                data: [0],
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 3,
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: '#b4b4c5',
                        font: {
                            family: 'Inter',
                            size: 12
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        color: '#7a7a8c'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    }
                },
                x: {
                    ticks: {
                        color: '#7a7a8c'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    }
                }
            }
        }
    });
}

// Load data when page loads
loadHomeData();
