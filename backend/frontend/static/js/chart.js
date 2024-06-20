function initializeBarPlot(chartData) {
    let barChart = new Chart("Barplot", {
        type: 'bar',
        data: {
            labels: chartData.map(function (item) { return item[1]; }),
            datasets: [{
                label: 'Num orders',
                data: chartData.map(function (item) { return item[0]; }),
            }]
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
}

function initializeBarPlot2(chartData) {
    let lineChart = new Chart("Barplot2", {
        type: "bar",
        data: {
            labels: chartData.map(function (item) { return item[1]; }),
            datasets: [
                {
                    label: 'Num orders',
                    data: chartData.map(function (item) { return item[0]; }),
                }
            ]
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
}