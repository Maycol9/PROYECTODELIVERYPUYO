from inventario.productos import Producto
from inventario.inventario import Inventario


def mostrar_menu():
    print("\n===== DELIVERPUYO - MENÚ INVENTARIO =====")
    print("1. Agregar producto")
    print("2. Eliminar producto")
    print("3. Actualizar producto")
    print("4. Buscar producto por nombre")
    print("5. Mostrar todos los productos")
    print("6. Mostrar categorías únicas")
    print("7. Mostrar resumen de un producto")
    print("0. Salir")


def main():
    inventario = Inventario()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            try:
                id_producto = int(input("ID: "))
                nombre = input("Nombre: ")
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: "))
                categoria = input("Categoría: ")

                producto = Producto(id_producto, nombre, cantidad, precio, categoria)
                if inventario.agregar_producto(producto):
                    print("Producto agregado correctamente.")
                else:
                    print("Ya existe un producto con ese ID.")
            except ValueError:
                print("Datos inválidos.")

        elif opcion == "2":
            try:
                id_producto = int(input("ID a eliminar: "))
                if inventario.eliminar_producto(id_producto):
                    print("Producto eliminado.")
                else:
                    print("Producto no encontrado.")
            except ValueError:
                print("ID inválido.")

        elif opcion == "3":
            try:
                id_producto = int(input("ID a actualizar: "))
                nueva_cantidad = int(input("Nueva cantidad: "))
                nuevo_precio = float(input("Nuevo precio: "))
                if inventario.actualizar_producto(id_producto, nueva_cantidad, nuevo_precio):
                    print("Producto actualizado.")
                else:
                    print("Producto no encontrado.")
            except ValueError:
                print("Datos inválidos.")

        elif opcion == "4":
            nombre = input("Nombre a buscar: ")
            resultados = inventario.buscar_por_nombre(nombre)
            if resultados:
                for producto in resultados:
                    print(producto)
            else:
                print("No se encontraron productos.")

        elif opcion == "5":
            productos = inventario.mostrar_todos()
            if productos:
                for producto in productos:
                    print(producto)
            else:
                print("No hay productos registrados.")

        elif opcion == "6":
            categorias = inventario.obtener_categorias_unicas()
            if categorias:
                print("Categorías:")
                for categoria in categorias:
                    print("-", categoria)
            else:
                print("No hay categorías registradas.")

        elif opcion == "7":
            try:
                id_producto = int(input("ID del producto: "))
                resumen = inventario.resumen_producto(id_producto)
                if resumen:
                    print(f"Nombre: {resumen[0]} | Cantidad: {resumen[1]} | Precio: ${resumen[2]:.2f}")
                else:
                    print("Producto no encontrado.")
            except ValueError:
                print("ID inválido.")

        elif opcion == "0":
            print("Saliendo...")
            break

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()