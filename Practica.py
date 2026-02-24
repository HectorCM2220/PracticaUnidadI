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

    def __init__(self, titulo, autor, ano, isbn, categoria):
        """
        Inicializa un objeto Libro con sus atributos básicos.

        Args:
            titulo (str): Título del libro.
            autor (str): Autor del libro.
            ano (str): Año de publicación.
            isbn (str): Código ISBN único.
            categoria (str): Categoría o género del libro.
        """
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.isbn = isbn
        self.categoria = categoria

    def __str__(self):
        """
        Devuelve una representación en cadena del libro.

        Returns:
            str: Cadena con los datos del libro.
        """
        return (
            f"{self.titulo} | {self.autor} | {self.ano} | "
            f"ISBN: {self.isbn} | {self.categoria}"
        )


class Nodo:
    """
    Clase que representa un nodo dentro de la lista doblemente enlazada.

    Atributos:
        dato (Libro): Objeto Libro almacenado en el nodo.
        siguiente (Nodo): Referencia al siguiente nodo.
        anterior (Nodo): Referencia al nodo anterior.
    """

    def __init__(self, dato):
        """
        Inicializa un nodo con un libro y referencias vacías.

        Args:
            dato (Libro): Objeto libro a almacenar en el nodo.
        """
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

    # --------- CREATE ----------
    def insertar_final(self, libro):
        """
        Inserta un libro al final de la lista.

        Args:
            libro (Libro): Objeto libro a insertar.
        """
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
        """Recorre y muestra los libros desde la cabeza hacia la cola."""
        actual = self.cabeza
        if actual is None:
            print("Biblioteca vacía")
            return
        while actual:
            print(actual.dato)
            actual = actual.siguiente

    def recorrer_atras(self):
        """Recorre y muestra los libros desde la cola hacia la cabeza."""
        actual = self.cola
        if actual is None:
            print("Biblioteca vacía")
            return
        while actual:
            print(actual.dato)
            actual = actual.anterior

    def buscar_isbn(self, isbn):
        """
        Busca un libro por su ISBN.

        Args:
            isbn (str): Código ISBN a buscar.

        Returns:
            Nodo | None: Nodo que contiene el libro encontrado o None.
        """
        actual = self.cabeza
        while actual:
            if actual.dato.isbn == isbn:
                return actual
            actual = actual.siguiente
        return None

    def buscar_autor_categoria(self, texto):
        """
        Busca libros por autor o categoría.

        Args:
            texto (str): Texto a comparar con autor o categoría.

        Returns:
            list: Lista de libros encontrados.
        """
        actual = self.cabeza
        encontrados = []
        while actual:
            if (
                actual.dato.autor.lower() == texto.lower()
                or actual.dato.categoria.lower() == texto.lower()
            ):
                encontrados.append(actual.dato)
            actual = actual.siguiente
        return encontrados

    def actualizar(self, isbn, titulo, autor, ano, categoria):
        """
        Actualiza los datos de un libro existente.

        Args:
            isbn (str): ISBN del libro a actualizar.
            titulo (str): Nuevo título.
            autor (str): Nuevo autor.
            ano (str): Nuevo año de publicación.
            categoria (str): Nueva categoría.
        """
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
        """
        Elimina un libro de la lista por su ISBN.

        Args:
            isbn (str): Código ISBN del libro a eliminar.
        """
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
    """Muestra el menú principal de opciones."""
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


# Ejecución principal
biblioteca = ListaDoble()

while True:
    menu()
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        titulo = input("Título: ")
        autor = input("Autor: ")
        ano = input("Año de publicación: ")
        isbn = input("ISBN: ")
        categoria = input("Categoría: ")
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
        texto = input("Autor o categoría: ")
        resultados = biblioteca.buscar_autor_categoria(texto)
        if resultados:
            for libro in resultados:
                print(libro)
        else:
            print("No se encontraron libros")

    elif opcion == "6":
        isbn = input("ISBN del libro a actualizar: ")
        titulo = input("Nuevo título: ")
        autor = input("Nuevo autor: ")
        ano = input("Nuevo año: ")
        categoria = input("Nueva categoría: ")
        biblioteca.actualizar(isbn, titulo, autor, ano, categoria)

    elif opcion == "7":
        isbn = input("ISBN del libro a eliminar: ")
        biblioteca.eliminar(isbn)

    elif opcion == "0":
        print("Saliendo")
        break

    else:
        print("Opción inválida")
