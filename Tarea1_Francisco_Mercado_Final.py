from datetime import datetime

# Clase Visitante
class Visitante:
    def __init__(self, nombre, edad, altura, dinero):
        if not (0 <= edad <= 120):
            raise ValueError("Edad no válida")
        if not (50 <= altura <= 250):
            raise ValueError("Altura no válida")

        self.nombre = nombre
        self.edad = edad
        self.altura = altura
        self.dinero = dinero
        self.tickets = []

    def comprar_ticket(self, atraccion):
        if self.dinero >= atraccion.precio:
            self.tickets.append(Ticket(len(self.tickets) + 1, atraccion.nombre, atraccion.precio))
            self.dinero -= atraccion.precio
            print(f"{self.nombre} ha comprado un ticket para {atraccion.nombre}.")
        else:
            print(f"{self.nombre} no tiene suficiente dinero para comprar el ticket.")

    def entregar_ticket(self, atraccion):
        ticket_encontrado = None
        for ticket in self.tickets:
            if ticket.atraccion == atraccion.nombre:
                ticket_encontrado = ticket
                break
        if ticket_encontrado:
            self.tickets.remove(ticket_encontrado)
            print(f"{self.nombre} ha entregado el ticket para {atraccion.nombre}.")
        else:
            print(f"{self.nombre} no tiene un ticket para {atraccion.nombre}.")

    def hacer_cola(self, atraccion):
        if not atraccion.verificar_restricciones(self):
            return
        if atraccion not in [t.atraccion for t in self.tickets]:
            print(f"{self.nombre} no tiene un ticket para {atraccion.nombre}. No puede hacer cola.")
        else:
            if len(atraccion.cola) >= atraccion.capacidad:
                print(f"La cola para {atraccion.nombre} está llena. No se pueden aceptar más visitantes.")
            else:
                atraccion.cola.append(self)
                print(f"{self.nombre} se ha puesto en la cola para {atraccion.nombre}.")

# Clase VisitanteVIP
class VisitanteVIP(Visitante):
    def __init__(self, nombre, edad, altura, dinero):
        super().__init__(nombre, edad, altura, dinero)
        self.entradas_gratis = {}

    def comprar_ticket(self, atraccion):
        if not atraccion.verificar_restricciones(self):
            return  # Verificación de restricciones antes del acceso gratuito.
        
        if self.entradas_gratis.get(atraccion.nombre, 0) < 2:
            self.entradas_gratis[atraccion.nombre] = self.entradas_gratis.get(atraccion.nombre, 0) + 1
            print(f"{self.nombre} ha accedido gratis a {atraccion.nombre}.")
        else:
            super().comprar_ticket(atraccion)

# Clase Atraccion
class Atraccion:
    def __init__(self, nombre, capacidad, duracion, precio):
        self.nombre = nombre
        self.capacidad = capacidad
        self.duracion = duracion
        self.estado = "activo"
        self.precio = precio
        self.cola = []

    def verificar_restricciones(self, visitante):
        return True

    def iniciar_ronda(self):
        if self.estado == "activo":
            num_participantes = min(len(self.cola), self.capacidad)
            print(f"Iniciando ronda en {self.nombre} con {num_participantes} participantes.")
            vip_participantes = [v for v in self.cola if isinstance(v, VisitanteVIP)]
            num_vip = min(len(vip_participantes), int(self.capacidad * 0.4))
            self.cola = self.cola[num_participantes:]
        else:
            print(f"La atracción {self.nombre} está fuera de servicio.")

# Clase AtraccionInfantil
class AtraccionInfantil(Atraccion):
    def verificar_restricciones(self, visitante):
        if visitante.edad > 10:
            print(f"{visitante.nombre} no puede ingresar a {self.nombre} por ser mayor de 10 años.")
            return False
        return True

# Clase MontañaRusa
class MontañaRusa(Atraccion):
    def __init__(self, nombre, capacidad, duracion, precio, velocidad_maxima, altura_maxima, extension):
        super().__init__(nombre, capacidad, duracion, precio)
        self.velocidad_maxima = velocidad_maxima
        self.altura_maxima = altura_maxima
        self.extension = extension

    def verificar_restricciones(self, visitante):
        if visitante.altura < 140:
            print(f"{visitante.nombre} no puede ingresar a {self.nombre} por no cumplir con la altura mínima de 140 cm.")
            return False
        return True

# Clase Ticket
class Ticket:
    def __init__(self, numero, atraccion, precio):
        self.numero = numero
        self.atraccion = atraccion
        self.precio = precio
        self.fecha_compra = datetime.now()

# Clase Parque
class Parque:
    def __init__(self, nombre):
        self.nombre = nombre
        self.juegos = []
        self.ventas = {}

    def agregar_atraccion(self, atraccion):
        self.juegos.append(atraccion)

    def cobrar_ticket(self, visitante, atraccion):
        visitante.comprar_ticket(atraccion)
        self.ventas[atraccion.nombre] = self.ventas.get(atraccion.nombre, 0) + atraccion.precio

    def resumen_de_ventas(self, dia):
        total_ingresos = 0
        for atraccion, ingresos in self.ventas.items():
            print(f"{atraccion}: {ingresos} en ventas.")
            total_ingresos += ingresos
        print(f"Total de ingresos del día: {total_ingresos}")

# Prueba de valores extremos
if __name__ == "__main__":
    # Crear parque
    parque = Parque("Diversiones Python")
    
    # Crear atracciones
    montana_rusa = MontañaRusa("Montaña Rusa Extrema", 5, 3, 100, 100, 200, 1500)
    juego_infantil = AtraccionInfantil("Carrusel Infantil", 10, 5, 20)
    
    parque.agregar_atraccion(montana_rusa)
    parque.agregar_atraccion(juego_infantil)
    
    # Crear visitantes
    visitante1 = Visitante("Finn", 15, 145, 150)
    visitante_vip = VisitanteVIP("Marceline", 25, 160, 200)
    visitante_sin_dinero = Visitante("Rollo de Canela", 25, 170, 0)  
    visitante_bajo = Visitante("Jake", 12, 130, 100)  
    
    # Comprar tickets
    parque.cobrar_ticket(visitante1, montana_rusa)
    parque.cobrar_ticket(visitante_vip, juego_infantil)
    parque.cobrar_ticket(visitante_sin_dinero, montana_rusa)  
    parque.cobrar_ticket(visitante_bajo, montana_rusa)  

    # Hacer cola
    visitante1.hacer_cola(montana_rusa)
    visitante_vip.hacer_cola(juego_infantil)
    visitante_bajo.hacer_cola(montana_rusa)  

    # Iniciar ronda
    montana_rusa.iniciar_ronda()
    juego_infantil.iniciar_ronda()

    # Resumen de ventas
    parque.resumen_de_ventas(datetime.now().date())
