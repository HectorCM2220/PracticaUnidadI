from fastapi import FastAPI, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional, List
import os

app = FastAPI(title="Sistema de Biblioteca")


class Libro:
    """
    Clase que representa un libro dentro de la biblioteca.

    Atributos:
        titulo (str): Título del libro.
        autor (str): Autor del libro.
        ano (str): Año de publicación.
        isbn (str): Código ISBN único.
        categoria (str): Categoría o género del libro.
    """

    def __init__(self, titulo: str, autor: str, ano: str, isbn: str, categoria: str):
        """Inicializa un objeto Libro con sus atributos básicos."""
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.isbn = isbn
        self.categoria = categoria

    def to_dict(self) -> dict:
        """Convierte el objeto libro a un diccionario para JSON."""
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "ano": self.ano,
            "isbn": self.isbn,
            "categoria": self.categoria
        }


class Nodo:
    """
    Clase que representa un nodo dentro de la lista doblemente enlazada.

    Atributos:
        dato (Libro): Objeto Libro almacenado en el nodo.
        siguiente (Nodo): Referencia al siguiente nodo.
        anterior (Nodo): Referencia al nodo anterior.
    """

    def __init__(self, dato: Libro):
        """Inicializa un nodo con un libro y referencias vacías."""
        self.dato = dato
        self.siguiente = None
        self.anterior = None


class ListaDoble:
    """
    Clase que implementa una lista doblemente enlazada para gestionar libros.

    Atributos:
        cabeza (Nodo): Primer nodo de la lista.
        cola (Nodo): Último nodo de la lista.
    """

    def __init__(self):
        """Inicializa una lista doblemente enlazada vacía."""
        self.cabeza = None
        self.cola = None

    def insertar_final(self, libro: Libro):
        """Inserta un libro al final de la lista."""
        nuevo = Nodo(libro)
        if self.cola is None:
            self.cabeza = self.cola = nuevo
        else:
            nuevo.anterior = self.cola
            self.cola.siguiente = nuevo
            self.cola = nuevo

    def obtener_todos(self) -> List[dict]:
        """Devuelve todos los libros en una lista de diccionarios."""
        actual = self.cabeza
        libros = []
        while actual:
            libros.append(actual.dato.to_dict())
            actual = actual.siguiente
        return libros

    def buscar_isbn(self, isbn: str) -> Optional[Nodo]:
        """Busca un libro por su ISBN."""
        actual = self.cabeza
        while actual:
            if actual.dato.isbn == isbn:
                return actual
            actual = actual.siguiente
        return None

    def eliminar(self, isbn: str) -> bool:
        """Elimina un libro de la lista por su ISBN. Retorna True si tuvo éxito."""
        actual = self.cabeza
        while actual:
            if actual.dato.isbn == isbn:
                if actual.anterior:
                    actual.anterior.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente

                if actual.siguiente:
                    actual.siguiente.anterior = actual.anterior
                else:
                    self.cola = actual.anterior
                return True
            actual = actual.siguiente
        return False

# --- Inicialización de la Biblioteca ---
biblioteca = ListaDoble()

# --- Endpoints de la API ---

@app.get("/api/libros")
async def listar_libros():
    """Retorna la lista de todos los libros."""
    return biblioteca.obtener_todos()

@app.post("/api/libros")
async def agregar_libro(data: dict = Body(...)):
    """
    Agrega un nuevo libro. 
    Recibe un JSON con: titulo, autor, ano, isbn, categoria.
    """
    # Validamos que no exista el ISBN (opcional pero recomendado)
    if biblioteca.buscar_isbn(data.get("isbn")):
        raise HTTPException(status_code=400, detail="El ISBN ya existe")
    
    nuevo_libro = Libro(
        titulo=data.get("titulo"),
        autor=data.get("autor"),
        ano=data.get("ano"),
        isbn=data.get("isbn"),
        categoria=data.get("categoria")
    )
    biblioteca.insertar_final(nuevo_libro)
    return {"status": "success", "mensaje": "Libro agregado correctamente"}

@app.delete("/api/libros/{isbn}")
async def eliminar_libro(isbn: str):
    """Elimina un libro por su ISBN."""
    exito = biblioteca.eliminar(isbn)
    if not exito:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return {"status": "success", "mensaje": "Libro eliminado"}

# --- Montaje de archivos estáticos ---
# IMPORTANTE: Esto debe ir al final para no interferir con las rutas de la API
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
async def root():
    """Sirve el archivo index.html principal."""
    return FileResponse("static/index.html")
