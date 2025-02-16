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

    // Pagination and Search for Reports
    let currentPage = 1;
    const perPage = 10;
    let scamChartInstance = null; // To store the chart instance
    
    function fetchReports(page = 1, search = "") {
        fetch(`/api/get_reports?page=${page}&per_page=${perPage}&search=${search}`)
            .then(response => response.json())
            .then(data => {
                console.log("✅ API Response:", data);
    
                let reportTable = document.getElementById("report-table");
                reportTable.innerHTML = "";
    
                let scamCount = 0, safeCount = 0;
                data.reports.forEach(report => {
                    console.log("📜 Report Object:", report);
                    if (report.is_scam) scamCount++; else safeCount++;
    
                    let row = `<tr class='border'>
                        <td class='border p-2'>${report.ad_id || "N/A"}</td>
                        <td class='border p-2'>${report.text || "No description available"}</td>
                        <td class='border p-2'>${report.is_scam ? "✅ Scam" : "❌ Safe"}</td>
                        <td class='border p-2'>${(report.confidence * 100).toFixed(2)}%</td>
                    </tr>`;
                    reportTable.innerHTML += row;
                });
    
                document.getElementById("page-info").textContent = `Page ${data.page} of ${Math.ceil(data.total / perPage)}`;
                currentPage = data.page;
                updateScamChart(scamCount, safeCount);
            })
            .catch(error => console.error("❌ Error fetching reports:", error));
    }
    
    function updateScamChart(scamCount, safeCount) {
        const ctx = document.getElementById('scamChart').getContext('2d');
        
        // Destroy previous chart instance if it exists
        if (scamChartInstance) {
            scamChartInstance.destroy();
        }
    
        scamChartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Scam', 'Safe'],
                datasets: [{
                    label: 'Number of Ads',
                    data: [scamCount, safeCount],
                    borderColor: ['#ff4d4d', '#4caf50'],
                    backgroundColor: 'rgba(0, 0, 0, 0)',
                    borderWidth: 2,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    document.getElementById("prev-page").addEventListener("click", () => {
        if (currentPage > 1) fetchReports(currentPage - 1, document.getElementById("search-bar").value);
    });
    document.getElementById("next-page").addEventListener("click", () => {
        fetchReports(currentPage + 1, document.getElementById("search-bar").value);
    });
    document.getElementById("search-bar").addEventListener("input", (event) => {
        fetchReports(1, event.target.value);
    });

    fetchReports();
});
