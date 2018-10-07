class Item:

    def __init__(self, prev, next, elem):
        self.prev = prev
        self.next = next
        self.elem = elem


class DoubleLinkedList:

    def __init__(self):
        self.first = None
        self.last = None

    def push(self, data):

        new = Item(None, None, data)

        if self.first is None:
            self.first = new
            self.last = self.first
        else:
            new.prev = self.last
            new.next = None
            self.last.next = new
            self.last = new

    def pop(self):

        if self.last is not self.first:
            self.last = self.last.prev
            self.last.next = None
        else:
            self.first = self.last = None

    def unshift(self, data):

        new = Item(None, None, data)

        if self.first is None:
            self.first = new
            self.last = self.first

        else:
            new.next = self.first
            new.prev = None
            self.first.prev = new
            self.first = new

    def shift(self):

        try:
            if self.first.next is not None:
                self.first = self.first.next
                del self.first.prev

            else:
                self.first = self.last = None
        except AttributeError:
            print("List is empty")

    def len(self):

        temp = self.first
        length = 1

        if temp is None:
            return 0

        while temp.next is not None:

            temp = temp.next
            length += 1

        return length

    def delete(self, data):

        temp = self.first

        if self.first is None and self.last is None:
            msg = "List is already empty"
            raise AttributeError(msg)

        if self.first is self.last:
            if self.first.elem == data:
                self.first = self.last = None
        else:
            while temp.next is not None:
                if temp.elem == data:
                    if temp.prev is not None:
                        temp.next.prev = temp.prev
                        temp.prev.next = temp.next

                    else:
                        self.first = temp.next
                        temp.next.prev = None

                temp = temp.next

            if temp.next is None and temp.elem == data:
                temp.prev.next = None
                self.last = temp.prev

    def contains(self, data):

        temp = self.first

        while temp is not None:
            if temp.elem == data:
                return True
            else:
                temp = temp.next

        return False

    def first_(self):

        if self.first is not None:
            return self.first.elem
        else:
            return None

    def last_(self):

        if self.last is not None:
            return self.last.elem
        else:
            return None


if __name__ == "__main__":
    d = DoubleLinkedList()
    d.pop()
