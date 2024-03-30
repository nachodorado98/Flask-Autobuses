// Funcion para obtener las paradas destino en base a la parada origen correspondiente en el formulario
function actualizarParadas() {
    var paradaSeleccionada = document.getElementById("parada-origen").value;
    var paradaDropdown = document.getElementById("parada-destino");

    while (paradaDropdown.options.length > 0) {
        paradaDropdown.remove(0);
    }

    if (paradaSeleccionada) {

        fetch("/posibles_paradas_destino?parada_origen=" + encodeURIComponent(paradaSeleccionada))
            .then(response => response.json())
            .then(paradas_destino => {

                paradas_destino.forEach(function(paradas_destino) {
                    var option = document.createElement("option");
                    option.text = "Nº "+paradas_destino[0]+": "+paradas_destino[1];
                    option.value = paradas_destino[0];
                    paradaDropdown.add(option);
                });
            })
            .catch(error => console.error("Error al obtener paradas_destino:", error));
    }
}