class Producto:
    """
    Representa un producto en el inventario.
    """
    def __init__(self, id, nombre, precio, cantidad):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def __repr__(self):
        """
        Representación en cadena de un objeto Producto.
        """
        return f"ID: {self.id}, Nombre: {self.nombre}, Precio: ${self.precio:.2f}, Cantidad: {self.cantidad}"

class Inventario:
    """
    Gestiona el inventario de productos.
    """
    def __init__(self):
        self.productos = []
        self._proximo_id = 1

    def agregar_producto(self, nombre, precio, cantidad):
        """
        Agrega un nuevo producto al inventario.
        """
        producto = Producto(self._proximo_id, nombre, precio, cantidad)
        self.productos.append(producto)
        self._proximo_id += 1
        print(f"Producto '{nombre}' agregado exitosamente.")

    def eliminar_producto(self, id_producto):
        """
        Elimina un producto del inventario por su ID.
        """
        producto_a_eliminar = self.busqueda_lineal(id_producto, 'id')
        if producto_a_eliminar:
            self.productos.remove(producto_a_eliminar)
            print(f"Producto con ID {id_producto} eliminado.")
        else:
            print(f"Error: No se encontró un producto con ID {id_producto}.")

    def modificar_producto(self, id_producto, nuevo_nombre, nuevo_precio, nueva_cantidad):
        """
        Modifica los atributos de un producto existente.
        """
        producto = self.busqueda_lineal(id_producto, 'id')
        if producto:
            if nuevo_nombre:
                producto.nombre = nuevo_nombre
            if nuevo_precio is not None:
                producto.precio = nuevo_precio
            if nueva_cantidad is not None:
                producto.cantidad = nueva_cantidad
            print(f"Producto con ID {id_producto} modificado.")
        else:
            print(f"Error: No se encontró un producto con ID {id_producto}.")

    def mostrar_productos(self, lista_a_mostrar=None):
        """
        Muestra todos los productos en el inventario.
        """
        lista = lista_a_mostrar if lista_a_mostrar is not None else self.productos
        print("\n--- Inventario Actual ---")
        if not lista:
            print("El inventario está vacío.")
        else:
            for producto in lista:
                print(producto)
        print("-------------------------")

    # --- Algoritmos de Búsqueda ---

    def busqueda_lineal(self, valor, atributo='id'):
        for producto in self.productos:
            if str(getattr(producto, atributo)).lower() == str(valor).lower():
                return producto
        return None

    def busqueda_binaria(self, valor, atributo='id'):
        copia_ordenada = self._quicksort(list(self.productos), atributo)
        izquierda, derecha = 0, len(copia_ordenada) - 1
        while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            valor_medio = getattr(copia_ordenada[medio], atributo)
            if valor_medio == valor:
                return copia_ordenada[medio]
            elif valor_medio < valor:
                izquierda = medio + 1
            else:
                derecha = medio - 1
        return None

    # --- Algoritmos de Ordenamiento ---

    def ordenar_productos(self, atributo, algoritmo='quicksort'):
        if algoritmo.lower() == 'quicksort':
            self.productos = self._quicksort(self.productos, atributo)
        elif algoritmo.lower() == 'mergesort':
            self.productos = self._mergesort(self.productos, atributo)
        else:
            print("Error: Algoritmo no válido.")
            return
        print(f"Inventario ordenado por '{atributo}' usando {algoritmo.capitalize()}.")

    def _quicksort(self, lista, atributo):
        if len(lista) <= 1: return lista
        pivote = lista[len(lista) // 2]
        menores = [p for p in lista if getattr(p, atributo) < getattr(pivote, atributo)]
        iguales = [p for p in lista if getattr(p, atributo) == getattr(pivote, atributo)]
        mayores = [p for p in lista if getattr(p, atributo) > getattr(pivote, atributo)]
        return self._quicksort(menores, atributo) + iguales + self._quicksort(mayores, atributo)

    def _mergesort(self, lista, atributo):
        if len(lista) <= 1: return lista
        medio = len(lista) // 2
        izquierda = self._mergesort(lista[:medio], atributo)
        derecha = self._mergesort(lista[medio:], atributo)
        return self._merge(izquierda, derecha, atributo)

    def _merge(self, izquierda, derecha, atributo):
        resultado = []
        idx_izq, idx_der = 0, 0
        while idx_izq < len(izquierda) and idx_der < len(derecha):
            if getattr(izquierda[idx_izq], atributo) < getattr(derecha[idx_der], atributo):
                resultado.append(izquierda[idx_izq]); idx_izq += 1
            else:
                resultado.append(derecha[idx_der]); idx_der += 1
        resultado.extend(izquierda[idx_izq:]); resultado.extend(derecha[idx_der:])
        return resultado


def mostrar_menu():
    """Imprime el menú de opciones."""
    print("\n===== Sistema de Gestión de Inventario =====")
    print("1. Agregar producto")
    print("2. Eliminar producto")
    print("3. Modificar producto")
    print("4. Ordenar inventario")
    print("5. Mostrar todo el inventario")
    print("6. Salir")
    print("==========================================")

def main():
    """Función principal que ejecuta el menú interactivo."""
    inventario = Inventario()
    
    # Agregar datos iniciales para demostración
    inventario.agregar_producto("Fideos", 1200.50, 10)
    inventario.agregar_producto("Harina", 1225.00, 50)
    inventario.agregar_producto("Aceite", 3075.99, 30)
    inventario.agregar_producto("Azucar", 1300.00, 20)

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            try:
                nombre = input("Ingrese nombre del producto: ")
                precio = float(input("Ingrese precio del producto: "))
                cantidad = int(input("Ingrese cantidad del producto: "))
                inventario.agregar_producto(nombre, precio, cantidad)
            except ValueError:
                print("Error: El precio y la cantidad deben ser números.")

        elif opcion == '2':
            try:
                id_prod = int(input("Ingrese el ID del producto a eliminar: "))
                inventario.eliminar_producto(id_prod)
            except ValueError:
                print("Error: El ID debe ser un número.")

        elif opcion == '3':
            try:
                id_prod = int(input("Ingrese el ID del producto a modificar: "))
                producto = inventario.busqueda_lineal(id_prod)
                if producto:
                    print(f"Modificando producto: {producto}")
                    nuevo_nombre = input(f"Nuevo nombre (dejar en blanco para no cambiar): ") or producto.nombre
                    nuevo_precio_str = input(f"Nuevo precio (dejar en blanco para no cambiar): ")
                    nuevo_cantidad_str = input(f"Nueva cantidad (dejar en blanco para no cambiar): ")

                    nuevo_precio = float(nuevo_precio_str) if nuevo_precio_str else producto.precio
                    nueva_cantidad = int(nuevo_cantidad_str) if nuevo_cantidad_str else producto.cantidad
                    
                    inventario.modificar_producto(id_prod, nuevo_nombre, nuevo_precio, nueva_cantidad)
                else:
                    print("Error: No se encontró un producto con ese ID.")
            except ValueError:
                print("Error: Ingrese valores válidos.")
        
        elif opcion == '4':
            atributo = input("Ordenar por 'id', 'nombre', 'precio' o 'cantidad': ").lower()
            if atributo not in ['id', 'nombre', 'precio', 'cantidad']:
                print("Atributo no válido.")
                continue
            
            algoritmo = input("Usar 'quicksort' o 'mergesort': ").lower()
            if algoritmo in ['quicksort', 'mergesort']:
                inventario.ordenar_productos(atributo, algoritmo)
                inventario.mostrar_productos()
            else:
                print("Algoritmo no válido.")

        elif opcion == '5':
            inventario.mostrar_productos()

        elif opcion == '6':
            print("Saliendo del sistema. ¡Hasta pronto!")
            break

        else:
            print("Opción no válida. Por favor, intente de nuevo.")


# --- Punto de Entrada del Programa ---
if __name__ == "__main__":
    main()