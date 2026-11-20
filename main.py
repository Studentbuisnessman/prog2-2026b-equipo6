"""Interfaz sencilla por terminal para el control de acceso simulado."""

from modelo import Administrador, Servidor, Usuario
from sistema import SistemaAccesos


ARCHIVO = "registros.txt"


def main():
    """Carga registros, muestra el menú y procesa las opciones del usuario."""
    sistema = SistemaAccesos()
    try:
        sistema.cargar(ARCHIVO)
    except ValueError as error:
        print("Error al cargar el archivo:", error)
        print("Los registros existentes no se modificarán automáticamente.")
        return

    while True:
        print("\n====== CONTROL DE ACCESOS ======")
        print("1. Registrar cuenta")
        print("2. Registrar servidor")
        print("3. Asignar acceso")
        print("4. Listar registros")
        print("5. Guardar datos")
        print("6. Salir")
        opcion = input("Seleccione una opción: ").strip()

        try:
            if opcion == "1":
                tipo = input("Tipo (1=Usuario, 2=Administrador): ").strip()
                if tipo not in ("1", "2"):
                    raise ValueError("Tipo inválido: escribe 1 o 2.")
                cuenta = input("Cuenta: ")
                nombre = input("Nombre: ")
                if tipo == "1":
                    objeto = Usuario(cuenta, nombre, input("Área: "))
                else:
                    nivel = input("Nivel de privilegio (1-3): ")
                    objeto = Administrador(cuenta, nombre, nivel)
                sistema.registrar(objeto)
                sistema.guardar(ARCHIVO)
                print("Cuenta registrada correctamente.")

            elif opcion == "2":
                nombre = input("Nombre del servidor: ")
                ip = input("Dirección IPv4: ")
                cupo = input("Cupo máximo: ")
                sistema.registrar(Servidor(nombre, ip, cupo))
                sistema.guardar(ARCHIVO)
                print("Servidor registrado correctamente.")

            elif opcion == "3":
                cuenta = input("Cuenta: ")
                nombre_servidor = input("Nombre del servidor: ")
                sistema.asignar(cuenta, nombre_servidor)
                sistema.guardar(ARCHIVO)
                print("Acceso asignado correctamente.")

            elif opcion == "4":
                sistema.listar()

            elif opcion == "5":
                sistema.guardar(ARCHIVO)
                print("Datos guardados correctamente.")

            elif opcion == "6":
                sistema.guardar(ARCHIVO)
                print("Datos guardados. Hasta luego.")
                break

            else:
                print("Opción inválida: elige un número del 1 al 6.")

        except ValueError as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
