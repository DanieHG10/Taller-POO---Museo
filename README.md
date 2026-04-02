# Sistema de Gestión de Obras de Arte (Museo)

Este es el taller POO sobre la gestion de las obras, cuadro y obras del museo desarrollado en Python utilizando Programación Orientada a Objetos.

## Diagrama UML de Clases

A continuación se presenta la arquitectura del sistema:

```mermaid
classDiagram
    %% Enumeraciones
    class EstadoObra {
        <<enumeration>>
        EXPUESTA
        RESTAURACION
    }
    class TipoRestauracion {
        <<enumeration>>
        MANTENIMIENTO
        REPARACION
        RESTAURACION_COMPLETA
    }

    %% Jerarquía de Usuarios
    class Usuario {
        <<abstract>>
        +nombre: str
        +usuario: str
        +contraseña: str
        +autenticar(usuario, contraseña) bool
        +obtener_menu()* str
    }
    class EncargadoCatalogo {
        +obtener_menu() str
    }
    class RestauradorJefe {
        +obtener_menu() str
    }
    class Director {
        +obtener_menu() str
    }
    class Visitante {
        +obtener_menu() str
    }

    Usuario <|-- EncargadoCatalogo
    Usuario <|-- RestauradorJefe
    Usuario <|-- Director
    Usuario <|-- Visitante

    %% Jerarquía de Obras de Arte
    class ObraDeArte {
        <<abstract>>
        +id_obra: str
        +autor: str
        +periodo: str
        +valor: float
        +fecha_creacion: datetime
        +fecha_entrada: datetime
        +estado: EstadoObra
        +obtener_info_especifica()* str
        +obtener_info_completa() str
        +enviar_a_restauracion(tipo) Restauracion
        +finalizar_restauracion(restauracion) bool
        +obtener_historial_restauraciones() List~Restauracion~
        +necesita_restauracion_automatica() bool
        +puede_ser_cedida() bool
    }

    class Cuadro {
        +estilo: str
        +tecnica: str
        +obtener_info_especifica() str
    }
    class Escultura {
        +estilo: str
        +material: str
        +obtener_info_especifica() str
    }
    class Objeto {
        +descripcion: str
        +obtener_info_especifica() str
    }

    ObraDeArte <|-- Cuadro
    ObraDeArte <|-- Escultura
    ObraDeArte <|-- Objeto

    %% Clases Operativas
    class Restauracion {
        +id_restauracion: str
        +fecha_inicio: datetime
        +fecha_fin: datetime
        +obtener_info() str
    }

    class Cesion {
        +id_cesion: str
        +museo_cesionario: str
        +importe: float
        +fecha_inicio: datetime
        +fecha_fin: datetime
        +esta_vigente() bool
        +obtener_info() str
    }

    %% Sistemas Gestores
    class GestorMuseo {
        +museos_colaboradores: List~str~
        +registrar_cuadro(...) Cuadro
        +registrar_escultura(...) Escultura
        +registrar_objeto(...) Objeto
        +iniciar_restauracion(...) Restauracion
        +finalizar_restauracion(id_obra) bool
        +ceder_obra(...) Cesion
        +calcular_valoracion_total() float
    }

    class SistemaAutenticacion {
        +autenticar(usuario, contraseña) Usuario
        +obtener_usuarios_demo() str
    }

    %% Relaciones
    GestorMuseo o-- Usuario : "usuario_autenticado"
    GestorMuseo *-- ObraDeArte : "gestiona"
    GestorMuseo *-- Restauracion : "gestiona"
    GestorMuseo *-- Cesion : "gestiona"
    SistemaAutenticacion *-- Usuario : "registra"
    
    ObraDeArte "1" *-- "*" Restauracion : "tiene"
    ObraDeArte "1" o-- "0..1" Cesion : "cesion_vigente"
    
    ObraDeArte --> EstadoObra
    Restauracion --> TipoRestauracion
    Restauracion --> ObraDeArte
    Cesion --> ObraDeArte
    Cesion --> ObraDeArte
