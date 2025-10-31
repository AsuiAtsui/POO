

class Persona:
    def __init__(self, nombre, correo, direccion, telefono):
        self.nombre = nombre
        self.correo = correo
        self.direccion = direccion
        self.telefono = telefono

    def mostrar_info(self):
        print(f"Nombre: {self.nombre} | Correo: {self.correo} | Dirección: {self.direccion} | Teléfono: {self.telefono}")



class Cliente(Persona):
    def __init__(self, nombre, correo, direccion, telefono, rfc, tipo):
        super().__init__(nombre, correo, direccion, telefono)
        self.rfc = rfc
        self.tipo = tipo

    def mostrar_info(self):
        super().mostrar_info()
        print(f"RFC: {self.rfc} | Tipo: {self.tipo}")


class Empleado(Persona):
    def __init__(self, nombre, correo, direccion, telefono, id_empleado, departamento, usuario, contrasena):
        super().__init__(nombre, correo, direccion, telefono)
        self.id_empleado = id_empleado
        self.departamento = departamento
        self.usuario = usuario
        self.contrasena = contrasena

    def mostrar_info(self):
        print(f"\n--- Información del Empleado ---")
        super().mostrar_info()
        print(f"ID Empleado: {self.id_empleado} | Departamento: {self.departamento}")


class Producto:
    def __init__(self, codigo, nombre, precio, cantidad):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def mostrar_info(self):
        print(f"Código: {self.codigo} | Nombre: {self.nombre} | Precio: ${self.precio:.2f} | Cantidad: {self.cantidad}")

    def actualizar_stock(self, cantidad):
        self.cantidad += cantidad


class Inventario:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        for p in self.productos:
            if p.codigo == producto.codigo:
                print("El producto ya existe en el inventario.")
                return
        self.productos.append(producto)
        print("Producto agregado correctamente.")

    def mostrar_inventario(self):
        if not self.productos:
            print("No hay productos registrados.")
        else:
            print("\n--- Inventario de la Ferretería ---")
            for p in self.productos:
                p.mostrar_info()

    def buscar_producto(self, codigo):
        for p in self.productos:
            if p.codigo == codigo:
                return p
        return None

    def eliminar_producto(self, codigo):
        producto = self.buscar_producto(codigo)
        if producto:
            self.productos.remove(producto)
            print("Producto eliminado correctamente.")
        else:
            print("Producto no encontrado.")


class Venta:
    def __init__(self, cliente, producto, cantidad):
        self.cliente = cliente
        self.producto = producto
        self.cantidad = cantidad
        self.total = self.calcular_total()

    def calcular_total(self):
        return self.producto.precio * self.cantidad

    def mostrar_detalle(self):
        print("\n--- Detalle de Venta ---")
        self.cliente.mostrar_info()
        print(f"Producto: {self.producto.nombre}")
        print(f"Cantidad: {self.cantidad}")
        print(f"Total a pagar: ${self.total:.2f}")


class RegistroClientes:
    def __init__(self):
        self.clientes = []

    def registrar_cliente(self):
        telefono = input("Teléfono del cliente: ")
        for c in self.clientes:
            if c.telefono == telefono:
                print("Ya existe un cliente con este teléfono.")
                return

        nombre = input("Nombre del cliente: ")
        correo = input("Correo del cliente: ")
        direccion = input("Dirección del cliente: ")
        rfc = input("RFC del cliente: ")
        tipo = "Registrado"
        cliente = Cliente(nombre, correo, direccion, telefono, rfc, tipo)
        self.clientes.append(cliente)
        print("Cliente registrado correctamente.")

    def mostrar_clientes(self):
        if not self.clientes:
            print("No hay clientes registrados.")
        else:
            print("\n--- Lista de Clientes Registrados ---")
            for c in self.clientes:
                c.mostrar_info()

    def buscar_cliente(self, telefono):
        for c in self.clientes:
            if c.telefono == telefono:
                return c
        return None



class Ferreteria:
    def __init__(self, nombre):
        self.nombre = nombre
        self.inventario = Inventario()
        self.registro_clientes = RegistroClientes()
        self.empleados = []
        self.empleado_actual = None
        self.crear_empleado_admin()


    def crear_empleado_admin(self):
        admin = Empleado(
            "Administrador", "admin@ferreteria.com", "Calle Principal #123",
            "0000000000", "E001", "Administración", "admin", "1234"
        )
        self.empleados.append(admin)


    def iniciar_sesion(self):
        print("\n--- Inicio de Sesión ---")
        usuario = input("Usuario: ")
        contrasena = input("Contraseña: ")

        for emp in self.empleados:
            if emp.usuario == usuario and emp.contrasena == contrasena:
                self.empleado_actual = emp
                print(f"\nBienvenido, {emp.nombre} ({emp.departamento})")
                return True

        print("Credenciales incorrectas.")
        return False

    def cerrar_sesion(self):
        print(f"Sesión cerrada. Hasta luego, {self.empleado_actual.nombre}.")
        self.empleado_actual = None

    def registrar_producto(self):
        codigo = input("Código del producto: ")
        nombre = input("Nombre del producto: ")
        precio = float(input("Precio del producto: "))
        cantidad = int(input("Cantidad en stock: "))
        producto = Producto(codigo, nombre, precio, cantidad)
        self.inventario.agregar_producto(producto)

    def realizar_venta(self):
        telefono = input("Teléfono del cliente (si no está registrado, se creará como General): ")
        cliente = self.registro_clientes.buscar_cliente(telefono)

        if not cliente:
            nombre_cliente = input("Nombre del cliente: ")
            correo = input("Correo del cliente: ")
            direccion = input("Dirección del cliente: ")
            rfc = "N/A"
            cliente = Cliente(nombre_cliente, correo, direccion, telefono, rfc, "General")

        codigo = input("Código del producto a vender: ")
        producto = self.inventario.buscar_producto(codigo)
        if not producto:
            print("Producto no encontrado.")
            return

        cantidad = int(input("Cantidad a comprar: "))
        if cantidad > producto.cantidad:
            print("No hay suficiente stock para realizar la venta.")
            return
        producto.actualizar_stock(-cantidad)

        venta = Venta(cliente, producto, cantidad)
        venta.mostrar_detalle()

    def menu(self):
        while True:
            if not self.empleado_actual:
                if not self.iniciar_sesion():
                    continue

            print(f"\n--- Sistema de Ferretería {self.nombre} ---")
            print("1. Registrar producto")
            print("2. Mostrar inventario")
            print("3. Eliminar producto")
            print("4. Realizar venta")
            print("5. Registrar cliente")
            print("6. Ver clientes registrados")
            print("7. Cerrar sesión")
            print("8. Salir del sistema")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.registrar_producto()
            elif opcion == "2":
                self.inventario.mostrar_inventario()
            elif opcion == "3":
                codigo = input("Ingrese el código del producto a eliminar: ")
                self.inventario.eliminar_producto(codigo)
            elif opcion == "4":
                self.realizar_venta()
            elif opcion == "5":
                self.registro_clientes.registrar_cliente()
            elif opcion == "6":
                self.registro_clientes.mostrar_clientes()
            elif opcion == "7":
                self.cerrar_sesion()
            elif opcion == "8":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción inválida.")


# Ejecucion
print("Bienvenido a la Ferretería 'La Llavenuda'")

ferreteria = Ferreteria("La Llavenuda")
ferreteria.menu()

