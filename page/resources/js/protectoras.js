async function loadJSON(ruta) {
    try {
        const response = await fetch(ruta);
        if (!response.ok) {
            throw new Error('Error en la red: ' + response.statusText);
        }
        return await response.json();
    } catch (error) {
        console.error('Hubo un problema al obtener los datos:', error);
    }
}
let ruta = "resources/js/protectoras.json"
const protectoras = await loadJSON(ruta);
const comunidades = Object.keys(protectoras);

for (let comunidad of comunidades) {
    const comunidadAutonoma = document.createElement("details");
    comunidadAutonoma.className = "comunidad";

    const titulo = document.createElement("summary");
    const tituloTexto = document.createElement("h2");
    tituloTexto.textContent = comunidad;
    titulo.appendChild(tituloTexto);
    comunidadAutonoma.appendChild(titulo);

    const protectorasCaja = document.createElement("div");
    protectorasCaja.classList.add("protectoras");

    for (let protectora of protectoras[comunidad]) {
        const protectoraCaja = document.createElement("div");
        protectoraCaja.id = protectora.number;
        protectoraCaja.classList.add("protectoraCaja", "card");

        protectoraCaja.innerHTML += `
            <h5 class="card-title">${protectora.name}</h5>
        `;

        if (protectora.web) {
            protectoraCaja.innerHTML += `
                <a class='btn btn-outline-success' href='${protectora.web}' target="_blank">Sitio Web</a>
            `;
        }
            
        // Añadir los atributos para activar el modal cuando se hace clic en la tarjeta
        protectoraCaja.setAttribute("data-bs-toggle", "modal");  // Para activar el modal
        protectoraCaja.setAttribute("data-bs-target", "#modalInfo");  // ID del modal
        protectoraCaja.setAttribute("data-id", protectora.number);  // ID de la protectora para identificarla


        protectorasCaja.appendChild(protectoraCaja);
    }

    comunidadAutonoma.appendChild(protectorasCaja);
    document.querySelector("#CAs").appendChild(comunidadAutonoma);
}
// add event listener to the button
[...document.querySelectorAll(".protectoraCaja")].forEach(x => {
    x.addEventListener("click", async () => {
        // get element clicked
        const protectoraCaja = event.currentTarget;
        // get the id of the clicked element
        const id = protectoraCaja.id;

        const protectora = await (await fetch(ruta)).json().then(data => {
            // get the comunidad of the clicked element
            const comunidad = Object.keys(data)

            for (let com of comunidad) {
                // get the protectora of the clicked element
                const protectora = data[com].find(p => p.number == id);
                if (protectora) {
                    return protectora;
                }
            }
        })
        if (protectora) {
            const modalBody = document.querySelector("#protectoraInfo");
            modalBody.innerHTML = `
            ${protectora.logo ? `
            <div class="text-center mb-4">
                <img src="${protectora.logo}" alt="${protectora.name}" class="img-fluid" style="max-height: 150px; max-width: 200px;">
            </div>` : ""
            }

            <h4>${protectora.name || "Nombre no disponible"}</h4>
            ${protectora.comunidad_autonoma ? `<p><strong>Comunidad Autónoma:</strong> ${protectora.comunidad_autonoma}</p>` : ""}
            ${protectora.phone ? `<p><strong>Teléfono:</strong> ${protectora.phone}</p>` : ""}
            ${protectora.mailto ? `<p><strong>Correo:</strong> <a href="mailto:${protectora.mailto}">${protectora.mailto}</a></p>` : ""}
            ${protectora.web ? `<p><strong>Sitio Web:</strong> <a href="${protectora.web}" target="_blank">${protectora.web}</a></p>` : ""}
            ${protectora.paginas && protectora.paginas.length > 0 ? `
            <p><strong>Páginas de adopción:</strong></p>
            <p>${protectora.paginas.map(pagina => `<a href="${protectora.web + pagina}" target="_blank">${protectora.web + pagina}</a>`).join(', ')}</p>
            ` : ""}
        `;
        }


    })
});
