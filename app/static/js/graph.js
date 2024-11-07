    // Fonction pour récupérer les données du serveur
    async function fetchData() {
        const response = await fetch('/data/graph-pts-collecte');
        const data = await response.json();
        return data;
    }

    // Générer le graphique
    fetchData().then(data => {
        const labels = Object.keys(data); // Les noms des points de collecte
        const categories = new Set(); // Pour stocker les catégories uniques

        // Organiser les données pour chaque point de collecte
        const datasetMap = {};

        labels.forEach(pt_collecte => {
            data[pt_collecte].forEach(item => {
                categories.add(item.categorie);
                if (!datasetMap[item.categorie]) {
                    datasetMap[item.categorie] = [];
                }
            });
        });

        // Initialiser les datasets pour chaque catégorie
        categories.forEach(categorie => {
            datasetMap[categorie] = labels.map(pt_collecte => {
                const catData = data[pt_collecte].find(item => item.categorie === categorie);
                return catData ? catData.quantite : 0;
            });
        });

        const datasets = Array.from(categories).map(categorie => ({
            label: categorie,
            data: datasetMap[categorie],
            backgroundColor: '#' + Math.floor(Math.random() * 16777215).toString(16), // Couleur aléatoire
        }));

        const ctx = document.getElementById('myChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels, // Les noms des points de collecte
                datasets: datasets, // Les données pour chaque catégorie
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        stacked: true // Empilement des barres
                    },
                    y: {
                        stacked: true // Empilement des barres
                    }
                }
            }
        });
    });
    // Generate random colors for each waste type
    function getRandomColor() {
        return '#' + Math.floor(Math.random() * 16777215).toString(16); // Random hex color
    }

    // Fetch data from Flask API and render chart
    fetch('data/dechets')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('dechetChart').getContext('2d');

            const datasets = [];
            const wasteTypes = {};

            // Process data
            data.details.forEach((categoryDetails, categoryIndex) => {
                categoryDetails.forEach(dechet => {
                    if (!wasteTypes[dechet.nom]) {
                        wasteTypes[dechet.nom] = {
                            label: dechet.nom,
                            backgroundColor: getRandomColor(),
                            data: Array(data.categories.length).fill(0)
                        };
                        datasets.push(wasteTypes[dechet.nom]);
                    }
                    wasteTypes[dechet.nom].data[categoryIndex] = dechet.quantite;
                });
            });

            // Create the stacked bar chart
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.categories,
                    datasets: datasets
                },
                options: {
                    scales: {
                        y: { beginAtZero: true, stacked: true },
                        x: { stacked: true }
                    },
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function (tooltipItem) {
                                    const dataset = tooltipItem.dataset;
                                    return `${dataset.label}: ${dataset.data[tooltipItem.dataIndex]} unités`;
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching data:', error));