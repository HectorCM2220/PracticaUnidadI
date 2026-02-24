from fastapi import FastAPI, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional, List
import os
import json

app = FastAPI(title="Sistema de Biblioteca")

DB_FILE = "libros.json"


class Libro:
    """Clase que representa un libro."""
    def __init__(self, titulo: str, autor: str, ano: str, isbn: str, categoria: str):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.isbn = isbn
        self.categoria = categoria

    def to_dict(self) -> dict:
        return {
            "titulo": self.titulo, "autor": self.autor,
            "ano": self.ano, "isbn": self.isbn, "categoria": self.categoria
        }

class Nodo:
    """Clase que representa un nodo de la lista doble."""
    def __init__(self, dato: Libro):
        self.dato = dato
        self.siguiente = None
        self.anterior = None

class ListaDoble:
    """Lista doblemente enlazada con persistencia y múltiples tipos de inserción."""
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.size = 0

    def insertar_final(self, libro: Libro):
        nuevo = Nodo(libro)
        if self.cola is None:
            self.cabeza = self.cola = nuevo
        else:
            nuevo.anterior = self.cola
            self.cola.siguiente = nuevo
            self.cola = nuevo
        self.size += 1

    def insertar_inicio(self, libro: Libro):
        nuevo = Nodo(libro)
        if self.cabeza is None:
            self.cabeza = self.cola = nuevo
        else:
            nuevo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo
            self.cabeza = nuevo
        self.size += 1

    def insertar_en_posicion(self, libro: Libro, pos: int):
        if pos <= 0:
            self.insertar_inicio(libro)
            return
        if pos >= self.size:
            self.insertar_final(libro)
            return
        
        nuevo = Nodo(libro)
        actual = self.cabeza
        for _ in range(pos - 1):
            actual = actual.siguiente
        
        nuevo.siguiente = actual.siguiente
        nuevo.anterior = actual
        actual.siguiente.anterior = nuevo
        actual.siguiente = nuevo
        self.size += 1

    def obtener_todos(self) -> List[dict]:
        actual = self.cabeza
        libros = []
        while actual:
            libros.append(actual.dato.to_dict())
            actual = actual.siguiente
        return libros

    def buscar_isbn(self, isbn: str) -> Optional[Nodo]:
        actual = self.cabeza
        while actual:
            if actual.dato.isbn == isbn:
                return actual
            actual = actual.siguiente
        return None

    def eliminar(self, isbn: str) -> bool:
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
                self.size -= 1
                return True
            actual = actual.siguiente
        return False

    def guardar_en_archivo(self):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(self.obtener_todos(), f, indent=4)

    def cargar_desde_archivo(self):
        if os.path.exists(DB_FILE):
            try:
                with open(DB_FILE, "r", encoding="utf-8") as f:
                    libros = json.load(f)
                    for l in libros:
                        self.insertar_final(Libro(**l))
            except:
                pass

# --- Inicialización ---
biblioteca = ListaDoble()
biblioteca.cargar_desde_archivo()

# --- Endpoints ---

@app.get("/api/libros")
async def listar_libros():
    return biblioteca.obtener_todos()

@app.post("/api/libros")
async def agregar_libro(data: dict = Body(...)):
    ano = str(data.get("ano", ""))
    isbn = str(data.get("isbn", ""))

    if not (ano.isdigit() and isbn.isdigit()):
        raise HTTPException(
            status_code=400, 
            detail="El Año y el ISBN deben ser valores numéricos."
        )

    if biblioteca.buscar_isbn(isbn):
        raise HTTPException(status_code=400, detail="El ISBN ya está registrado.")
    
    nuevo_libro = Libro(
        titulo=data.get("titulo"), autor=data.get("autor"),
        ano=ano, isbn=isbn, categoria=data.get("categoria")
    )
    
    posicion = data.get("posicion", "final")
    if posicion == "inicio":
        biblioteca.insertar_inicio(nuevo_libro)
    elif posicion == "medio":
        idx = int(data.get("index", 0))
        biblioteca.insertar_en_posicion(nuevo_libro, idx)
    else:
        biblioteca.insertar_final(nuevo_libro)
        
    biblioteca.guardar_en_archivo()
    return {"status": "success", "mensaje": "Libro enlazado", "pos": posicion}

@app.delete("/api/libros/{isbn}")
async def eliminar_libro(isbn: str):
    if biblioteca.eliminar(isbn):
        biblioteca.guardar_en_archivo()
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="No encontrado")

# --- Archivos Estáticos ---
if not os.path.exists("static"): os.makedirs("static")
app.mount("/", StaticFiles(directory="static", html=True), name="static")
@app.get("/")
async def root(): return FileResponse("static/index.html")
