"""Registro, asignación y persistencia en texto plano del sistema."""

from modelo import Usuario, Administrador, Servidor


class SistemaAccesos:
    """Coordina el registro de cuentas y sus asignaciones a servidores."""

    def __init__(self):
        """Inicia los registros de cuentas y servidores vacíos."""
        self._cuentas = {}
        self._servidores = {}

    def registrar(self, objeto):
        """Registra un Usuario o Administrador si su cuenta es única."""
        if not isinstance(objeto, (Usuario, Administrador)):
            raise ValueError("Solo se pueden registrar usuarios o administradores.")
        if objeto.cuenta in self._cuentas:
            raise ValueError(f"La cuenta '{objeto.cuenta}' ya está registrada.")
        self._cuentas[objeto.cuenta] = objeto

    def registrar_servidor(self, servidor):
        """Agrega un servidor nuevo al sistema."""
        if not isinstance(servidor, Servidor):
            raise ValueError("Solo se pueden agregar objetos de tipo Servidor.")
        if servidor.nombre in self._servidores:
            raise ValueError(f"El servidor '{servidor.nombre}' ya está registrado.")
        self._servidores[servidor.nombre] = servidor

    def asignar(self, identificador, clave):
        """Asigna una cuenta registrada al servidor indicado por su nombre."""
        if identificador not in self._cuentas:
            raise ValueError(f"La cuenta '{identificador}' no está registrada.")
        if clave not in self._servidores:
            raise ValueError(f"El servidor '{clave}' no existe.")
        self._servidores[clave].dar_acceso(identificador)

    def listar(self):
        """Imprime las cuentas, los servidores y sus sesiones registradas."""
        if not self._cuentas and not self._servidores:
            print("No hay registros.")
            return

        print("\nCUENTAS:")
        if not self._cuentas:
            print("No hay cuentas registradas.")
        else:
            for cuenta in self._cuentas.values():
                print("-", cuenta.describir())

        print("\nSERVIDORES:")
        if not self._servidores:
            print("No hay servidores registrados.")
        else:
            for servidor in self._servidores.values():
                print("-", servidor.resumen())
                if servidor.sesiones:
                    print("  Accesos:", ", ".join(servidor.sesiones))
                else:
                    print("  Sin accesos asignados.")

    def guardar(sistema, ruta):
        """Ofrece el método del contrato y delega la escritura del TXT."""
        guardar(sistema, ruta)

    def cargar(sistema, ruta):
        """Ofrece el método del contrato y delega la lectura del TXT."""
        cargar(sistema, ruta)


def guardar(sistema, ruta):
    """Escribe las cuentas, servidores y accesos en un archivo de texto."""
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            for cuenta in sistema._cuentas.values():
                if isinstance(cuenta, Usuario):
                    archivo.write(
                        f"USUARIO|{cuenta.cuenta}|{cuenta.nombre}|{cuenta.area}\n"
                    )
                else:
                    archivo.write(
                        f"ADMINISTRADOR|{cuenta.cuenta}|{cuenta.nombre}|"
                        f"{cuenta.nivel_privilegio}\n"
                    )

            for servidor in sistema._servidores.values():
                archivo.write(
                    f"SERVIDOR|{servidor.nombre}|{servidor.ip}|{servidor.cupo}\n"
                )
                for cuenta in servidor.sesiones:
                    archivo.write(f"ACCESO|{cuenta}|{servidor.nombre}\n")
    except OSError as error:
        raise ValueError(f"No se pudieron guardar los datos: {error}") from error


def cargar(sistema, ruta):
    """Lee registros de un TXT y reconstruye las cuentas y servidores."""
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
    except FileNotFoundError:
        sistema._cuentas = {}
        sistema._servidores = {}
        return
    except OSError as error:
        raise ValueError(f"No se pudieron leer los datos: {error}") from error

    temporal = SistemaAccesos()
    accesos_pendientes = []

    for numero, linea in enumerate(lineas, start=1):
        if not linea.strip():
            continue
        partes = linea.rstrip("\n\r").split("|")
        tipo = partes[0]

        if tipo == "USUARIO" and len(partes) == 4:
            temporal.registrar(Usuario(partes[1], partes[2], partes[3]))
        elif tipo == "ADMINISTRADOR" and len(partes) == 4:
            if not partes[3].isascii() or not partes[3].isdigit():
                raise ValueError(f"Línea {numero}: nivel de privilegio inválido.")
            temporal.registrar(
                Administrador(partes[1], partes[2], int(partes[3]))
            )
        elif tipo == "SERVIDOR" and len(partes) == 4:
            if not partes[3].isascii() or not partes[3].isdigit():
                raise ValueError(f"Línea {numero}: cupo inválido.")
            temporal.registrar_servidor(
                Servidor(partes[1], partes[2], int(partes[3]))
            )
        elif tipo == "ACCESO" and len(partes) == 3:
            accesos_pendientes.append((partes[1], partes[2]))
        else:
            raise ValueError(f"Línea {numero}: registro desconocido o incompleto.")

    for cuenta, servidor in accesos_pendientes:
        temporal.asignar(cuenta, servidor)

    sistema._cuentas = temporal._cuentas
    sistema._servidores = temporal._servidores
