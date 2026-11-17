from abc import ABC, abstractmethod
from datetime import datetime
from functools import singledispatchmethod
import re
from typing import List, Optional
 
 
# ==============================================================================
# 1. JERARQUÍA DE EXCEPCIONES PERSONALIZADAS
# ==============================================================================
class SoftwareFJError(Exception):
    """Excepción base para todos los errores del dominio de Software FJ."""
    pass
 
 
class DatoInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos ingresados no cumplen las reglas de validación."""
    pass
 
 
class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un argumento obligatorio o es None/vacío."""
    pass
 
 
class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza al intentar reservar un servicio inactivo o sin disponibilidad."""
    pass
 
 
class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza al intentar transiciones de estado inválidas o duplicados."""
    pass
 
 
class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un cálculo financiero arroja valores negativos o incoherentes."""
    pass
 
 
# ==============================================================================
# 2. GESTOR DE LOGS (PERSISTENCIA EN ARCHIVO PLANO)
# ==============================================================================
class SistemaLogger:
    """Gestiona el registro de eventos y errores en un archivo de texto plano."""
 
    def __init__(self, ruta_archivo: str = "software_fj.log") -> None:
        self._ruta_archivo = ruta_archivo
 
    def registrar_evento(self, mensaje: str) -> None:
        self._escribir("INFO", mensaje)
 
    def registrar_error(self, error: Exception, contexto: str = "") -> None:
        detalle_causa = f" | Causa original: {repr(error.__cause__)}" if error.__cause__ else ""
        mensaje = f"{contexto} -> [{type(error).__name__}] {str(error)}{detalle_causa}"
        self._escribir("ERROR", mensaje)
 
    def _escribir(self, nivel: str, mensaje: str) -> None:
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{marca_tiempo}] [{nivel}] {mensaje}\n"
        archivo = None
        try:
            archivo = open(self._ruta_archivo, mode="a", encoding="utf-8")
            archivo.write(linea)
        except OSError as exc:
            print(f"[CRÍTICO] No se pudo escribir en el archivo de log: {exc}")
        finally:
            if archivo and not archivo.closed:
                archivo.close()
 
 
# ==============================================================================
# 3. CLASES ABSTRACTAS Y ENTIDADES DEL DOMINIO (POO)
# ==============================================================================
class EntidadSistema(ABC):
    """Clase abstracta base para todas las entidades identificables del sistema."""
 
    def __init__(self, id_entidad: str) -> None:
        if not id_entidad or not str(id_entidad).strip():
            raise ParametroFaltanteError("El ID de la entidad no puede estar vacío.")
        self._id = str(id_entidad).strip()
        self._fecha_creacion = datetime.now()
 
    @property
    def id(self) -> str:
        return self._id
 
    @property
    def fecha_creacion(self) -> datetime:
        return self._fecha_creacion
 
    @abstractmethod
    def obtener_resumen(self) -> str:
        """Devuelve una representación legible del estado actual de la entidad."""
        pass
 
 
class Cliente(EntidadSistema):
    """Representa un cliente de Software FJ con encapsulación y validaciones estrictas."""
 
    def __init__(self, id_cliente: str, nombre: str, documento: str, email: str, telefono: str) -> None:
        super().__init__(id_cliente)
        self.nombre = nombre
        self.documento = documento
        self.email = email
        self.telefono = telefono
 
    @property
    def nombre(self) -> str:
        return self._nombre
 
    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or len(valor.strip()) < 3:
            raise DatoInvalidoError("El nombre del cliente debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()
 
    @property
    def documento(self) -> str:
        return self._documento
 
    @documento.setter
    def documento(self, valor: str) -> None:
        if not valor or not str(valor).isdigit() or len(str(valor)) < 6:
            raise DatoInvalidoError(f"Documento inválido: '{valor}'. Debe contener al menos 6 dígitos numéricos.")
        self._documento = str(valor).strip()
 
    @property
    def email(self) -> str:
        return self._email
 
    @email.setter
    def email(self, valor: str) -> None:
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not valor or not re.match(patron, valor.strip()):
            raise DatoInvalidoError(f"Correo electrónico inválido: '{valor}'.")
        self._email = valor.strip().lower()
 
    @property
    def telefono(self) -> str:
        return self._telefono
 
    @telefono.setter
    def telefono(self, valor: str) -> None:
        limpio = str(valor).strip() if valor else ""
        if not limpio.isdigit() or len(limpio) < 7:
            raise DatoInvalidoError(f"Teléfono inválido: '{valor}'.")
        self._telefono = limpio
 
    def obtener_resumen(self) -> str:
        return f"Cliente [{self.id}] {self.nombre} | Doc: {self.documento} | Email: {self.email}"
 
 
class Servicio(EntidadSistema, ABC):
    """Clase abstracta que define el contrato polimórfico de los servicios."""
 
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True) -> None:
        super().__init__(id_servicio)
        if not nombre or not nombre.strip():
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        self._nombre = nombre.strip()
        self.tarifa_base = tarifa_base
        self._disponible = bool(disponible)
 
    @property
    def nombre(self) -> str:
        return self._nombre
 
    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base
 
    @tarifa_base.setter
    def tarifa_base(self, valor: float) -> None:
        try:
            tarifa = float(valor)
        except (TypeError, ValueError) as exc:
            raise DatoInvalidoError(f"La tarifa '{valor}' no es un número válido.") from exc
        if tarifa <= 0:
            raise DatoInvalidoError("La tarifa base debe ser mayor a cero.")
        self._tarifa_base = tarifa
 
    @property
    def disponible(self) -> bool:
        return self._disponible
 
    @disponible.setter
    def disponible(self, estado: bool) -> None:
        self._disponible = bool(estado)
 
    @abstractmethod
    def validar_parametros(self, duracion: int) -> None:
        """Valida las reglas específicas del servicio antes de reservar."""
        pass
 
    @abstractmethod
    def calcular_costo_base(self, duracion: int) -> float:
        """Calcula el costo neto según las reglas del servicio especializado."""
        pass
 
    @abstractmethod
    def describir_servicio(self) -> str:
        """Devuelve la ficha técnica detallada del servicio."""
        pass
 
    # --- SOBRECARGA DE MÉTODOS MEDIANTE SINGLEDISPATCHMETHOD ---
    @singledispatchmethod
    def calcular_total(self, duracion: int, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        """
        Sobrecarga 1 (Por defecto - int): Calcula costo a partir de duración,
        aplicando descuento porcentual e impuestos.
        """
        self.validar_parametros(duracion)
        if not (0 <= impuesto <= 1) or not (0 <= descuento < 1):
            raise CalculoInconsistenteError("Impuesto o descuento fuera de rango permitido (0.0 a 1.0).")
 
        subtotal = self.calcular_costo_base(duracion)
        monto_descuento = subtotal * descuento
        base_gravable = subtotal - monto_descuento
        total = base_gravable * (1 + impuesto)
 
        if total <= 0:
            raise CalculoInconsistenteError("El cálculo total arrojó un valor menor o igual a cero.")
        return round(total, 2)
 
    @calcular_total.register
    def _(self, configuracion: dict) -> float:
        """
        Sobrecarga 2 (dict): Permite calcular pasando un diccionario con parámetros
        financieros adicionales (ej. recargos fijos por logística o soporte).
        """
        if "duracion" not in configuracion:
            raise ParametroFaltanteError("El diccionario de cálculo debe incluir la clave 'duracion'.")
        duracion = configuracion["duracion"]
        impuesto = configuracion.get("impuesto", 0.19)
        descuento = configuracion.get("descuento", 0.0)
        recargo = configuracion.get("recargo_fijo", 0.0)
 
        if recargo < 0:
            raise CalculoInconsistenteError("El recargo fijo no puede ser negativo.")
 
        total_base = self.calcular_total(duracion, impuesto, descuento)
        return round(total_base + recargo, 2)
 
    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Servicio [{self.id}] {self.nombre} (${self.tarifa_base:,.2f}) - {estado}"
 
 
class ReservaSala(Servicio):
    """Servicio especializado para alquiler de salas de reuniones o capacitación."""
 
    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, capacidad: int, tiene_proyector: bool = True) -> None:
        super().__init__(id_servicio, nombre, tarifa_hora)
        if capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser mayor a 0.")
        self._capacidad = capacidad
        self._tiene_proyector = tiene_proyector
 
    def validar_parametros(self, duracion: int) -> None:
        if not isinstance(duracion, int) or duracion < 1 or duracion > 12:
            raise DatoInvalidoError("La reserva de sala debe ser entre 1 y 12 horas.")
 
    def calcular_costo_base(self, duracion: int) -> float:
        self.validar_parametros(duracion)
        recargo_audiovisual = 15000.0 if self._tiene_proyector else 0.0
        return (self.tarifa_base * duracion) + recargo_audiovisual
 
    def describir_servicio(self) -> str:
        proy = "con proyector 4K" if self._tiene_proyector else "sin proyector"
        return f"Sala '{self.nombre}' | Capacidad: {self._capacidad} personas ({proy}) | Tarifa/h: ${self.tarifa_base:,.2f}"
 
 
class AlquilerEquipo(Servicio):
    """Servicio especializado para préstamo de hardware (laptops, servidores, estaciones)."""
 
    def __init__(self, id_servicio: str, nombre: str, tarifa_dia: float, serial: str, deposito_garantia: float) -> None:
        super().__init__(id_servicio, nombre, tarifa_dia)
        if not serial or not serial.strip():
            raise ParametroFaltanteError("El serial del equipo es obligatorio.")
        if deposito_garantia < 0:
            raise DatoInvalidoError("El depósito de garantía no puede ser negativo.")
        self._serial = serial.strip()
        self._deposito_garantia = deposito_garantia
 
    def validar_parametros(self, duracion: int) -> None:
        if not isinstance(duracion, int) or duracion < 1 or duracion > 30:
            raise DatoInvalidoError("El alquiler de equipos debe ser entre 1 y 30 días.")
 
    def calcular_costo_base(self, duracion: int) -> float:
        self.validar_parametros(duracion)
        return (self.tarifa_base * duracion) + self._deposito_garantia
 
    def describir_servicio(self) -> str:
        return (
            f"Equipo '{self.nombre}' [S/N: {self._serial}] | "
            f"Tarifa/día: ${self.tarifa_base:,.2f} + Garantía: ${self._deposito_garantia:,.2f}"
        )
 
 
class AsesoriaEspecializada(Servicio):
    """Servicio especializado de consultoría en arquitectura, DevOps o desarrollo."""
 
    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, especialidad: str, nivel_senior: bool = True) -> None:
        super().__init__(id_servicio, nombre, tarifa_hora)
        if not especialidad or not especialidad.strip():
            raise ParametroFaltanteError("Debe especificar el área de especialidad de la asesoría.")
        self._especialidad = especialidad.strip()
        self._nivel_senior = nivel_senior
 
    def validar_parametros(self, duracion: int) -> None:
        if not isinstance(duracion, int) or duracion < 2:
            raise DatoInvalidoError("Las asesorías especializadas requieren un mínimo de 2 horas.")
 
    def calcular_costo_base(self, duracion: int) -> float:
        self.validar_parametros(duracion)
        factor_senior = 1.25 if self._nivel_senior else 1.0
        return self.tarifa_base * duracion * factor_senior
 
    def describir_servicio(self) -> str:
        nivel = "Senior" if self._nivel_senior else "Semi-Senior"
        return f"Asesoría {nivel} en {self._especialidad} ('{self.nombre}') | Tarifa base/h: ${self.tarifa_base:,.2f}"
 
 
class Reserva(EntidadSistema):
    """Integra Cliente, Servicio, duración y ciclo de vida de la reserva."""
 
    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "PROCESADA", "CANCELADA")
 
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: int, descuento: float = 0.0) -> None:
        super().__init__(id_reserva)
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("Se requiere una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("Se requiere una instancia válida de Servicio.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no está disponible actualmente.")
 
        servicio.validar_parametros(duracion)
 
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._descuento = descuento
        self._estado = "PENDIENTE"
        self._costo_total = self._servicio.calcular_total(duracion, descuento=descuento)
 
    @property
    def estado(self) -> str:
        return self._estado
 
    @property
    def costo_total(self) -> float:
        return self._costo_total
 
    def confirmar(self) -> None:
        if self._estado != "PENDIENTE":
            raise OperacionNoPermitidaError(f"No se puede confirmar una reserva en estado '{self._estado}'.")
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self._servicio.nombre}' dejó de estar disponible.")
        self._estado = "CONFIRMADA"
        if isinstance(self._servicio, AlquilerEquipo):
            self._servicio.disponible = False
 
    def procesar(self) -> None:
        if self._estado != "CONFIRMADA":
            raise OperacionNoPermitidaError(
                f"Solo se pueden procesar reservas CONFIRMADAS (estado actual: '{self._estado}')."
            )
        self._estado = "PROCESADA"
        if isinstance(self._servicio, AlquilerEquipo):
            self._servicio.disponible = True
 
    def cancelar(self) -> None:
        if self._estado in ("PROCESADA", "CANCELADA"):
            raise OperacionNoPermitidaError(f"No es posible cancelar una reserva en estado '{self._estado}'.")
        estado_anterior = self._estado
        self._estado = "CANCELADA"
        if estado_anterior == "CONFIRMADA" and isinstance(self._servicio, AlquilerEquipo):
            self._servicio.disponible = True
 
    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self.id}] | Estado: {self._estado} | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} ({self._duracion} unid.) | Total: ${self._costo_total:,.2f}"
        )
 
 
# ==============================================================================
# 4. CONTROLADOR LÓGICO (GESTIÓN DE LISTAS INTERNAS Y EXCEPCIONES)
# ==============================================================================
class GestorSoftwareFJ:
    """Controlador lógico central de Software FJ sin dependencias de base de datos."""
 
    def __init__(self, logger: SistemaLogger) -> None:
        self._logger = logger
        self._clientes: List[Cliente] = []
        self._servicios: List[Servicio] = []
        self._reservas: List[Reserva] = []
 
    def registrar_cliente(self, cliente: Cliente) -> bool:
        try:
            if any(c.id == cliente.id or c.documento == cliente.documento for c in self._clientes):
                raise OperacionNoPermitidaError(
                    f"Ya existe un cliente con ID '{cliente.id}' o documento '{cliente.documento}'."
                )
            self._clientes.append(cliente)
        except SoftwareFJError as exc:
            self._logger.registrar_error(exc, f"Fallo al registrar cliente '{getattr(cliente, 'id', 'N/A')}'")
            print(f"[ERROR CONTROLADO] {exc}")
            return False
        else:
            self._logger.registrar_evento(f"Cliente registrado: {cliente.obtener_resumen()}")
            print(f"[OK] {cliente.obtener_resumen()}")
            return True
 
    def registrar_servicio(self, servicio: Servicio) -> bool:
        try:
            if any(s.id == servicio.id for s in self._servicios):
                raise OperacionNoPermitidaError(f"El servicio con ID '{servicio.id}' ya existe.")
            self._servicios.append(servicio)
        except SoftwareFJError as exc:
            self._logger.registrar_error(exc, "Fallo al registrar servicio")
            print(f"[ERROR CONTROLADO] {exc}")
            return False
        else:
            self._logger.registrar_evento(f"Servicio registrado: {servicio.obtener_resumen()}")
            print(f"[OK] {servicio.describir_servicio()}")
            return True
 
    def buscar_cliente(self, id_cliente: str) -> Cliente:
        for cliente in self._clientes:
            if cliente.id == id_cliente:
                return cliente
        raise DatoInvalidoError(f"No se encontró ningún cliente con ID '{id_cliente}'.")
 
    def buscar_servicio(self, id_servicio: str) -> Servicio:
        for servicio in self._servicios:
            if servicio.id == id_servicio:
                return servicio
        raise DatoInvalidoError(f"No se encontró ningún servicio con ID '{id_servicio}'.")
 
    def crear_reserva(
        self, id_reserva: str, id_cliente: str, id_servicio: str, duracion: int, descuento: float = 0.0
    ) -> Optional[Reserva]:
        try:
            if any(r.id == id_reserva for r in self._reservas):
                raise OperacionNoPermitidaError(f"El ID de reserva '{id_reserva}' ya está en uso.")
 
            try:
                cliente = self.buscar_cliente(id_cliente)
                servicio = self.buscar_servicio(id_servicio)
            except DatoInvalidoError as exc_busqueda:
                raise OperacionNoPermitidaError(
                    f"Imposible crear reserva '{id_reserva}' por referencias inexistentes."
                ) from exc_busqueda
 
            nueva_reserva = Reserva(id_reserva, cliente, servicio, duracion, descuento)
            self._reservas.append(nueva_reserva)
        except SoftwareFJError as exc:
            self._logger.registrar_error(exc, f"Error creando reserva '{id_reserva}'")
            print(f"[ERROR CONTROLADO] Reserva '{id_reserva}': {exc}")
            return None
        else:
            self._logger.registrar_evento(f"Reserva creada: {nueva_reserva.obtener_resumen()}")
            print(f"[OK] {nueva_reserva.obtener_resumen()}")
            return nueva_reserva
 
    def gestionar_estado_reserva(self, id_reserva: str, accion: str) -> bool:
        try:
            reserva = next((r for r in self._reservas if r.id == id_reserva), None)
            if not reserva:
                raise DatoInvalidoError(f"Reserva '{id_reserva}' no encontrada.")
 
            accion_norm = accion.strip().upper()
            if accion_norm == "CONFIRMAR":
                reserva.confirmar()
            elif accion_norm == "PROCESAR":
                reserva.procesar()
            elif accion_norm == "CANCELAR":
                reserva.cancelar()
            else:
                raise DatoInvalidoError(f"Acción de reserva desconocida: '{accion}'.")
        except SoftwareFJError as exc:
            self._logger.registrar_error(exc, f"Error al {accion} reserva '{id_reserva}'")
            print(f"[ERROR CONTROLADO] Acción '{accion}' en '{id_reserva}': {exc}")
            return False
        else:
            self._logger.registrar_evento(f"Reserva '{id_reserva}' actualizada a estado {reserva.estado}")
            print(f"[OK] Reserva '{id_reserva}' -> Nuevo estado: {reserva.estado}")
            return True
        finally:
            self._logger.registrar_evento(f"Auditoría de transición ejecutada sobre '{id_reserva}'.")
 
    def generar_reporte_consola(self) -> None:
        print("\n" + "=" * 75)
        print("RESUMEN GENERAL EN MEMORIA - SOFTWARE FJ")
        print("=" * 75)
        print(f"Clientes activos : {len(self._clientes)}")
        print(f"Servicios activos: {len(self._servicios)}")
        print(f"Reservas totales : {len(self._reservas)}")
        for r in self._reservas:
            print(f"  -> {r.obtener_resumen()}")
        print("=" * 75)
 
 
# ==============================================================================
# 5. SIMULACIÓN DE OPERACIONES (VALIDACIÓN DE ESTABILIDAD ANTE ERRORES)
# ==============================================================================
def ejecutar_simulacion() -> None:
    logger = SistemaLogger("software_fj.log")
    gestor = GestorSoftwareFJ(logger)
    logger.registrar_evento("=== INICIO DE SIMULACIÓN DEL SISTEMA SOFTWARE FJ ===")
 
    print("--- FASE 1: REGISTRO DE CLIENTES (OPERACIONES 1 A 4) ---")
    # Op 1: Cliente válido 1
    c1 = Cliente("CLI-01", "Laura Gómez", "1061789456", "laura.gomez@empresa.com", "3104567890")
    gestor.registrar_cliente(c1)
 
    # Op 2: Cliente válido 2
    c2 = Cliente("CLI-02", "Carlos Méndez", "76321987", "cmendez@techcauca.co", "3209876543")
    gestor.registrar_cliente(c2)
 
    # Op 3: Cliente inválido (correo mal formado y documento corto)
    try:
        c_invalido = Cliente("CLI-03", "Ana", "123", "correo_sin_arroba", "300")
        gestor.registrar_cliente(c_invalido)
    except SoftwareFJError as exc:
        logger.registrar_error(exc, "Instanciación fallida de Cliente CLI-03")
        print(f"[ERROR CONTROLADO] Instanciación Cliente: {exc}")
 
    # Op 4: Cliente duplicado por documento
    c_duplicado = Cliente("CLI-04", "Laura Copia", "1061789456", "otra@empresa.com", "3112223344")
    gestor.registrar_cliente(c_duplicado)
 
    print("\n--- FASE 2: CREACIÓN DE SERVICIOS ESPECIALIZADOS (OPERACIONES 5 A 8) ---")
    # Op 5: Servicio Sala válido
    s1 = ReservaSala("SRV-01", "Sala Innovación Cauca", 80000.0, capacidad=15, tiene_proyector=True)
    gestor.registrar_servicio(s1)
 
    # Op 6: Servicio Alquiler de Equipo válido
    s2 = AlquilerEquipo("SRV-02", "Workstation Ryzen 9 + 64GB RAM", 120000.0, serial="FJ-WK-9981", deposito_garantia=200000.0)
    gestor.registrar_servicio(s2)
 
    # Op 7: Servicio Asesoría Especializada válido
    s3 = AsesoriaEspecializada("SRV-03", "Arquitectura Cloud & Docker", 150000.0, especialidad="DevOps", nivel_senior=True)
    gestor.registrar_servicio(s3)
 
    # Op 8: Servicio inválido (tarifa negativa)
    try:
        s_invalido = ReservaSala("SRV-04", "Sala Fantasma", -50000.0, capacidad=5)
        gestor.registrar_servicio(s_invalido)
    except SoftwareFJError as exc:
        logger.registrar_error(exc, "Instanciación fallida de Servicio SRV-04")
        print(f"[ERROR CONTROLADO] Instanciación Servicio: {exc}")
 
    print("\n--- FASE 3: DEMOSTRACIÓN DE SOBRECARGA DE MÉTODOS ---")
    costo_estandar = s3.calcular_total(4, impuesto=0.19, descuento=0.10)
    costo_paquete = s3.calcular_total({"duracion": 4, "impuesto": 0.19, "descuento": 0.10, "recargo_fijo": 25000.0})
    print(f"[INFO SOBRECARGA] Asesoría 4h (int): ${costo_estandar:,.2f} | Con recargo (dict): ${costo_paquete:,.2f}")
 
    print("\n--- FASE 4: GESTIÓN DE RESERVAS Y CICLO DE VIDA (OPERACIONES 9 A 14) ---")
    # Op 9: Reserva exitosa de Sala + Confirmación + Procesamiento
    gestor.crear_reserva("RES-101", "CLI-01", "SRV-01", duracion=3, descuento=0.05)
    gestor.gestionar_estado_reserva("RES-101", "CONFIRMAR")
    gestor.gestionar_estado_reserva("RES-101", "PROCESAR")
 
    # Op 10: Reserva exitosa de Equipo (bloquea disponibilidad al confirmar)
    gestor.crear_reserva("RES-102", "CLI-02", "SRV-02", duracion=5)
    gestor.gestionar_estado_reserva("RES-102", "CONFIRMAR")
 
    # Op 11: Reserva fallida por servicio no disponible (el equipo SRV-02 ya está alquilado)
    gestor.crear_reserva("RES-103", "CLI-01", "SRV-02", duracion=2)
 
    # Op 12: Reserva fallida por violar regla de duración mínima (Asesoría exige >= 2 horas)
    gestor.crear_reserva("RES-104", "CLI-02", "SRV-03", duracion=1)
 
    # Op 13: Reserva fallida con cliente inexistente (encadenamiento de excepciones)
    gestor.crear_reserva("RES-105", "CLI-999", "SRV-01", duracion=2)
 
    # Op 14: Operación de estado no permitida (intentar cancelar RES-101 ya PROCESADA)
    gestor.gestionar_estado_reserva("RES-101", "CANCELAR")
 
    # Liberar equipo de RES-102 procesando la devolución
    gestor.gestionar_estado_reserva("RES-102", "PROCESAR")
 
    gestor.generar_reporte_consola()
    logger.registrar_evento("=== FIN DE SIMULACIÓN SIN INTERRUPCIONES ===")


ejecutar_simulacion();
