document.addEventListener("DOMContentLoaded", function () {
    fetch("/filter_expenses/")
        .then(response => response.json())
        .then(data => {
            const categories = data.categories;
            const totals = data.totals;
            const months = data.months;
            const monthTotals = data.month_totals;

            console.log("Fetched Categories:", categories);
            console.log("Fetched Totals:", totals);
            console.log("Fetched Months:", months);
            console.log("Fetched Month Totals:", monthTotals);

            // 🎯 PIE CHART
            new Chart(document.getElementById("pieChart"), {
                type: "pie",
                data: {
                    labels: categories,
                    datasets: [{
                        data: totals,
                        backgroundColor: ["#ff6384", "#36a2eb", "#ffcd56", "#4bc0c0", "#9966ff", "#ff9f40"]
                    }]
                },
                options: { responsive: true }
            });

            // 🎯 BAR CHART
            new Chart(document.getElementById("barChart"), {
                type: "bar",
                data: {
                    labels: categories,
                    datasets: [{
                        label: "Total Expense",
                        data: totals,
                        backgroundColor: "#36a2eb",
                        borderColor: "#007bff",
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    animation: {
                        duration: 2000,
                        easing: "easeInOutBounce"
                    },
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });

            // 🎯 LINE GRAPH (Wave Animation for Monthly Expenses)
            // 🎯 LINE CHART (Fix for Small Screens)
            new Chart(document.getElementById("lineChart"), {
                type: "line",
                data: {
                    labels: months,
                    datasets: [{
                        label: "Monthly Expenses",
                        data: monthTotals,
                        fill: true,
                        borderColor: "#ff6384",
                        backgroundColor: "rgba(255, 99, 132, 0.2)",
                        borderWidth: 2,
                        tension: 0.4 // Creates the wave effect
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,  // ⚠️ Allow flexible resizing
                    animation: {
                        duration: 2000,
                        easing: "easeInOutQuart"
                    },
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });

        })
        .catch(error => console.error("Error fetching data:", error));
});