const API_URL = 'http://127.0.0.1:5000';

document.addEventListener('DOMContentLoaded', () => {
    const predictionForm = document.getElementById('predictionForm');
    const resultCard = document.getElementById('resultCard');
    const riskLevelEl = document.getElementById('riskLevel');
    const reasonEl = document.getElementById('reason');
    const suggestionEl = document.getElementById('suggestion');
    const predictBtn = document.getElementById('predictBtn');
    const btnText = predictBtn.querySelector('.btn-text');
    const loader = predictBtn.querySelector('.loader');

    // Stats Elements
    const totalStudentsEl = document.getElementById('totalStudents');
    const highRiskEl = document.getElementById('highRiskCount');
    const mediumRiskEl = document.getElementById('mediumRiskCount');
    const lowRiskEl = document.getElementById('lowRiskCount');

    // Fetch Initial Stats
    fetchStats();

    predictionForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(predictionForm);
        const data = Object.fromEntries(formData.entries());

        // 1. Show Cinematic Loader
        const executionScreen = document.getElementById('executionScreen');
        const progressBar = document.getElementById('progressBar');
        executionScreen.classList.remove('hidden');
        
        // 2. Animate Progress Bar (5 seconds)
        let progress = 0;
        const loadPctEl = document.getElementById('loadPct');
        progressBar.style.width = '0%'; // Reset progress bar
        const interval = setInterval(() => {
            progress += 2;
            if (progress <= 100) {
                progressBar.style.width = progress + '%';
                loadPctEl.innerText = progress;
            }
            if (progress >= 100) clearInterval(interval);
        }, 100);

        try {
            // 3. Parallel API Call (Start while loading)
            const response = await fetch(`${API_URL}/predict`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();

            // 4. Wait for the 5-second cinematic experience to complete
            setTimeout(() => {
                executionScreen.classList.add('hidden');
                if (response.ok) {
                    showResult(result);
                } else {
                    alert('Error: ' + result.error);
                }
            }, 5000);

        } catch (error) {
            console.error('Error:', error);
            alert('Service error. Please check if backend is running.');
            executionScreen.classList.add('hidden');
        }
    });

    function showResult(result) {
        const resultScreen = document.getElementById('resultScreen');
        resultScreen.classList.remove('hidden');
        
        riskLevelEl.innerText = result.risk_level;
        document.getElementById('riskPercentage').innerText = result.risk_percentage;
        reasonEl.innerText = result.reason;
        suggestionEl.innerText = result.suggestion;

        // Reset and Apply risk classes
        riskLevelEl.className = 'risk-badge';
        const bgClass = result.risk_level.toLowerCase().replace(' ', '-') + '-bg';
        riskLevelEl.classList.add(bgClass);
    }

    // Reset Button Logic
    document.getElementById('resetBtn').addEventListener('click', () => {
        document.getElementById('resultScreen').classList.add('hidden');
        predictionForm.reset();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    async function fetchStats() {
        try {
            const response = await fetch(`${API_URL}/stats`);
            const stats = await response.json();

            totalStudentsEl.innerText = stats.total_students;
            highRiskEl.innerText = stats.high_risk;
            mediumRiskEl.innerText = stats.medium_risk;
            lowRiskEl.innerText = stats.low_risk;

            renderChart(stats);
        } catch (error) {
            console.error('Stats fetch error:', error);
        }
    }

    function renderChart(stats) {
        const ctx = document.getElementById('riskChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Low Risk', 'Medium Risk', 'High Risk'],
                datasets: [{
                    data: [stats.low_risk, stats.medium_risk, stats.high_risk],
                    backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
});
