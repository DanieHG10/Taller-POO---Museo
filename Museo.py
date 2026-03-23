from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional
from enum import Enum
import uuid

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
    

    
    def __init__(self, nombre: str, usuario: str, contraseña: str):
        #Inicializa un usuario con credenciales.
       
        self.nombre = nombre
        self.usuario = usuario
        self.contraseña = contraseña
    
    def autenticar(self, usuario: str, contraseña: str) -> bool:
        #Autentica al usuario verificando credenciales.
        
        
        return self.usuario == usuario and self.contraseña == contraseña
    
    @abstractmethod
    def obtener_menu(self) -> str:
        #Define qué opciones de menú tiene cada tipo de usuario#
        pass

# USUARIOS CONCRETOS 

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


# CLASE ABSTRACTA: OBRA DE ARTE 

class ObraDeArte(ABC):
    # Clase abstracta base para todas las obras de arte del museo.
    #Implementa el principio de Responsabilidad Única: Define la estructura común y comportamiento de cualquier obra.
        
    def __init__(self, id_obra: str, autor: str, periodo: str, 
                 valor: float, fecha_creacion: datetime, fecha_entrada: datetime):
    
        #Inicializa una obra de arte con sus atributos básicos.
        
        self.id_obra = id_obra
        self.autor = autor
        self.periodo = periodo
        self.valor = valor
        self.fecha_creacion = fecha_creacion
        self.fecha_entrada = fecha_entrada
        self.estado = EstadoObra.EXPUESTA
        self.restauraciones: List['Restauracion'] = []
        self.cesion_vigente: Optional['Cesion'] = None
    
    @abstractmethod
    def obtener_info_especifica(self) -> str:
        # Método abstracto que cada subclase implementará con sus atributos únicos.
        pass
    
    def obtener_info_completa(self) -> str:
        #Retorna información completa de la obra
        info = f"""
        === INFORMACIÓN DE LA OBRA ===
        ID: {self.id_obra}
        Autor: {self.autor}
        Período: {self.periodo}
        Valor: ${self.valor:.2f}
        Fecha Creación: {self.fecha_creacion.strftime('%d/%m/%Y')}
        Fecha Entrada: {self.fecha_entrada.strftime('%d/%m/%Y')}
        Estado: {self.estado.value}
        {self.obtener_info_especifica()}
        """
        return info
    
    def enviar_a_restauracion(self, tipo_restauracion: TipoRestauracion) -> 'Restauracion':
        
        #Cambia el estado de la obra a restauración.
       
        self.estado = EstadoObra.RESTAURACION
        restauracion = Restauracion(
            id_restauracion=str(uuid.uuid4()),
            obra=self,
            tipo=tipo_restauracion,
            fecha_inicio=datetime.now()
        )
        self.restauraciones.append(restauracion)
        return restauracion
    
    def finalizar_restauracion(self, restauracion: 'Restauracion') -> bool:
        
        #Finaliza la restauración actual de la obra.
        
        if restauracion in self.restauraciones:
            restauracion.fecha_fin = datetime.now()
            self.estado = EstadoObra.EXPUESTA
            self.cesion_vigente = None  # Se puede exponer nuevamente
            return True
        return False
    
    def obtener_historial_restauraciones(self) -> List['Restauracion']:
        #Retorna el historial de restauraciones ordenado por antigüedad
        return sorted(self.restauraciones, key=lambda r: r.fecha_inicio)
    
    def calcular_dias_desde_ultima_restauracion(self) -> Optional[int]:
        #Calcula días desde la última restauración
        if not self.restauraciones:
            return None
        ultima = self.restauraciones[-1]
        return (datetime.now() - ultima.fecha_fin).days if ultima.fecha_fin else None
    
    def necesita_restauracion_automatica(self) -> bool:
        #Determina si la obra necesita restauración automática (cada 5 años)
        dias_desde_ultima = self.calcular_dias_desde_ultima_restauracion()
        
        # Si nunca ha sido restaurada, usar fecha de entrada
        if dias_desde_ultima is None:
            dias_desde_entrada = (datetime.now() - self.fecha_entrada).days
            return dias_desde_entrada >= (365 * 5)
        
        return dias_desde_ultima >= (365 * 5)
    
    def puede_ser_cedida(self) -> bool:
        """Verifica si la obra puede ser cedida (no está dañada ni en restauración)"""
        return self.estado == EstadoObra.EXPUESTA and self.cesion_vigente is None

# CLASES CONCRETAS DE OBRAS

class Cuadro(ObraDeArte):
    #Obra de arte tipo Cuadro
    
    def __init__(self, id_obra: str, autor: str, periodo: str, valor: float,
                 fecha_creacion: datetime, fecha_entrada: datetime,
                 estilo: str, tecnica: str):
        
        #Inicializa un cuadro con sus atributos específicos.
        
        super().__init__(id_obra, autor, periodo, valor, fecha_creacion, fecha_entrada)
        self.estilo = estilo
        self.tecnica = tecnica
    
    def obtener_info_especifica(self) -> str:
        #Implementa el método abstracto con información específica del cuadro
        return f"""
        --- CUADRO ---
        Estilo: {self.estilo}
        Técnica: {self.tecnica}
        """


class Escultura(ObraDeArte):
    #Obra de arte tipo Escultura
    
    def __init__(self, id_obra: str, autor: str, periodo: str, valor: float,
                 fecha_creacion: datetime, fecha_entrada: datetime,
                 estilo: str, material: str):
        
        #Inicializa una escultura con sus atributos específicos.
        
        super().__init__(id_obra, autor, periodo, valor, fecha_creacion, fecha_entrada)
        self.estilo = estilo
        self.material = material
    
    def obtener_info_especifica(self) -> str:
        #Implementa el método abstracto con información específica de la escultura
        return f"""
        --- ESCULTURA ---
        Estilo: {self.estilo}
        Material: {self.material}
        """


class Objeto(ObraDeArte):
    #Obra de arte tipo Objeto (categoría genérica)
    
    def __init__(self, id_obra: str, autor: str, periodo: str, valor: float,
                 fecha_creacion: datetime, fecha_entrada: datetime,
                 descripcion: str):
        
        #Inicializa un objeto con descripción genérica.
        
        super().__init__(id_obra, autor, periodo, valor, fecha_creacion, fecha_entrada)
        self.descripcion = descripcion
    
    def obtener_info_especifica(self) -> str:
        #Implementa el método abstracto con información específica del objeto
        return f"""
        --- OBJETO ---
        Descripción: {self.descripcion}
        """


# CLASE: RESTAURACIÓN

class Restauracion:
    
    #Representa un proceso de restauración de una obra. Responsabilidad Única: Gestionar solo los datos de una restauración.
   
    def __init__(self, id_restauracion: str, obra: ObraDeArte, 
                 tipo: TipoRestauracion, fecha_inicio: datetime):
        
        self.id_restauracion = id_restauracion
        self.obra = obra
        self.tipo = tipo
        self.fecha_inicio = fecha_inicio
        self.fecha_fin: Optional[datetime] = None
    
    def obtener_info(self) -> str:
        #Retorna información de la restauración
        fecha_fin_str = self.fecha_fin.strftime('%d/%m/%Y') if self.fecha_fin else "En progreso"
        duracion = ""
        if self.fecha_fin:
            dias = (self.fecha_fin - self.fecha_inicio).days
            duracion = f" (Duración: {dias} días)"
        
        return f"""
        ID Restauración: {self.id_restauracion}
        Obra: {self.obra.id_obra}
        Tipo: {self.tipo.value}
        Inicio: {self.fecha_inicio.strftime('%d/%m/%Y')}
        Fin: {fecha_fin_str}{duracion}
        """


# CLASE: CESIÓN DE OBRA

class Cesion:
    #Representa la cesión de una obra a otro museo. Responsabilidad Única: Gestionar los detalles de una cesión.
       
    def __init__(self, id_cesion: str, obra: ObraDeArte, museo_cesionario: str,
                 importe: float, fecha_inicio: datetime, fecha_fin: datetime):
        
        self.id_cesion = id_cesion
        self.obra = obra
        self.museo_cesionario = museo_cesionario
        self.importe = importe
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
    
    def esta_vigente(self) -> bool:
        #Verifica si la cesión está actualmente vigente
        hoy = datetime.now()
        return self.fecha_inicio <= hoy <= self.fecha_fin
    
    def obtener_info(self) -> str:
        
        #Retorna información de la cesión
        vigencia = "Vigente" if self.esta_vigente() else "Finalizada"
        return f"""
        ID Cesión: {self.id_cesion}
        Obra: {self.obra.id_obra}
        Museo Cesionario: {self.museo_cesionario}
        Importe: ${self.importe:.2f}
        Período: {self.fecha_inicio.strftime('%d/%m/%Y')} - {self.fecha_fin.strftime('%d/%m/%Y')}
        Estado: {vigencia}
        """


# CLASE: GESTOR DEL MUSEO

class GestorMuseo:
    
    #Gestor centralizado del museo.
    
    def __init__(self):
        #Inicializa el gestor del museo
        self.obras: List[ObraDeArte] = []
        self.restauraciones: List[Restauracion] = []
        self.cesiones: List[Cesion] = []
        self.museos_colaboradores: List[str] = []
        self.usuario_autenticado: Optional[Usuario] = None
    
    def registrar_cuadro(self, autor: str, periodo: str, valor: float,
                        fecha_creacion: datetime, fecha_entrada: datetime,
                        estilo: str, tecnica: str) -> Cuadro:
        #Registra un nuevo cuadro en el catálogo
        id_obra = str(uuid.uuid4())[:8]
        cuadro = Cuadro(id_obra, autor, periodo, valor, 
                       fecha_creacion, fecha_entrada, estilo, tecnica)
        self.obras.append(cuadro)
        return cuadro
    
    def registrar_escultura(self, autor: str, periodo: str, valor: float,
                           fecha_creacion: datetime, fecha_entrada: datetime,
                           estilo: str, material: str) -> Escultura:
        #Registra una nueva escultura en el catálogo
        id_obra = str(uuid.uuid4())[:8]
        escultura = Escultura(id_obra, autor, periodo, valor,
                             fecha_creacion, fecha_entrada, estilo, material)
        self.obras.append(escultura)
        return escultura
    
    def registrar_objeto(self, autor: str, periodo: str, valor: float,
                        fecha_creacion: datetime, fecha_entrada: datetime,
                        descripcion: str) -> Objeto:
        #Registra un nuevo objeto en el catálogo
        id_obra = str(uuid.uuid4())[:8]
        objeto = Objeto(id_obra, autor, periodo, valor,
                       fecha_creacion, fecha_entrada, descripcion)
        self.obras.append(objeto)
        return objeto
    
    def obtener_obras(self) -> List[ObraDeArte]:
        #Retorna todas las obras registradas
        return self.obras
    
    def obtener_obra_por_id(self, id_obra: str) -> Optional[ObraDeArte]:
        #Busca una obra por su ID
        for obra in self.obras:
            if obra.id_obra == id_obra:
                return obra
        return None
    
    def iniciar_restauracion(self, id_obra: str, 
                            tipo_restauracion: TipoRestauracion) -> Optional[Restauracion]:
        #Inicia una restauración para una obra
        obra = self.obtener_obra_por_id(id_obra)
        if obra:
            restauracion = obra.enviar_a_restauracion(tipo_restauracion)
            self.restauraciones.append(restauracion)
            return restauracion
        return None
    
    def finalizar_restauracion(self, id_obra: str) -> bool:
        #Finaliza la restauración de una obra
        obra = self.obtener_obra_por_id(id_obra)
        if obra and obra.estado == EstadoObra.RESTAURACION:
            # Encontrar la restauración en progreso
            for restauracion in obra.restauraciones:
                if restauracion.fecha_fin is None:
                    obra.finalizar_restauracion(restauracion)
                    return True
        return False
    
    def obtener_obras_para_restauracion_automatica(self) -> List[ObraDeArte]:
        #Retorna obras que necesitan restauración automática
        return [obra for obra in self.obras 
                if obra.estado == EstadoObra.EXPUESTA 
                and obra.necesita_restauracion_automatica()]
    
    def ceder_obra(self, id_obra: str, museo_cesionario: str, 
                   importe: float, fecha_fin: datetime) -> Optional[Cesion]:
        #Cede una obra a otro museo
        obra = self.obtener_obra_por_id(id_obra)
        if obra and obra.puede_ser_cedida() and museo_cesionario in self.museos_colaboradores:
            id_cesion = str(uuid.uuid4())[:8]
            cesion = Cesion(id_cesion, obra, museo_cesionario, importe,
                          datetime.now(), fecha_fin)
            obra.cesion_vigente = cesion
            self.cesiones.append(cesion)
            return cesion
        return None
    
    def registrar_museo_colaborador(self, nombre_museo: str) -> bool:
        #Registra un nuevo museo colaborador
        if nombre_museo not in self.museos_colaboradores:
            self.museos_colaboradores.append(nombre_museo)
            return True
        return False
    
    def obtener_cesiones_vigentes(self) -> List[Cesion]:
        #Retorna todas las cesiones actualmente vigentes
        return [c for c in self.cesiones if c.esta_vigente()]
    
    def calcular_valoracion_total(self) -> float:
        #Calcula la valoración total de todas las obras en el museo
        return sum(obra.valor for obra in self.obras 
                  if obra.estado == EstadoObra.EXPUESTA)


# CLASE: SISTEMA DE AUTENTICACIÓN

class SistemaAutenticacion:
    #Gestiona la autenticación de usuarios.
    
    
    def __init__(self):
        #Inicializa el sistema con usuarios predefinidos
        self.usuarios: List[Usuario] = [
            EncargadoCatalogo("Juan Pérez", "juanperez", "cataimg123"),
            RestauradorJefe("María García", "mariagarcia", "restaur456"),
            Director("Carlos López", "carloslopez", "director789"),
            Visitante("Público General", "visitante", "visitante123")
        ]
    
    def autenticar(self, usuario: str, contraseña: str) -> Optional[Usuario]:
        
        for user in self.usuarios:
            if user.autenticar(usuario, contraseña):
                return user
        return None
    
    def obtener_usuarios_demo(self) -> str:
        #Retorna información de usuarios de demostración
        info = "=== USUARIOS DE DEMOSTRACIÓN ===\n"
        for user in self.usuarios:
            info += f"Usuario: {user.usuario} | Contraseña: {user.contraseña} | Rol: {user.__class__.__name__}\n"
        return info

# INTERFAZ DE USUARIO (MENÚ INTERACTIVO)

def validar_float(mensaje: str, permitir_negativo: bool = False) -> float:
    
    #Valida la entrada de un número decimal.
    
    while True:
        try:
            valor = float(input(mensaje))
            if not permitir_negativo and valor < 0:
                print("❌ Error: El valor no puede ser negativo.")
                continue
            return valor
        except ValueError:
            print("❌ Error: Ingrese un número válido.")


def validar_fecha(mensaje: str) -> datetime:
    
    #Valida la entrada de una fecha.
    
    while True:
        try:
            fecha_str = input(mensaje + " (DD/MM/YYYY): ")
            return datetime.strptime(fecha_str, "%d/%m/%Y")
        except ValueError:
            print("❌ Error: Formato de fecha inválido. Use DD/MM/YYYY")


def menu_registrar_cuadro(gestor: GestorMuseo) -> None:
    #Menú para registrar un nuevo cuadro
    print("\n=== REGISTRAR NUEVO CUADRO ===")
    
    autor = input("Autor: ")
    periodo = input("Período artístico: ")
    valor = validar_float("Valor ($): ")
    fecha_creacion = validar_fecha("Fecha de creación")
    fecha_entrada = validar_fecha("Fecha de entrada al museo")
    estilo = input("Estilo artístico: ")
    tecnica = input("Técnica pictórica: ")
    
    cuadro = gestor.registrar_cuadro(autor, periodo, valor, 
                                     fecha_creacion, fecha_entrada,
                                     estilo, tecnica)
    print(f"\n✅ Cuadro registrado exitosamente con ID: {cuadro.id_obra}")


def menu_registrar_escultura(gestor: GestorMuseo) -> None:
    #Menú para registrar una nueva escultura
    print("\n=== REGISTRAR NUEVA ESCULTURA ===")
    
    autor = input("Autor: ")
    periodo = input("Período artístico: ")
    valor = validar_float("Valor ($): ")
    fecha_creacion = validar_fecha("Fecha de creación")
    fecha_entrada = validar_fecha("Fecha de entrada al museo")
    estilo = input("Estilo artístico: ")
    material = input("Material: ")
    
    escultura = gestor.registrar_escultura(autor, periodo, valor,
                                          fecha_creacion, fecha_entrada,
                                          estilo, material)
    print(f"\n✅ Escultura registrada exitosamente con ID: {escultura.id_obra}")


def menu_registrar_objeto(gestor: GestorMuseo) -> None:
    #Menú para registrar un nuevo objeto
    print("\n=== REGISTRAR NUEVO OBJETO ===")
    
    autor = input("Autor: ")
    periodo = input("Período artístico: ")
    valor = validar_float("Valor ($): ")
    fecha_creacion = validar_fecha("Fecha de creación")
    fecha_entrada = validar_fecha("Fecha de entrada al museo")
    descripcion = input("Descripción del objeto: ")
    
    objeto = gestor.registrar_objeto(autor, periodo, valor,
                                    fecha_creacion, fecha_entrada,
                                    descripcion)
    print(f"\n✅ Objeto registrado exitosamente con ID: {objeto.id_obra}")


def menu_consultar_obras(gestor: GestorMuseo) -> None:
    #Menú para consultar obras registradas
    obras = gestor.obtener_obras()
    
    if not obras:
        print("\n❌ No hay obras registradas.")
        return
    
    print(f"\n=== OBRAS REGISTRADAS ({len(obras)}) ===")
    for i, obra in enumerate(obras, 1):
        print(f"{i}. {obra.id_obra} - {obra.autor} ({obra.__class__.__name__}) - ${obra.valor:.2f}")
    
    print("\n¿Desea ver detalles de alguna obra? (s/n): ", end="")
    if input().lower() == 's':
        id_obra = input("Ingrese el ID de la obra: ")
        obra = gestor.obtener_obra_por_id(id_obra)
        if obra:
            print(obra.obtener_info_completa())
        else:
            print("❌ Obra no encontrada.")


def menu_restaurador_jefe(gestor: GestorMuseo) -> None:
    #Menú interactivo para el Restaurador Jefe
    while True:
        usuario_actual = gestor.usuario_autenticado
        print(usuario_actual.obtener_menu())
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            # Ver obras que necesitan restauración
            obras_a_restaurar = gestor.obtener_obras_para_restauracion_automatica()
            
            if not obras_a_restaurar:
                print("\n✅ No hay obras que requieran restauración automática en este momento.")
            else:
                print(f"\n=== OBRAS QUE NECESITAN RESTAURACIÓN ({len(obras_a_restaurar)}) ===")
                for i, obra in enumerate(obras_a_restaurar, 1):
                    dias = (datetime.now() - obra.fecha_entrada).days
                    print(f"{i}. {obra.id_obra} - {obra.autor} (En museo: {dias // 365} años)")
        
        elif opcion == "2":
            # Iniciar restauración
            if not gestor.obtener_obras():
                print("\n❌ No hay obras registradas.")
                continue
            
            print("\n=== INICIAR RESTAURACIÓN ===")
            obras = gestor.obtener_obras()
            for i, obra in enumerate(obras, 1):
                estado_info = f" ({obra.estado.value})" if obra.estado != EstadoObra.EXPUESTA else ""
                print(f"{i}. {obra.id_obra} - {obra.autor}{estado_info}")
            
            id_obra = input("\nIngrese el ID de la obra a restaurar: ")
            
            print("\nTipos de restauración:")
            for i, tipo in enumerate(TipoRestauracion, 1):
                print(f"{i}. {tipo.value}")
            
            try:
                tipo_idx = int(input("Seleccione el tipo de restauración (número): ")) - 1
                tipo_restauracion = list(TipoRestauracion)[tipo_idx]
                
                restauracion = gestor.iniciar_restauracion(id_obra, tipo_restauracion)
                if restauracion:
                    print(f"\n✅ Restauración iniciada exitosamente.")
                    print(restauracion.obtener_info())
                else:
                    print("\n❌ No se pudo iniciar la restauración. Verifique el ID de la obra.")
            except (ValueError, IndexError):
                print("❌ Selección inválida.")
        
        elif opcion == "3":
            # Finalizar restauración
            print("\n=== FINALIZAR RESTAURACIÓN ===")
            id_obra = input("Ingrese el ID de la obra: ")
            
            if gestor.finalizar_restauracion(id_obra):
                print(f"\n✅ Restauración finalizada exitosamente.")
            else:
                print("\n❌ No se encontró restauración en progreso para esta obra.")
        
        elif opcion == "4":
            # Consultar historial de restauraciones
            print("\n=== HISTORIAL DE RESTAURACIONES ===")
            id_obra = input("Ingrese el ID de la obra: ")
            obra = gestor.obtener_obra_por_id(id_obra)
            
            if obra:
                historial = obra.obtener_historial_restauraciones()
                if not historial:
                    print(f"La obra {id_obra} no tiene restauraciones registradas.")
                else:
                    print(f"\nHistorial de restauraciones para {id_obra}:")
                    for restauracion in historial:
                        print(restauracion.obtener_info())
            else:
                print("❌ Obra no encontrada.")
        
        elif opcion == "5":
            print("\n👋 Cerrando sesión...")
            break
        
        else:
            print("❌ Opción no válida.")


def menu_director(gestor: GestorMuseo) -> None:
    #Menú interactivo para el Director
    while True:
        usuario_actual = gestor.usuario_autenticado
        print(usuario_actual.obtener_menu())
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            # Consultar valoración total
            total = gestor.calcular_valoracion_total()
            print(f"\n=== VALORACIÓN TOTAL DEL MUSEO ===")
            print(f"Total: ${total:,.2f}")
            print(f"Número de obras en exposición: {len([o for o in gestor.obtener_obras() if o.estado == EstadoObra.EXPUESTA])}")
        
        elif opcion == "2":
            # Ceder obra
            if not gestor.museos_colaboradores:
                print("\n❌ No hay museos colaboradores registrados. Registre uno primero.")
                continue
            
            print("\n=== CEDER OBRA A OTRO MUSEO ===")
            obras_disponibles = [o for o in gestor.obtener_obras() if o.puede_ser_cedida()]
            
            if not obras_disponibles:
                print("❌ No hay obras disponibles para cesión.")
                continue
            
            for i, obra in enumerate(obras_disponibles, 1):
                print(f"{i}. {obra.id_obra} - {obra.autor} - ${obra.valor:.2f}")
            
            id_obra = input("Ingrese el ID de la obra: ")
            
            print("\nMuseos colaboradores:")
            for i, museo in enumerate(gestor.museos_colaboradores, 1):
                print(f"{i}. {museo}")
            
            museo_cesionario = input("Seleccione el museo cesionario: ")
            importe = validar_float("Importe de la cesión ($): ")
            fecha_fin = validar_fecha("Fecha de fin de la cesión")
            
            cesion = gestor.ceder_obra(id_obra, museo_cesionario, importe, fecha_fin)
            if cesion:
                print("\n✅ Obra cedida exitosamente.")
                print(cesion.obtener_info())
            else:
                print("\n❌ No se pudo ceder la obra. Verifique los datos.")
        
        elif opcion == "3":
            # Consultar cesiones vigentes
            cesiones_vigentes = gestor.obtener_cesiones_vigentes()
            
            if not cesiones_vigentes:
                print("\n✅ No hay cesiones vigentes en este momento.")
            else:
                print(f"\n=== CESIONES VIGENTES ({len(cesiones_vigentes)}) ===")
                for cesion in cesiones_vigentes:
                    print(cesion.obtener_info())
        
        elif opcion == "4":
            # Registrar museo colaborador
            print("\n=== REGISTRAR MUSEO COLABORADOR ===")
            nombre_museo = input("Nombre del museo: ")
            
            if gestor.registrar_museo_colaborador(nombre_museo):
                print(f"✅ Museo '{nombre_museo}' registrado exitosamente.")
            else:
                print(f"❌ El museo '{nombre_museo}' ya está registrado.")
        
        elif opcion == "5":
            print("\n👋 Cerrando sesión...")
            break
        
        else:
            print("❌ Opción no válida.")


def menu_encargado_catalogo(gestor: GestorMuseo) -> None:
    #Menú interactivo para el Encargado de Catálogo
    while True:
        usuario_actual = gestor.usuario_autenticado
        print(usuario_actual.obtener_menu())
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            menu_registrar_cuadro(gestor)
        elif opcion == "2":
            menu_registrar_escultura(gestor)
        elif opcion == "3":
            menu_registrar_objeto(gestor)
        elif opcion == "4":
            menu_consultar_obras(gestor)
        elif opcion == "5":
            print("\n👋 Cerrando sesión...")
            break
        else:
            print("❌ Opción no válida.")


def menu_visitante(gestor: GestorMuseo) -> None:
    #Menú interactivo para Visitantes
    while True:
        usuario_actual = gestor.usuario_autenticado
        print(usuario_actual.obtener_menu())
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            menu_consultar_obras(gestor)
        elif opcion == "2":
            print("\n=== DETALLES DE OBRA ===")
            id_obra = input("Ingrese el ID de la obra: ")
            obra = gestor.obtener_obra_por_id(id_obra)
            if obra:
                print(obra.obtener_info_completa())
            else:
                print("❌ Obra no encontrada.")
        elif opcion == "3":
            print("\n👋 Gracias por visitarnos. ¡Hasta pronto!")
            break
        else:
            print("❌ Opción no válida.")


def pantalla_principal(gestor: GestorMuseo, autenticacion: SistemaAutenticacion) -> None:
    #Pantalla principal del sistema
    while True:
        print("""   SISTEMA DE GESTIÓN DE OBRAS DEL MUSEO   
                      
        1. Iniciar sesión
        2. Ver usuarios de demostración
        3. Salir
        """)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            usuario = input("\nUsuario: ")
            contraseña = input("Contraseña: ")
            
            usuario_autenticado = autenticacion.autenticar(usuario, contraseña)
            
            if usuario_autenticado:
                print(f"\n✅ ¡Bienvenido, {usuario_autenticado.nombre}!")
                gestor.usuario_autenticado = usuario_autenticado
                
                # Derivar al menú correspondiente según el tipo de usuario
                if isinstance(usuario_autenticado, EncargadoCatalogo):
                    menu_encargado_catalogo(gestor)
                elif isinstance(usuario_autenticado, RestauradorJefe):
                    menu_restaurador_jefe(gestor)
                elif isinstance(usuario_autenticado, Director):
                    menu_director(gestor)
                elif isinstance(usuario_autenticado, Visitante):
                    menu_visitante(gestor)
            else:
                print("❌ Usuario o contraseña incorrectos.")
        
        elif opcion == "2":
            print("\n" + autenticacion.obtener_usuarios_demo())
        
        elif opcion == "3":
            print("\n👋 ¡Gracias por usar el sistema! Adiós.")
            break
        
        else:
            print("❌ Opción no válida.")


# ============================================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================================

if __name__ == "__main__":
    """
    Punto de entrada principal del sistema.
    
    Se inicializa:
    1. El sistema de autenticación
    2. El gestor del museo
    3. Se inicia la pantalla principal interactiva
    """
    print("\n" + "="*50)
    print("INICIANDO SISTEMA DE GESTIÓN DE OBRAS DE ARTE")
    print("="*50 + "\n")
    
    # Crear instancias de los sistemas principales
    gestor_museo = GestorMuseo()
    sistema_autenticacion = SistemaAutenticacion()
    
    # Iniciar la interfaz principal
    pantalla_principal(gestor_museo, sistema_autenticacion)