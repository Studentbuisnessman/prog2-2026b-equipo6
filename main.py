"""Interfaz sencilla por terminal para el control de acceso simulado."""

from modelo import Administrador, Servidor, Usuario
from sistema import SistemaAccesos, cargar, guardar


ARCHIVO = "registros.txt"

REQUISITOS_SERVIDOR = (
    "Nombre del servidor: 2 a 30 caracteres. Usa letras de a-z o A-Z, "
    "dígitos, guion o guion bajo e incluye al menos una letra o un dígito."
)


def pedir_cuenta():
    """Pide los datos del tipo de cuenta elegido y construye el objeto."""
    print("\n1. Usuario")
    print("2. Administrador")
    tipo = input("Tipo de cuenta: ").strip()
    if tipo not in ("1", "2"):
        raise ValueError("Elige 1 para usuario o 2 para administrador.")

    print("Cada persona debe registrarse con un nombre completo único.")
    print("Nombre completo: 4 a 60 caracteres. Solo letras y espacios.")
    if tipo == "1":
        print("Área: 2 a 60 caracteres. Solo letras y espacios.")
    else:
        print("Nivel de privilegio: número entero del 1 al 3.")

    print("La longitud del texto se mide sin los espacios de los extremos.")
    nombre = input("Nombre completo: ")
    if tipo == "1":
        return Usuario(nombre, input("Área: "))
    return Administrador(nombre, input("Nivel de privilegio: "))


def pedir_servidor():
    """Muestra los requisitos y pide los datos del servidor."""
    print("\n" + REQUISITOS_SERVIDOR)
    print("IPv4: cuatro bloques de 0 a 255 separados por puntos, sin ceros iniciales.")
    print("Cupo de sesiones: número entero mayor que cero.")
    nombre = input("Nombre del servidor: ")
    ip = input("Dirección IPv4: ")
    cupo = input("Cupo de sesiones: ")
    return Servidor(nombre, ip, cupo)


def main():
    """Carga registros, muestra el menú y procesa las opciones del usuario."""
    sistema = SistemaAccesos()
    try:
        cargar(sistema, ARCHIVO)
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
                sistema.registrar(pedir_cuenta())
                guardar(sistema, ARCHIVO)
                print("Cuenta registrada correctamente.")

            elif opcion == "2":
                sistema.registrar(pedir_servidor())
                guardar(sistema, ARCHIVO)
                print("Servidor registrado correctamente.")

            elif opcion == "3":
                print(REQUISITOS_SERVIDOR)
                print("Usa una cuenta y un servidor registrados, con cupo disponible.")
                print("Cada cuenta puede tener un acceso por servidor.")
                nombre = input("Nombre completo registrado: ")
                nombre_servidor = input("Nombre del servidor: ")
                sistema.asignar(nombre, nombre_servidor)
                guardar(sistema, ARCHIVO)
                print("Acceso asignado correctamente.")

            elif opcion == "4":
                sistema.listar()

            elif opcion == "5":
                guardar(sistema, ARCHIVO)
                print("Datos guardados correctamente.")

            elif opcion == "6":
                guardar(sistema, ARCHIVO)
                print("Datos guardados. Hasta luego.")
                break

            else:
                print("Opción inválida: elige un número del 1 al 6.")

        except ValueError as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
