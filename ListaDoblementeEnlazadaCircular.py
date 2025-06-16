class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

class CircularDoublyLinkedList:
    def __init__(self):
        self.tail = None
        self.size = 0

    def esta_vacia(self):
        return self.size == 0

    def insertar_al_inicio(self, value):
        new_node = Node(value)
        if self.esta_vacia():
            new_node.next = new_node
            new_node.prev = new_node
            self.tail = new_node
        else:
            head = self.tail.next
            new_node.next = head
            new_node.prev = self.tail
            head.prev = new_node
            self.tail.next = new_node
        self.size += 1

    def insertar_al_final(self, value):
        self.insertar_al_inicio(value)
        self.tail = self.tail.next

    def insertar_en(self, value, index):
        if index < 0 or index > self.size:
            raise IndexError("Índice fuera de rango")
        if index == 0:
            self.insertar_al_inicio(value)
        elif index == self.size:
            self.insertar_al_final(value)
        else:
            new_node = Node(value)
            current = self.tail.next
            for _ in range(index - 1):
                current = current.next
            new_node.next = current.next
            new_node.prev = current
            current.next.prev = new_node
            current.next = new_node
            self.size += 1

    def eliminar_al_inicio(self):
        if self.esta_vacia():
            raise Exception("La lista está vacía")
        if self.size == 1:
            self.tail = None
        else:
            head = self.tail.next
            self.tail.next = head.next
            head.next.prev = self.tail
        self.size -= 1

    def eliminar_al_final(self):
        if self.esta_vacia():
            raise Exception("La lista está vacía")
        if self.size == 1:
            self.tail = None
        else:
            prev_tail = self.tail.prev
            prev_tail.next = self.tail.next
            self.tail.next.prev = prev_tail
            self.tail = prev_tail
        self.size -= 1

    def eliminar_en(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Índice fuera de rango")
        if index == 0:
            self.eliminar_al_inicio()
        elif index == self.size - 1:
            self.eliminar_al_final()
        else:
            current = self.tail.next
            for _ in range(index):
                current = current.next
            current.prev.next = current.next
            current.next.prev = current.prev
            self.size -= 1

    def obtener_tamaño(self):
        return self.size

    def __str__(self):
        if self.esta_vacia():
            return "La lista está vacía"
        result = []
        current = self.tail.next
        while True:
            result.append(str(current.value))
            current = current.next
            if current == self.tail.next:
                break
        return ", ".join(result)