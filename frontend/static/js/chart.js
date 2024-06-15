const barMockData = {
    labels: ["January", "February", "March", "April", "May", "June"],
    datasets: [
        {
            label: "Category1",
            data: [65, 59, 80, 81, 56, 55],
            backgroundColor: "#d2b4de"
        },
        {
            label: "Category2",
            data: [45, 29, 70, 71, 46, 45],
            backgroundColor: "#aed6f1"
        },
        {
            label: "Category3",
            data: [25, 19, 60, 61, 36, 35],
            backgroundColor: "#fae5d3"
        }
    ]
};

function initializeBarPlot() {
    let barChart = new Chart("Barplot", {
        type: "bar",
        data: {
            labels: barMockData.labels,
            datasets: barMockData.datasets
        },
        options: {
            scales: {
                x: {
                    stacked: true
                },
                y: {
                    stacked: true
                }
            }
        }
    });

    document.getElementById("BarCategoryselect").addEventListener('change', function () {
        let selectedCategory = this.value;
        let newMockData;

        if (selectedCategory === "all") {
            newMockData = barMockData.datasets;
        }
        else {
            newMockData = [barMockData.datasets.find(dataset => dataset.label === selectedCategory)];
        }
        barChart.data.datasets = newMockData;
        barChart.update();
    });
}

const lineMockData = {
    labels: ["January", "February", "March", "April", "May", "June"],
    datasets: [
        {
            label: "Category1",
            data: [65, 59, 80, 81, 56, 55],
            borderColor: "#d2b4de",
            fill: false
        },
        {
            label: "Category2",
            data: [45, 29, 70, 71, 46, 45],
            borderColor: "#aed6f1",
            fill: false
        },
        {
            label: "Category3",
            data: [25, 19, 60, 61, 36, 35],
            borderColor: "#fae5d3",
            fill: false
        }
    ]
};

function initializeLinePlot() {
    let lineChart = new Chart("Lineplot", {
        type: "line",
        data: {
            labels: lineMockData.labels,
            datasets: lineMockData.datasets
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Month'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Value'
                    }
                }
            }
        }
    });

    document.getElementById("LineCategoryselect").addEventListener('change', function () {
        let selectedCategory = this.value;
        let newMockData;

        if (selectedCategory === "all") {
            newMockData = lineMockData.datasets;
        }
        else {
            newMockData = [lineMockData.datasets.find(dataset => dataset.label === selectedCategory)];
        }
        lineChart.data.datasets = newMockData;
        lineChart.update();
    });
}

window.onload = function () {
    initializeBarPlot();
    initializeLinePlot();
}