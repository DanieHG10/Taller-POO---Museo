from abc import ABC, abstractmethod
from enum import Enum

# ENUMERACIONES Y CONSTANTES

class EstadoObra(Enum):
    #Estados posibles de una obra de arte
    EXPUESTA = "Expuesta"
    RESTAURACION = "En Restauración"


class TipoRestauracion(Enum):
    #Tipos de restauración posibles
    MANTENIMIENTO = "Mantenimiento"
    REPARACION = "Reparación"
    RESTAURACION_COMPLETA = "Restauración Completa"


# CLASE ABSTRACTA: USUARIO (Principio D - Dependency Inversion)

class Usuario(ABC):
    #Clase abstracta que define la interfaz para todos los usuarios del sistema.
    
    #Implementa el principio de Inversión de Dependencias: Las clases concretas dependen de esta abstracción.
    
    
    def __init__(self, nombre: str, usuario: str, contraseña: str):
        #Inicializa un usuario con credenciales.
        
        #Args:
            #nombre: Nombre real del usuario
            #usuario: Nombre de usuario (login)
            #contraseña: Contraseña (en producción se encriptaría)

        self.nombre = nombre
        self.usuario = usuario
        self.contraseña = contraseña
    
    def autenticar(self, usuario: str, contraseña: str) -> bool:
        #Autentica al usuario verificando credenciales.
        
        #Args:
            #usuario: Usuario ingresado
            #contraseña: Contraseña ingresada
            
        #Returns:
           # True si las credenciales son correctas, False en caso contrario
        
        return self.usuario == usuario and self.contraseña == contraseña
    
    @abstractmethod
    def obtener_menu(self) -> str:
        #Define qué opciones de menú tiene cada tipo de usuario#
        pass

# USUARIOS CONCRETOS (Polimorfismo)

class EncargadoCatalogo(Usuario):
    #Usuario responsable de introducir datos de obras de arte
    
    def obtener_menu(self) -> str:
        return """
        === MENÚ ENCARGADO DE CATÁLOGO ===
        1. Registrar nuevo cuadro
        2. Registrar nueva escultura
        3. Registrar nuevo objeto
        4. Consultar obras registradas
        5. Salir
        """


class RestauradorJefe(Usuario):
    #Usuario responsable de gestionar restauraciones

    def obtener_menu(self) -> str:
        return """
        === MENÚ RESTAURADOR JEFE ===
        1. Ver obras que necesitan restauración
        2. Iniciar restauración
        3. Finalizar restauración
        4. Consultar historial de restauraciones de una obra
        5. Salir
        """


class Director(Usuario):
    #Usuario responsable de gestionar cesiones y valoraciones
    
    def obtener_menu(self) -> str:
        return """
        === MENÚ DIRECTOR DEL MUSEO ===
        1. Consultar valoración total de obras
        2. Ceder obra a otro museo
        3. Consultar cesiones vigentes
        4. Registrar museo colaborador
        5. Salir
        """


class Visitante(Usuario):
    #Usuario con acceso de solo lectura
    
    def obtener_menu(self) -> str:
        return """
        === MENÚ VISITANTE ===
        1. Consultar obras por sala
        2. Ver detalles de obra
        3. Salir
        """