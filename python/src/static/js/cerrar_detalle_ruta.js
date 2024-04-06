document.getElementById("botonCerrarDetalle").addEventListener("click", function() {
    var contenedorRutaDetalle = document.getElementById("contenedorRutaDetalle");
    var contenedorBoton = document.getElementById("contenedorBoton");

    contenedorRutaDetalle.style.display = "none";
    contenedorBoton.style.display = "block";
});