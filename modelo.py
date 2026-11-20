"""Clases y validaciones del control de acceso simulado a servidores."""


def validar_texto(valor, campo, minimo=2, maximo=60):
    """Valida un nombre compuesto únicamente por letras y espacios."""
    if not isinstance(valor, str):
        raise ValueError(f"{campo} debe ser texto, no otro tipo de dato.")
    if valor == "":
        raise ValueError(f"{campo} no puede estar vacío.")
    if not valor.strip():
        raise ValueError(f"{campo} no puede contener solo espacios.")

    if "\n" in valor or "\r" in valor or "|" in valor:
        raise ValueError(f"{campo} contiene caracteres inválidos.")

    texto = valor.strip()
    if len(texto) < minimo:
        raise ValueError(f"{campo} debe tener al menos {minimo} caracteres.")
    if len(texto) > maximo:
        raise ValueError(f"{campo} no puede superar {maximo} caracteres.")
    if any(caracter.isdigit() for caracter in texto):
        raise ValueError(f"{campo} no puede contener números; usa letras y espacios.")
    if not all(caracter.isalpha() or caracter == " " for caracter in texto):
        raise ValueError(
            f"{campo} contiene caracteres inválidos; usa letras y espacios."
        )
    return texto


def validar_cuenta(valor):
    """Valida el identificador de cuenta: 3 a 16 caracteres permitidos."""
    if not isinstance(valor, str):
        raise ValueError("La cuenta debe ser texto.")
    if valor == "":
        raise ValueError("La cuenta no puede estar vacía.")
    if not valor.strip():
        raise ValueError("La cuenta no puede contener solo espacios.")
    if len(valor) < 3:
        raise ValueError("La cuenta debe tener al menos 3 caracteres.")
    if len(valor) > 16:
        raise ValueError("La cuenta no puede superar 16 caracteres.")
    if valor[0] not in "abcdefghijklmnopqrstuvwxyz":
        raise ValueError("La cuenta debe comenzar con una letra minúscula (a-z).")
    for caracter in valor:
        if caracter not in "abcdefghijklmnopqrstuvwxyz0123456789_":
            raise ValueError(
                "La cuenta contiene caracteres inválidos: usa minúsculas, "
                "números y guion bajo, sin espacios."
            )
    return valor


def validar_nombre_servidor(valor):
    """Valida un nombre de servidor de 2 a 30 caracteres."""
    if not isinstance(valor, str):
        raise ValueError("El servidor debe tener un nombre de tipo texto.")
    if valor == "":
        raise ValueError("El nombre del servidor no puede estar vacío.")
    if not valor.strip():
        raise ValueError("El nombre del servidor no puede contener solo espacios.")
    if len(valor) < 2:
        raise ValueError("El nombre del servidor debe tener al menos 2 caracteres.")
    if len(valor) > 30:
        raise ValueError("El nombre del servidor no puede superar 30 caracteres.")
    permitidos = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    if not any(caracter.isalnum() for caracter in valor):
        raise ValueError(
            "El nombre del servidor debe contener al menos una letra o un número."
        )
    if any(caracter not in permitidos for caracter in valor):
        raise ValueError(
            "El nombre del servidor contiene caracteres inválidos: "
            "usa letras, números, guion o guion bajo, sin espacios."
        )
    return valor


def validar_entero(valor, campo, minimo=1, maximo=None):
    """Convierte dígitos a entero y explica los errores de tipo o rango."""
    if type(valor) is int:
        numero = valor
    elif isinstance(valor, str):
        if valor == "":
            raise ValueError(f"{campo} no puede estar vacío.")
        if not valor.strip():
            raise ValueError(f"{campo} no puede contener solo espacios.")
        texto = valor.strip()
        if texto.startswith("-") and texto[1:].isascii() and texto[1:].isdigit():
            numero = int(texto)
        elif texto.isascii() and texto.isdigit():
            numero = int(texto)
        elif texto.replace(" ", "").isalpha():
            raise ValueError(
                f"{campo} no puede ser texto: escribe un número entero, "
                "por ejemplo 2."
            )
        elif "." in texto or "," in texto:
            raise ValueError(f"{campo} no acepta decimales: escribe un entero.")
        else:
            raise ValueError(
                f"{campo} contiene caracteres inválidos: usa solo dígitos."
            )
    else:
        raise ValueError(f"{campo} debe ser un número entero, no otro tipo de dato.")

    if numero < minimo:
        raise ValueError(f"{campo} debe ser como mínimo {minimo}.")
    if maximo is not None and numero > maximo:
        raise ValueError(f"{campo} debe ser como máximo {maximo}.")
    return numero


def validar_ip(valor):
    """Valida una dirección IPv4 escrita como cuatro números decimales."""
    if not isinstance(valor, str):
        raise ValueError(
            "La IP debe ser texto con formato IPv4, por ejemplo 192.168.1.10."
        )
    if valor == "":
        raise ValueError("La IP no puede estar vacía.")
    if not valor.strip():
        raise ValueError("La IP no puede contener solo espacios.")
    partes = valor.split(".")
    if len(partes) != 4:
        raise ValueError("La IP debe contener cuatro números separados por puntos.")
    for parte in partes:
        if parte == "":
            raise ValueError("La IP tiene un bloque vacío entre puntos.")
        if not parte.isascii() or not parte.isdigit():
            raise ValueError(
                "La IP contiene caracteres inválidos: usa solo números y puntos."
            )
        if len(parte) > 1 and parte.startswith("0"):
            raise ValueError("La IP no debe tener ceros iniciales en sus bloques.")
        if int(parte) > 255:
            raise ValueError("Cada bloque de la IP debe estar entre 0 y 255.")
    return valor


class CuentaAcceso:
    """Representa los datos comunes de una cuenta."""

    def __init__(self, cuenta, nombre):
        """Valida y guarda el identificador y el nombre de la cuenta."""
        self.__cuenta = validar_cuenta(cuenta)
        self.__nombre = validar_texto(nombre, "El nombre")

    def obtener_cuenta(self):
        """Devuelve el identificador sin permitir modificarlo directamente."""
        return self.__cuenta

    def obtener_nombre(self):
        """Devuelve el nombre registrado."""
        return self.__nombre

    def describir(self):
        """Devuelve la descripción común de la cuenta."""
        return f"{self.__cuenta} - {self.__nombre}"


class Usuario(CuentaAcceso):
    """Representa una cuenta de usuario de un área."""

    def __init__(self, cuenta, nombre, area):
        """Valida los datos y guarda el área del usuario."""
        super().__init__(cuenta, nombre)
        self.__area = validar_texto(area, "El área")

    def obtener_area(self):
        """Devuelve el área del usuario."""
        return self.__area

    def describir(self):
        """Describe un usuario con su área."""
        return f"Usuario: {super().describir()} | Área: {self.__area}"


class Administrador(CuentaAcceso):
    """Representa una cuenta con privilegios administrativos."""

    def __init__(self, cuenta, nombre, nivel_privilegio):
        """Valida los datos y el nivel de privilegio del administrador."""
        super().__init__(cuenta, nombre)
        self.__nivel_privilegio = validar_entero(
            nivel_privilegio, "El nivel de privilegio", 1, 3
        )

    def obtener_nivel_privilegio(self):
        """Devuelve el nivel de privilegio del administrador."""
        return self.__nivel_privilegio

    def describir(self):
        """Describe un administrador con su nivel."""
        return (
            f"Administrador: {super().describir()} "
            f"| Nivel: {self.__nivel_privilegio}"
        )


class Servidor:
    """Representa un servidor con un cupo máximo de sesiones."""

    def __init__(self, nombre, ip, cupo):
        """Valida los datos y comienza con cero sesiones."""
        self.__nombre = validar_nombre_servidor(nombre)
        self.__ip = validar_ip(ip)
        self.__cupo = validar_entero(cupo, "El cupo", 1)
        self.__sesiones = []

    def obtener_nombre(self):
        """Devuelve el nombre del servidor."""
        return self.__nombre

    def obtener_ip(self):
        """Devuelve la dirección IPv4 del servidor."""
        return self.__ip

    def obtener_cupo(self):
        """Devuelve la capacidad del servidor sin modificarla."""
        return self.__cupo

    def obtener_sesiones(self):
        """Devuelve una tupla de sesiones que no admite append ni remove."""
        return tuple(self.__sesiones)

    def dar_acceso(self, cuenta):
        """Asigna una cuenta validada sin repetirla ni superar el cupo."""
        cuenta = validar_cuenta(cuenta)
        if cuenta in self.__sesiones:
            raise ValueError(
                f"La cuenta '{cuenta}' ya tiene acceso a '{self.__nombre}'."
            )
        if len(self.__sesiones) >= self.__cupo:
            raise ValueError(f"El servidor '{self.__nombre}' ya alcanzó su cupo.")
        self.__sesiones.append(cuenta)

    def resumen(self):
        """Describe el servidor y su ocupación actual."""
        return (
            f"{self.__nombre} ({self.__ip}) - "
            f"{len(self.__sesiones)}/{self.__cupo} sesiones"
        )
