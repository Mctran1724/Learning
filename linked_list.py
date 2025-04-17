class Node:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    
    def __repr__(self):
        return f'({self.val})'

    def __str__(self):
        return f'({self.val})'

class LinkedList:
    def __init__(self, lst = []):
        if lst:
            iterator = iter(lst)
            self.head = Node(next(iterator))
            curr = self.head
            while True:
                try:
                    curr.next = Node(next(iterator))
                    curr = curr.next
                except StopIteration:
                    break
    
    def __repr__(self):
        result = []
        curr = self.head
        while curr:
            result.append(str(curr))
            curr = curr.next
        return " -> ".join(result)
    
    def __str__(self):
        result = []
        curr = self.head
        while curr:
            result.append(str(curr))
            curr = curr.next
        return " -> ".join(result)
    


def even_odd(head):
    parity = 1
    
    if not head or not head.next:
        return head
    
    odd = head
    even = head.next
    even_head = even
    while odd.next and even.next:
        if parity == 1:
            odd.next = even.next
            odd = odd.next
        else:
            even.next = odd.next
            even = even.next
        parity ^= 1
    odd.next = even_head

    return head

if __name__ == "__main__":
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    ll = LinkedList(lst)
    print(ll)
    head = even_odd(ll.head)

    while head:
        print(head.val, end=" -> ")
        head = head.next

