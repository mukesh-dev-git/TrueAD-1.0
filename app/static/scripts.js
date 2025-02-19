// static/scripts.js - Interactive UI Enhancements for TrueAD

document.addEventListener("DOMContentLoaded", () => {
    // Toggle Sidebar
    const toggleButton = document.querySelector("#toggleSidebar");
    const sidebar = document.querySelector("#sidebar");
    
    if (toggleButton && sidebar) {
        toggleButton.addEventListener("click", () => {
            sidebar.classList.toggle("-translate-x-full");
        });
    }

    // Live Scam Alerts - WebSocket Integration
    const socket = io();
    socket.on("scam_alert", (data) => {
        const alertsList = document.querySelector("#live-alerts");
        if (alertsList) {
            const newAlert = document.createElement("li");
            newAlert.textContent = data.message;
            newAlert.classList.add("p-2", "bg-red-200", "rounded", "mt-1");
            alertsList.prepend(newAlert);
        }
    });

    let scamChartInstance = null;
    
    function fetchOverallStatistics() {
        fetch("/api/get_overall_statistics")
            .then(response => response.json())
            .then(data => {
                console.log("✅ Overall Statistics Response:", data);
                updateScamChart(data);
            })
            .catch(error => console.error("❌ Error fetching overall statistics:", error));
    }
    
    function updateScamChart(data) {
        const ctx = document.getElementById('scamChart').getContext('2d');
        
        if (scamChartInstance) {
            scamChartInstance.destroy();
        }

        scamChartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Scam', 'Safe'],
                datasets: [
                    {
                        label: 'Total Ads',
                        data: [data.total_scam, data.total_safe],
                        borderColor: '#ff4d4d',
                        backgroundColor: 'rgba(255, 77, 77, 0.3)',
                        borderWidth: 2,
                        fill: false
                    },
                    {
                        label: 'Confidence Level',
                        data: [data.avg_scam_confidence, data.avg_safe_confidence],
                        borderColor: '#4caf50',
                        backgroundColor: 'rgba(76, 175, 80, 0.3)',
                        borderWidth: 2,
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        suggestedMax: 100
                    }
                }
            }
        });
    }

    fetchOverallStatistics();
});
