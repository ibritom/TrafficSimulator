# Cola FIFO con nodos enlazados (para manejar autos en orden)
class LinkedListQueue:
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None

    def __init__(self):
        self.front = None
        self.rear = None
    # Agrega un nuevo elemento al final.
    def enqueue(self, data):
        new_node = self.Node(data)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
    # Retira y devuelve el primer elemento.
    def dequeue(self):
        if self.front is None:
            return None
        data = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        return data
    # Revisa si la cola está vacía.
    def is_empty(self):
        return self.front is None
