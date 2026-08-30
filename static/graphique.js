const donnees = JSON.parse(document.getElementById('graphiqueCodes').dataset.stats);
const labels = Object.keys(donnees);
const valeurs = Object.values(donnees);

new Chart(document.getElementById('graphiqueCodes'), {
    type: 'bar',
    data: { 
        labels : labels ,
        datasets : [{
            label : 'Nombre de logs par code',
            data : valeurs,
        }]
    }
});
