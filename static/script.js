/**
 * Lógica del Frontend para la Lista Doblemente Enlazada
 * Maneja la navegación entre nodos, búsqueda y registro.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Referencias al DOM
    const form = document.getElementById('libro-form');
    const nodeContainer = document.getElementById('active-node-container');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const currentIndexLabel = document.getElementById('current-index');
    const totalNodesLabel = document.getElementById('total-nodes');
    const searchInput = document.getElementById('search');
    const toast = document.getElementById('toast');

    // Estado local de la vista
    let librosData = [];
    let pointer = 0; // Representa el nodo actual en pantalla

    // --- INICIALIZACIÓN ---
    fetchLibros();

    // --- EVENTOS ---

    // Navegación de la Lista (Nodos)
    prevBtn.addEventListener('click', () => {
        if (pointer > 0) {
            pointer--;
            updateView('prev');
        }
    });

    nextBtn.addEventListener('click', () => {
        if (pointer < librosData.length - 1) {
            pointer++;
            updateView('next');
        }
    });

    // Envío del Formulario (Insertar Final)
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const nuevoLibro = {
            titulo: document.getElementById('titulo').value,
            autor: document.getElementById('autor').value,
            ano: document.getElementById('ano').value,
            isbn: document.getElementById('isbn').value,
            categoria: document.getElementById('categoria').value
        };

        try {
            const res = await fetch('/api/libros', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(nuevoLibro)
            });

            const data = await res.json();

            if (res.ok) {
                showToast("Libro enlazado exitosamente");
                form.reset();
                await fetchLibros();
                // Movemos el puntero al nuevo elemento (el final)
                pointer = librosData.length - 1;
                updateView();
            } else {
                showToast(data.detail || "Error al registrar", "error");
            }
        } catch (error) {
            showToast("Sin respuesta del servidor", "error");
        }
    });

    // Buscador (Filtro)
    searchInput.addEventListener('input', () => {
        const query = searchInput.value.toLowerCase();
        if (query === "") {
            fetchLibros();
            return;
        }

        // Buscamos el primer match y saltamos a él
        const matchIndex = librosData.findIndex(l =>
            l.titulo.toLowerCase().includes(query) ||
            l.autor.toLowerCase().includes(query) ||
            l.isbn.toLowerCase().includes(query)
        );

        if (matchIndex !== -1) {
            pointer = matchIndex;
            updateView();
        }
    });

    // --- FUNCIONES CORE ---

    /**
     * Obtiene los libros del backend y actualiza el estado local.
     */
    async function fetchLibros() {
        try {
            const res = await fetch('/api/libros');
            librosData = await res.json();
            updateView();
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    }

    /**
     * Actualiza la interfaz visual del nodo actual.
     * @param {string} direction - Dirección del movimiento para animación.
     */
    function updateView(direction = null) {
        if (librosData.length === 0) {
            renderEmpty();
            return;
        }

        const libro = librosData[pointer];

        // Aplicar animación de slide
        nodeContainer.style.opacity = '0';
        nodeContainer.style.transform = direction === 'next' ? 'translateX(20px)' : (direction === 'prev' ? 'translateX(-20px)' : 'scale(0.95)');

        setTimeout(() => {
            renderNode(libro);
            nodeContainer.style.opacity = '1';
            nodeContainer.style.transform = 'translateX(0) scale(1)';

            // Actualizar estados
            currentIndexLabel.textContent = pointer + 1;
            totalNodesLabel.textContent = librosData.length;

            prevBtn.disabled = pointer === 0;
            nextBtn.disabled = pointer === librosData.length - 1;
        }, 200);
    }

    function renderNode(libro) {
        nodeContainer.innerHTML = `
            <div class="node-content">
                <h3>${libro.titulo}</h3>
                <p class="author">por ${libro.autor}</p>
                <div class="node-details">
                    <div class="detail-item">
                        <span>Lanzamiento</span>
                        <p>${libro.ano}</p>
                    </div>
                    <div class="detail-item">
                        <span>Categoría</span>
                        <p>${libro.categoria}</p>
                    </div>
                    <div class="detail-item">
                        <span>Código ISBN</span>
                        <p>${libro.isbn}</p>
                    </div>
                </div>
                <a class="delete-action" onclick="window.confirmDelete('${libro.isbn}')">Eliminar este nodo</a>
            </div>
        `;
    }

    function renderEmpty() {
        nodeContainer.innerHTML = `<div class="empty-state"><p>Registre un libro</p></div>`;
        currentIndexLabel.textContent = 0;
        totalNodesLabel.textContent = 0;
        prevBtn.disabled = true;
        nextBtn.disabled = true;
    }

    function showToast(msg) {
        toast.textContent = msg;
        toast.classList.remove('hidden');
        setTimeout(() => toast.classList.add('hidden'), 3000);
    }

    // Exponer función de borrado al scope global
    window.confirmDelete = async (isbn) => {
        try {
            const res = await fetch(`/api/libros/${isbn}`, { method: 'DELETE' });
            if (res.ok) {
                showToast("Nodo eliminado");
                await fetchLibros();
                pointer = 0; // Reiniciar vista
                updateView();
            }
        } catch (err) {
            console.error(err);
        }
    };
});
