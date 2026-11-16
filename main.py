"""Menú de terminal para probar el control de acceso simulado."""

from modelo import Usuario, Administrador, Servidor
from sistema import SistemaAccesos


RUTA = "registros.txt"


def main():
    """Muestra el menú y pide los datos necesarios para cada operación."""
    sistema = SistemaAccesos()
    try:
        sistema.cargar(RUTA)
    except ValueError as error:
        print("No se pudieron recuperar los registros:", error)
        print("El sistema iniciará vacío.")

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
                cuenta = input("Cuenta: ")
                nombre = input("Nombre: ")

                if tipo == "1":
                    objeto = Usuario(cuenta, nombre, input("Área: "))
                elif tipo == "2":
                    nivel = input("Nivel de privilegio (1-3): ").strip()
                    if not nivel.isascii() or not nivel.isdigit():
                        raise ValueError("El nivel debe ser un número entre 1 y 3.")
                    objeto = Administrador(cuenta, nombre, int(nivel))
                else:
                    raise ValueError("Tipo de cuenta inválido.")

                sistema.registrar(objeto)
                sistema.guardar(RUTA)
                print("Cuenta registrada correctamente.")

            elif opcion == "2":
                nombre = input("Nombre del servidor: ")
                ip = input("Dirección IPv4: ")
                cupo = input("Cupo máximo: ").strip()
                if not cupo.isascii() or not cupo.isdigit():
                    raise ValueError("El cupo debe ser un número entero positivo.")
                sistema.registrar_servidor(Servidor(nombre, ip, int(cupo)))
                sistema.guardar(RUTA)
                print("Servidor registrado correctamente.")

            elif opcion == "3":
                identificador = input("Cuenta: ").strip()
                clave = input("Nombre del servidor: ").strip()
                sistema.asignar(identificador, clave)
                sistema.guardar(RUTA)
                print("Acceso asignado correctamente.")

            elif opcion == "4":
                sistema.listar()

            elif opcion == "5":
                sistema.guardar(RUTA)
                print(f"Datos guardados en {RUTA}.")

            elif opcion == "6":
                sistema.guardar(RUTA)
                print("Datos guardados. Hasta luego.")
                break

            else:
                print("Opción no válida.")

        except ValueError as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
