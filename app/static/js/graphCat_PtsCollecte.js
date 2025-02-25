function getPointCollecteIdFromUrl() {
    const path = window.location.pathname; 
    const parts = path.split('/');  
    // console.log(parts[parts.length - 1]);
    return parts[parts.length - 1];
}

async function fetchData(pointCollecteId) {
    const response = await fetch(`/data/graph-pts-collecte/${pointCollecteId}`);
    const data = await response.json();
    return data;
}

async function generateChart() {
    const ptCollecteId = getPointCollecteIdFromUrl(); 
    const data = await fetchData(ptCollecteId); 

    const pointCollecteName = Object.keys(data)[0]; 
    const collecteData = data[pointCollecteName]; 

    if (!collecteData || collecteData.length === 0) {
        console.log("Aucune donnée trouvée pour l'ID du point de collecte:", ptCollecteId);
        return;
    }

    function getRandomColor() {
        return '#' + Math.floor(Math.random() * 16777215).toString(16);
    }

    const datasets = collecteData.map(item => ({
        label: item.categorie, 
        data: [parseFloat(item.quantite)], 
        backgroundColor: getRandomColor(), 
    }));

    const ctx = document.getElementById('ptCollecteChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [pointCollecteName], 
            datasets: datasets 
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            },
            plugins: {
                legend: { display: true }, 
                tooltip: {
                    callbacks: {
                        label: function (tooltipItem) {
                            return `${tooltipItem.dataset.label}: ${tooltipItem.raw} unités`;
                        }
                    }
                }
            }
        }
    });
}

// generateChart();

document.addEventListener("DOMContentLoaded", function () {
    const graphButton = document.getElementById("graphButton");
    const graphContainer = document.getElementById("graphContainer");

    graphButton.addEventListener("click", function () {
        if (graphContainer.style.display === "none") {
            graphContainer.style.display = "block";
            graphButton.textContent = "Masquer le détail";
            generateChart(); // Appelle la fonction pour générer le graphique
        } else {
            graphContainer.style.display = "none";
            graphButton.textContent = "Afficher le détail";
        }
    });
});


