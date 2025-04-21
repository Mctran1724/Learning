"""
BST classes for benchmarking comparisons
"""
class BSTNode:
    def __init__(self, key, val, left = None, right = None):
        self.key = key
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
       return f"({self.key}, {self.val})"

    
    def __str__(self):
        return self.__repr__()


class BSTMap:

    elbow = "└──"
    pipe = "│  "
    tee = "├──"

    def __init__(self, method = "iterative"):
        self.root = None
        self.length = 0
        self.depth = 0 
        self.method = method

    def _inorder(self, node):
        if not node:
            return []
        return self._inorder(node.left) + [node] + self._inorder(node.right)

    def traverse(self, method="inorder"):
        if method == "inorder":
            return self._inorder(self.root)
        else:
            raise NotImplementedError("method must be 'inorder'")

    def __repr__(self):

        def recurse(node, level=0, is_last=True):
            prefix = ''
            if level > 0:
                prefix = '    ' * (level - 1) + ('└── ' if is_last else '┌── ')
            representation = prefix + str(node.key) + '\n'
            children = [child for child in [node.left, node.right] if child]
            for i, child in enumerate(children):
                is_last_child = i == len(children) - 1
                representation += recurse(child, level + 1, is_last_child)
            return representation 

        return recurse(self.root)

    def _recursive_insert(self, key, val) -> BSTNode:
        if not self.root:
            self.root = BSTNode(key, val)
            return self.root
        
        def recurse(node, key, val):
            if not node:
                return BSTNode(key, val)
            
            if key < node.key:
                node.left = recurse(node.left, key, val)
            elif key > node.key:
                node.right = recurse(node.right, key, val)
            else:
                # Key already exists. Update value
                node.val = val
            return node

        return recurse(self.root, key, val)
    
    def _iterative_insert(self, key, val):
        
        if not self.root:
            self.root = BSTNode(key, val)
            return self.root
        
        parent = None
        node = self.root

        # Find the spot to insert the node at
        while node:
            parent = node
            if key < node.key:
                node = node.left
            elif key > node.key: 
                node = node.right
            else:
                # key already exists. Update value
                node.val = val
                return self.root
        
        # Create and insert the new node
        
        if key <= parent.key:
            parent.left = BSTNode(key, val)
        else:
            parent.right = BSTNode(key, val)

        return self.root

    def insert(self, key, val):
        if self.method == "recursive":
            self._recursive_insert(key, val)
        elif self.method == "iterative":
            self._iterative_insert(key, val)
        else:
            raise NotImplementedError("method must be one of 'recursive' or 'iterative'")

    def _iterative_search(self, key):

        curr = self.root
        while curr:
            if key < curr.key:
                curr = curr.left
            elif key > curr.key:
                curr = curr.right
            else:
                # Node exists in BST
                return curr
        
        # Node does not exist in BST
        return None
    
    def _recursive_search(self, key):

        def recurse(node, key):
            if not node:
                return None
            if key < node.key:
                return recurse(node.left, key)
            elif key > node.key:
                return recurse(node.right, key)
            else:
                return node

        return recurse(self.root, key)

    def search(self, key):
        if self.method == "iterative":
            return self._iterative_search(key)
        elif self.method == "recursive":
            return self._recursive_search(key)
        else:
            raise NotImplementedError("method must be one of 'iterative' or 'recursive'")

        
    def _iterative_delete(self, key):
        curr = self.root
        prev = None

        # Find the node to delete and obtain its parent
        while curr and curr.key != key:
            prev = curr
            if key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        # Curr is now placed at the node to delete
        
        if not curr:
            # Node not found
            return None
        
        # Node has at most 1 child
        if not curr.left or not curr.right:
            # Replaces the node to be deleted
            replacement = None

            # Right child does not exist
            if curr.left:
                replacement = curr.left
            else:
                replacement = curr.right

            # Node to delete is the root
            if not prev:
                self.root = replacement
                return replacement
            # Node to delete is a left child
            elif prev.left == curr:
                prev.left = replacement
            # Node to delete is a right child
            else:
                prev.right = replacement
            curr = None
        # Node has 2 children to delete
        else:
            
            # Find inorder successor
            successor = curr.right
            succ_parent = curr
            while successor.left:
                succ_parent = successor
                successor = successor.left

            # Replace the node to delete with its inorder successor
            curr.key = successor.key
            curr.val = successor.val

            # Delete the inorder successor
            if successor.right:
                succ_parent.left = successor.right
            else:
                succ_parent.left = None
        
        return self.root

    def _recursive_delete(self, key):
        pass
    
    def delete(self, key):
        if self.method == "iterative":
            return self._iterative_delete(key)
        elif self.method == "recursive":
            raise NotImplementedError("recursive delete not implemented yet")	
        else:
            raise NotImplementedError("method must be one of 'iterative' or 'recursive'")
        
        



if __name__ == "__main__":
    tree = BSTMap()
    
    tree.insert(3, "three")
    tree.insert(1, "one")
    tree.insert(5, "five")
    tree.insert(2, "two")
    tree.insert(4, "four")
    tree.insert(6, "six")
    tree.insert(7, "seven")
    tree.insert(0, "zero")
    tree.insert(4.5, "four and a half")
    tree.insert(8, "eight")
    tree.insert(9, "nine")
    tree.insert(6.5, "six and a half")

    print(tree)
    print(tree.traverse())
    print(tree.search(7))

    

