// Ruta al archivo JSON
const jsonUrl = "resources/js/mascotas.json";
let allMascotas = []; // Variable para almacenar todas las mascotas

// Función para crear las cartas de Bootstrap
function createCard(mascota) {
    return `
        <div class="col-md-4 mb-4">
            <div class="card shadow-sm">
                <img src="${mascota.image}" class="card-img-top" alt="${mascota.name || 'Sin nombre'}">
                <div class="card-body">
                    <h5 class="card-title">${mascota.name || 'Sin nombre'}</h5>
                    <p class="card-text">
                        <strong>Raza:</strong> ${mascota.raza || 'Desconocida'}<br>
                        <strong>Sexo:</strong> ${mascota.sex || 'Desconocido'}<br>
                        <strong>Edad:</strong> ${mascota.age || 'Desconocida'}<br>
                        <strong>Protectora:</strong> ${mascota.protectora || 'Desconocida'}
                    </p>
                    <a href="${mascota.link}" class="btn btn-primary" target="_blank">Más información</a>
                </div>
            </div>
        </div>
    `;
}

// Función para mostrar las mascotas filtradas
function displayMascotas(mascotas) {
    const mascotasContainer = document.getElementById("Mascotas");
    mascotasContainer.innerHTML = ""; // Limpiar contenido previo

    if (mascotas.length === 0) {
        mascotasContainer.innerHTML = "<p>No se encontraron resultados.</p>";
        return;
    }

    mascotas.forEach(mascota => {
        mascotasContainer.innerHTML += createCard(mascota);
    });
}

// Función para aplicar los filtros
function applyFilters() {
    const filterName = document.getElementById("filterName").value.toLowerCase();
    const filterComunidad = document.getElementById("filterComunidad").value;
    const filterRaza = document.getElementById("filterRaza").value;
    const filterSexo = document.getElementById("filterSexo").value;
    const filterProtectora = document.getElementById("filterProtectora").value;

    const filteredMascotas = allMascotas.filter(mascota => {
        const matchesName = !filterName || (mascota.name && mascota.name.toLowerCase().includes(filterName));
        const matchesComunidad = !filterComunidad || (mascota.comunidadAutonoma && mascota.comunidadAutonoma === filterComunidad);
        const matchesRaza = !filterRaza || (mascota.raza && mascota.raza === filterRaza);
        const matchesSexo = !filterSexo || (mascota.sex && mascota.sex === filterSexo);
        const matchesProtectora = !filterProtectora || (mascota.protectora && mascota.protectora === filterProtectora);

        return matchesName && matchesComunidad && matchesRaza && matchesSexo && matchesProtectora;
    });

    displayMascotas(filteredMascotas);
}
// Función para poblar el filtro de Protectora
function populateProtectoraFilter() {
    const filterProtectora = document.getElementById("filterProtectora");

    // Extraer protectorAs únicas del JSON
    const protectoras = [...new Set(allMascotas.map(mascota => mascota.protectora).filter(Boolean))];

    // Ordenar alfabéticamente
    protectoras.sort();

    // Agregar las opciones al filtro
    filterProtectora.innerHTML = '<option value="">Protectora</option>'; // Opción por defecto
    protectoras.forEach(protectora => {
        const option = document.createElement("option");
        option.value = protectora;
        option.textContent = protectora;
        filterProtectora.appendChild(option);
    });
}
// Función para poblar el filtro de Comunidad Autónoma
function populateComunidadFilter() {
    const filterComunidad = document.getElementById("filterComunidad");

    // Extraer comunidades únicas del JSON
    const comunidades = [...new Set(allMascotas.map(mascota => mascota.comunidadAutonoma).filter(Boolean))];

    // Ordenar alfabéticamente
    comunidades.sort();

    // Agregar las opciones al filtro
    filterComunidad.innerHTML = '<option value="">Comunidad Autónoma</option>'; // Opción por defecto
    comunidades.forEach(comunidad => {
        const option = document.createElement("option");
        option.value = comunidad;
        option.textContent = comunidad;
        filterComunidad.appendChild(option);
    });
}

// Función para cargar y mostrar las mascotas
async function loadMascotas() {
    try {
        const response = await fetch(jsonUrl);
        const data = await response.json();

        // Convertir el JSON en un array de mascotas
        allMascotas = Object.keys(data).flatMap(protectora => {
            return data[protectora].map(mascota => ({
                ...mascota,
                protectora // Añadir el nombre de la protectora a cada mascota
            }));
        });
        populateProtectoraFilter(); // Poblar el filtro de Protectora
        populateComunidadFilter(); // Poblar el filtro de Comunidad Autónoma
        displayMascotas(allMascotas); // Mostrar todas las mascotas al inicio
    } catch (error) {
        console.error("Error al cargar las mascotas:", error);
        document.getElementById("Mascotas").innerHTML = "<p>Error al cargar las mascotas. Inténtalo más tarde.</p>";
    }
}

// Añadir eventos a los filtros
document.getElementById("filterName").addEventListener("input", applyFilters);
document.getElementById("filterComunidad").addEventListener("change", applyFilters);
document.getElementById("filterRaza").addEventListener("change", applyFilters);
document.getElementById("filterSexo").addEventListener("change", applyFilters);
document.getElementById("filterProtectora").addEventListener("change", applyFilters);

// Cargar las mascotas al cargar la página
document.addEventListener("DOMContentLoaded", loadMascotas);