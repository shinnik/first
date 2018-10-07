from DoubleLinkedList import DoubleLinkedList
import unittest


class DLLAssertion(unittest.TestCase):

    def testPush(self):

        dll = DoubleLinkedList()
        dll.push(17)
        self.assertEqual(dll.last.elem, 17)

    def testPop(self):

        dll = DoubleLinkedList()
        dll.push(15)
        dll.push(14)
        dll.pop()
        self.assertEqual(dll.last.elem, 15)

    def testPopEmpty(self):
        """
        test pop for empty list
        """

        dll = DoubleLinkedList()
        dll.push(4)
        dll.pop()
        self.assertEqual(dll.first, None)
        self.assertEqual(dll.last, None)

    def testUnshift(self):

        dll = DoubleLinkedList()

        dll.push(6)
        dll.unshift(5)

        self.assertEqual(dll.first.elem, 5)
        self.assertEqual(dll.last.elem, 6)

        dll.unshift(11)
        self.assertEqual(dll.first.elem, 11)

    def testShift(self):

        dll = DoubleLinkedList()

        dll.push(10)
        dll.unshift(5)
        dll.shift()

        self.assertEqual(dll.first.elem, 10)

        dll.shift()

        self.assertEqual(dll.first, None)
        self.assertEqual(dll.last, None)

    def testLen(self):

        dll = DoubleLinkedList()

        dll.push(11)
        dll.unshift(14)
        dll.unshift(14)

        self.assertEqual(dll.len(), 3)

        dll.shift()
        dll.shift()
        dll.shift()

        # len of empty list
        self.assertEqual(dll.len(), 0)

    def testDelete(self):

        dll = DoubleLinkedList()

        dll.push(4)
        dll.push("fff")

        dll.delete(4)
        self.assertEqual(dll.first.elem, "fff")

        dll.delete("fff")
        self.assertEqual(dll.first, None)
        self.assertEqual(dll.last, None)

        # delete from empty list
        with self.assertRaises(AttributeError):
            dll.delete(5)

    def testContains(self):

        dll = DoubleLinkedList()

        dll.push(1)
        dll.push(2)
        dll.push(4)

        self.assertTrue(dll.contains(4))

        dll.delete(4)

        self.assertFalse(dll.contains(4))

        dll.delete(1)
        dll.delete(2)

        self.assertFalse(dll.contains(2))

    def testFirst_(self):

        dll = DoubleLinkedList()

        dll.push(11)
        dll.unshift(14)

        self.assertEqual(dll.first_(), 14)

        dll.shift()
        dll.shift()

        self.assertEqual(dll.first_(), None)

    def testLast_(self):

        dll = DoubleLinkedList()

        dll.push(1)
        dll.unshift(8)

        self.assertEqual(dll.last_(), 1)

        dll.pop()

        self.assertEqual(dll.last_(), 8)

        dll.shift()

        self.assertEqual(dll.last_(), None)