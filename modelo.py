"""Clases que representan cuentas y servidores de la simulación."""


def validar_texto(valor, campo):
    """Comprueba que un campo de texto pueda guardarse en registros.txt."""
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"{campo} no puede estar vacío y debe ser texto.")
    if "|" in valor or "\n" in valor or "\r" in valor:
        raise ValueError(f"{campo} contiene caracteres no permitidos.")
    return valor.strip()


class CuentaAcceso:
    """Representa los datos compartidos por las cuentas del sistema."""

    def __init__(self, cuenta, nombre):
        """Valida y almacena la cuenta y el nombre de una persona."""
        cuenta = validar_texto(cuenta, "La cuenta")
        nombre = validar_texto(nombre, "El nombre")

        if len(cuenta) < 3 or len(cuenta) > 16:
            raise ValueError("La cuenta debe tener entre 3 y 16 caracteres.")
        if cuenta[0] not in "abcdefghijklmnopqrstuvwxyz":
            raise ValueError("La cuenta debe empezar con una letra minúscula.")
        for caracter in cuenta:
            if caracter not in "abcdefghijklmnopqrstuvwxyz0123456789_":
                raise ValueError("La cuenta solo admite minúsculas, números y guion bajo.")

        self.cuenta = cuenta
        self.nombre = nombre

    def describir(self):
        """Devuelve los datos generales de la cuenta."""
        return f"{self.cuenta} - {self.nombre}"


class Usuario(CuentaAcceso):
    """Representa una cuenta de usuario normal."""

    def __init__(self, cuenta, nombre, area):
        """Crea un usuario con el área a la que pertenece."""
        super().__init__(cuenta, nombre)
        self.area = validar_texto(area, "El área")

    def describir(self):
        """Devuelve la descripción de un usuario con su área."""
        return f"Usuario: {super().describir()} | Área: {self.area}"


class Administrador(CuentaAcceso):
    """Representa una cuenta con nivel administrativo."""

    def __init__(self, cuenta, nombre, nivel_privilegio):
        """Crea un administrador con un nivel de privilegio de 1 a 3."""
        super().__init__(cuenta, nombre)
        if type(nivel_privilegio) is not int or not 1 <= nivel_privilegio <= 3:
            raise ValueError("El nivel de privilegio debe ser un entero entre 1 y 3.")
        self.nivel_privilegio = nivel_privilegio

    def describir(self):
        """Devuelve la descripción de un administrador con su nivel."""
        return (f"Administrador: {super().describir()} "
                f"| Nivel: {self.nivel_privilegio}")


class Servidor:
    """Representa un servidor con cupo limitado de sesiones simuladas."""

    def __init__(self, nombre, ip, cupo):
        """Valida los datos del servidor y comienza sin sesiones."""
        self.nombre = validar_texto(nombre, "El nombre del servidor")
        ip = validar_texto(ip, "La IP")
        partes = ip.split(".")

        if len(partes) != 4:
            raise ValueError("La IP debe tener cuatro números separados por puntos.")
        for parte in partes:
            if not parte.isascii() or not parte.isdigit() or not 0 <= int(parte) <= 255:
                raise ValueError("La dirección IPv4 no es válida.")
        if type(cupo) is not int or cupo <= 0:
            raise ValueError("El cupo del servidor debe ser un entero mayor que cero.")

        self.ip = ip
        self.cupo = cupo
        self.sesiones = []

    def dar_acceso(self, cuenta):
        """Agrega una cuenta si no está repetida y queda cupo disponible."""
        if cuenta in self.sesiones:
            raise ValueError(f"La cuenta '{cuenta}' ya tiene acceso a '{self.nombre}'.")
        if len(self.sesiones) >= self.cupo:
            raise ValueError(f"El servidor '{self.nombre}' ya alcanzó su cupo.")
        self.sesiones.append(cuenta)

    def resumen(self):
        """Devuelve el estado actual del servidor."""
        return (f"{self.nombre} ({self.ip}) - "
                f"{len(self.sesiones)}/{self.cupo} sesiones")
