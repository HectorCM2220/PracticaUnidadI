
class Libro:
    def __init__(self, titulo, autor, ano, isbn, categoria):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.isbn = isbn
        self.categoria = categoria

    def __str__(self):
        return f"{self.titulo} | {self.autor} | {self.ano} | ISBN: {self.isbn} | {self.categoria}"

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None

class ListaDoble:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    # --------- CREATE ----------
    def insertar_final(self, libro):
        nuevo = Nodo(libro)
        if self.cola is None:
            self.cabeza = self.cola = nuevo
        else:
            nuevo.anterior = self.cola
            self.cola.siguiente = nuevo
            self.cola = nuevo
        print("Libro agregado correctamente")

    # ---------- READ ----------
    def recorrer_adelante(self):
        actual = self.cabeza
        if actual is None:
            print("Biblioteca vacia")
            return
        while actual:
            print(actual.dato)
            actual = actual.siguiente

    def recorrer_atras(self):
        actual = self.cola
        if actual is None:
            print("Biblioteca vacia")
            return
        while actual:
            print(actual.dato)
            actual = actual.anterior

    def buscar_isbn(self, isbn):
        actual = self.cabeza
        while actual:
            if actual.dato.isbn == isbn:
                return actual
            actual = actual.siguiente
        return None

    def buscar_autor_categoria(self, texto):
        actual = self.cabeza
        encontrados = []
        while actual:
            if (actual.dato.autor.lower() == texto.lower() or
                actual.dato.categoria.lower() == texto.lower()):
                encontrados.append(actual.dato)
            actual = actual.siguiente
        return encontrados

    def actualizar(self, isbn, titulo, autor, ano, categoria):
        nodo = self.buscar_isbn(isbn)
        if nodo:
            nodo.dato.titulo = titulo
            nodo.dato.autor = autor
            nodo.dato.ano = ano
            nodo.dato.categoria = categoria
            print("Libro actualizado correctamente")
        else:
            print("Libro no encontrado")

    def eliminar(self, isbn):
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

                print("Libro eliminado")
                return
            actual = actual.siguiente
        print("Libro no encontrado")

def menu():
    print("\n--------------------------------------------")
    print("[1] Agregar libro")
    print("[2] Mostrar libros (orden normal)")
    print("[3] Mostrar libros (orden inverso)")
    print("[4] Buscar libro por ISBN")
    print("[5] Buscar libros por autor o categoría")
    print("[6] Actualizar libro")
    print("[7] Eliminar libro")
    print("[0] Salir")
    print("----------------------------------------------")

biblioteca = ListaDoble()

while True:
    menu()
    opcion = input("Seleccione una opcion: ")

    if opcion == "1":
        titulo = input("Titulo: ")
        autor = input("Autor: ")
        ano = input("Año de publicacion: ")
        isbn = input("ISBN: ")
        categoria = input("Categoria: ")
        biblioteca.insertar_final(Libro(titulo, autor, ano, isbn, categoria))

    elif opcion == "2":
        biblioteca.recorrer_adelante()

    elif opcion == "3":
        biblioteca.recorrer_atras()

    elif opcion == "4":
        isbn = input("ISBN a buscar: ")
        nodo = biblioteca.buscar_isbn(isbn)
        print(nodo.dato if nodo else "Libro no encontrado")

    elif opcion == "5":
        texto = input("Autor o categoria: ")
        resultados = biblioteca.buscar_autor_categoria(texto)
        if resultados:
            for libro in resultados:
                print(libro)
        else:
            print("No se encontraron libros")

    elif opcion == "6":
        isbn = input("ISBN del libro a actualizar: ")
        titulo = input("Nuevo titulo: ")
        autor = input("Nuevo autor: ")
        ano = input("Nuevo año: ")
        categoria = input("Nueva categoria: ")
        biblioteca.actualizar(isbn, titulo, autor, ano, categoria)

    elif opcion == "7":
        isbn = input("ISBN del libro a eliminar: ")
        biblioteca.eliminar(isbn)

    elif opcion == "0":
        print("Saliendo")
        break

    else:
        print("Opcion invalida")