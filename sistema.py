"""Reglas del sistema y funciones sencillas para guardar/cargar un TXT."""

import os

from modelo import (
    Administrador,
    Servidor,
    Usuario,
    validar_cuenta,
    validar_nombre_servidor,
)


class SistemaAccesos:
    """Coordina los registros de cuentas y sus asignaciones a servidores."""

    def __init__(self):
        """Crea las colecciones privadas de cuentas y servidores."""
        self.__cuentas = {}
        self.__servidores = {}

    def registrar(self, objeto):
        """Registra una cuenta o un servidor, evitando identificadores repetidos."""
        if isinstance(objeto, Servidor):
            nombre = objeto.obtener_nombre()
            if nombre in self.__servidores:
                raise ValueError(f"El servidor '{nombre}' ya está registrado.")
            for servidor in self.__servidores.values():
                if servidor.obtener_ip() == objeto.obtener_ip():
                    raise ValueError(
                        f"La IP '{objeto.obtener_ip()}' ya pertenece a otro servidor."
                    )
            self.__servidores[nombre] = objeto
        elif isinstance(objeto, (Usuario, Administrador)):
            cuenta = objeto.obtener_cuenta()
            if cuenta in self.__cuentas:
                raise ValueError(f"La cuenta '{cuenta}' ya está registrada.")
            self.__cuentas[cuenta] = objeto
        else:
            raise ValueError(
                "Solo se pueden registrar objetos Usuario, Administrador o Servidor."
            )

    def asignar(self, identificador, clave):
        """Asigna una cuenta existente al servidor indicado por su nombre."""
        identificador = validar_cuenta(identificador)
        clave = validar_nombre_servidor(clave)
        if identificador not in self.__cuentas:
            raise ValueError(f"La cuenta '{identificador}' no está registrada.")
        if clave not in self.__servidores:
            raise ValueError(f"El servidor '{clave}' no está registrado.")
        self.__servidores[clave].dar_acceso(identificador)

    def listar(self):
        """Imprime cuentas, servidores y accesos o indica si no hay datos."""
        if not self.__cuentas and not self.__servidores:
            print("No hay registros.")
            return

        print("\nCUENTAS:")
        if not self.__cuentas:
            print("No hay cuentas registradas.")
        else:
            for cuenta in self.__cuentas.values():
                print("-", cuenta.describir())

        print("\nSERVIDORES:")
        if not self.__servidores:
            print("No hay servidores registrados.")
        else:
            for servidor in self.__servidores.values():
                print("-", servidor.resumen())
                accesos = servidor.obtener_sesiones()
                if accesos:
                    print("  Accesos:", ", ".join(accesos))
                else:
                    print("  Sin accesos asignados.")

    def obtener_cuentas(self):
        """Devuelve las cuentas para guardar sin exponer el diccionario."""
        return tuple(self.__cuentas.values())

    def obtener_servidores(self):
        """Devuelve los servidores para guardar sin exponer el diccionario."""
        return tuple(self.__servidores.values())

    def reemplazar_registros(self, otro):
        """Sustituye el estado solo después de una carga completa y válida."""
        if not isinstance(otro, SistemaAccesos):
            raise ValueError("Solo puede restaurarse otro SistemaAccesos válido.")
        self.__cuentas = otro.__cuentas.copy()
        self.__servidores = otro.__servidores.copy()

    def guardar(sistema, ruta):
        """Método obligatorio: delega la escritura a guardar_archivo()."""
        guardar_archivo(sistema, ruta)

    def cargar(sistema, ruta):
        """Método obligatorio: delega la lectura a cargar_archivo()."""
        cargar_archivo(sistema, ruta)


def validar_ruta(ruta):
    """Comprueba que la ruta del TXT no sea vacía ni tenga un tipo inválido."""
    if not isinstance(ruta, (str, os.PathLike)):
        raise ValueError("La ruta debe ser texto o una ruta de archivo válida.")
    texto = os.fspath(ruta)
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError(
            "La ruta del archivo no puede estar vacía ni contener solo espacios."
        )
    return ruta


def guardar_archivo(sistema, ruta):
    """Guarda el estado completo como renglones separados por barras."""
    if not isinstance(sistema, SistemaAccesos):
        raise ValueError("El sistema que se desea guardar no es válido.")
    ruta = validar_ruta(ruta)
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            for cuenta in sistema.obtener_cuentas():
                if isinstance(cuenta, Usuario):
                    archivo.write(
                        f"USUARIO|{cuenta.obtener_cuenta()}|"
                        f"{cuenta.obtener_nombre()}|{cuenta.obtener_area()}\n"
                    )
                else:
                    archivo.write(
                        f"ADMINISTRADOR|{cuenta.obtener_cuenta()}|"
                        f"{cuenta.obtener_nombre()}|"
                        f"{cuenta.obtener_nivel_privilegio()}\n"
                    )

            for servidor in sistema.obtener_servidores():
                archivo.write(
                    f"SERVIDOR|{servidor.obtener_nombre()}|"
                    f"{servidor.obtener_ip()}|{servidor.obtener_cupo()}\n"
                )
                for cuenta in servidor.obtener_sesiones():
                    archivo.write(f"ACCESO|{cuenta}|{servidor.obtener_nombre()}\n")
    except (OSError, TypeError, ValueError) as error:
        raise ValueError(f"No se pudieron guardar los datos: {error}") from error


def cargar_archivo(sistema, ruta):
    """Reconstruye los objetos desde el TXT sin aceptar datos incompletos."""
    if not isinstance(sistema, SistemaAccesos):
        raise ValueError("El sistema donde se desea cargar no es válido.")
    ruta = validar_ruta(ruta)
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
    except FileNotFoundError:
        sistema.reemplazar_registros(SistemaAccesos())
        return
    except (OSError, TypeError, UnicodeError) as error:
        raise ValueError(f"No se pudo leer el archivo de datos: {error}") from error

    temporal = SistemaAccesos()
    accesos = []

    for numero, linea in enumerate(lineas, 1):
        if not linea.strip():
            continue
        datos = linea.rstrip("\r\n").split("|")
        tipo = datos[0]
        try:
            if tipo == "USUARIO" and len(datos) == 4:
                temporal.registrar(Usuario(datos[1], datos[2], datos[3]))
            elif tipo == "ADMINISTRADOR" and len(datos) == 4:
                temporal.registrar(Administrador(datos[1], datos[2], datos[3]))
            elif tipo == "SERVIDOR" and len(datos) == 4:
                temporal.registrar(Servidor(datos[1], datos[2], datos[3]))
            elif tipo == "ACCESO" and len(datos) == 3:
                accesos.append((numero, datos[1], datos[2]))
            else:
                raise ValueError(
                    "tipo de registro desconocido o cantidad de campos incorrecta"
                )
        except ValueError as error:
            raise ValueError(f"Línea {numero}: {error}") from error

    for numero, cuenta, nombre_servidor in accesos:
        try:
            temporal.asignar(cuenta, nombre_servidor)
        except ValueError as error:
            raise ValueError(f"Línea {numero}: {error}") from error

    sistema.reemplazar_registros(temporal)


def guardar(sistema, ruta):
    """Permite invocar también el contrato guardar(sistema, ruta)."""
    guardar_archivo(sistema, ruta)


def cargar(sistema, ruta):
    """Permite invocar también el contrato cargar(sistema, ruta)."""
    cargar_archivo(sistema, ruta)
