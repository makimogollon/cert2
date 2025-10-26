/* CUENTA REGRESIVA */

var fecha = new Date(2025, 8, 13, 20)

var miliseg = fecha.getTime()

var pdias = document.querySelector("#dias")
var phoras = document.querySelector("#horas")
var pmin = document.querySelector("#minutos")
var pseg = document.querySelector("#segundos")
var cuenta = document.querySelector("#cuenta")

var intervalo = setInterval(() =>{
    var hoy = new Date().getTime()

    var restante = miliseg - hoy /* no da en milisegundos */

    var msDias = (1000*60*60*24)
    var msHoras = (1000*60*60)
    var msMin = (1000*60)
    var msSeg = 1000
    
    var dias = Math.floor(restante / msDias)
    var horas = Math.floor((restante % msDias)/ msHoras)
    var minutos = Math.floor((restante % msHoras) / msMin)
    var segundos = Math.floor((restante % msMin )/ msSeg)

    pdias.innerText = dias < 10 ? "0" + dias:dias
    phoras.innerText = horas < 10 ? "0" +horas:horas
    pmin.innerText = minutos < 10 ? "0" +minutos:minutos
    pseg.innerText = segundos < 10 ? "0" +segundos:segundos

    if (restante < 0){
        clearInterval(intervalo);
        cuenta.innerHTML = "<p> El evento ha comenzado!"
    }

}, 1000)

/* SECCION DE COMENTARIOS */

document.addEventListener("DOMContentLoaded", () => {
    var boton = document.getElementById("boton")
    var nombreInput = document.getElementById("nombre")
    var mensajeInput = document.getElementById("mensaje")
    var listaCom = document.querySelector("#comentarios ul")

    boton.addEventListener("click", () => {
        var nombre = nombreInput.value
        var mensaje = mensajeInput.value

        if (!nombre || !mensaje) {
            alert("Complete todos los campos")
            return
        }
        var fechaActual = new Date().toLocaleString()

        var newCom = document.createElement("li")
        newCom.classList.add("col-12", "col-md-6", "col-lg-4")
        newCom.innerHTML = 
            '<div class="card">' +
                '<h5 id="nombreEstilo">' + nombre + '</h5>' +
                '<p id="fechaEstilo">' + fechaActual +'</p>' +
                '<p id="mensajeEstilo">' + mensaje +'</p>' +
            '</div>'
            
        listaCom.appendChild(newCom)

        nombreInput.value = ""
        mensajeInput.value = ""
    })
})