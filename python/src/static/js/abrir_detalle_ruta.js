document.getElementById("botonRutaDetalle").addEventListener("click", function() {
    var contenedorRutaDetalle = document.getElementById("contenedorRutaDetalle");
    var contenedorBoton = document.getElementById("contenedorBoton");

    contenedorRutaDetalle.style.display = (contenedorRutaDetalle.style.display === "none") ? "block" : "none";

    if (contenedorRutaDetalle.style.display === "block") {
        contenedorRutaDetalle.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    contenedorBoton.style.display = "none";
});