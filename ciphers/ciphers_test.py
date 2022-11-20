class TreeNode:
    def __init__(self, key, left=None, right=None, parent=None, height=1):
        self.key = key
        self.leftChild = left
        self.rightChild = right
        self.parent = parent

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild


class BSTree:
    def __init__(self):
        self.root = None
        self.search_bool = False
        self.minumum = None

    def put(self, key):
        if self.root:
            self._put(key, self.root)
        else:
            self.root = TreeNode(key)
            self.minimum = int(self.root.key)

    def _put(self, key, cur_node):
        if key < cur_node.key:
            if cur_node.hasLeftChild():
                self._put(key, cur_node.leftChild)
            else:
                cur_node.leftChild = TreeNode(key, parent=cur_node)
        elif key > cur_node.key:
            if cur_node.hasRightChild():
                self._put(key, cur_node.rightChild)
            else:
                cur_node.rightChild = TreeNode(key, parent=cur_node)
        else:
            print('Node exist')

    def print_tree_inOrder(self):
        if self.root is not None:
            self._print_tree_inOrder(self.root)
        else:
            print('Tree Is Empty')

    def _print_tree_inOrder(self, cur_node):
        if cur_node is not None:
            self._print_tree_inOrder(cur_node.leftChild)
            print(cur_node.key)
            self._print_tree_inOrder(cur_node.rightChild)

    def print_tree_postOrder(self):
        if self.root is not None:
            self._print_tree_postOrder(self.root)
        else:
            print('Tree Is Empty')

    def _print_tree_postOrder(self, cur_node):
        if cur_node is not None:
            self._print_tree_postOrder(cur_node.leftChild)
            self._print_tree_postOrder(cur_node.rightChild)
            print(cur_node.key)

    def maxim(self):
        if not self.root:
            print('Tree Is Empty')
        else:
            self._maxim(self.root)

    def _maxim(self, cur_node):
        if cur_node.hasRightChild():
            self._maxim(cur_node.rightChild)
        else:
            print(cur_node.key)

    def minim(self):
        if not self.root:
            print('Tree Is Empty')
        else:
            self._minim(self.root)

    def _minim(self, cur_node):
        if cur_node.hasLeftChild():
            self._minim(cur_node.leftChild)
        else:
            print(cur_node.key)

    def search(self, key, cur_node):
        if not cur_node:
            pass
        elif cur_node.key == int(key):
            self.search_bool = True
        elif cur_node.key > int(key):
            self.search(key, cur_node.leftChild)
        elif cur_node.key < int(key):
            self.search(key, cur_node.rightChild)

    def print_tree_preOrder(self):
        if self.root is not None:
            self._print_tree_preOrder(self.root)
        else:
            print('Tree Is Empty')

    def _print_tree_preOrder(self, cur_node):
        if cur_node:
            print(cur_node.key)
            self._print_tree_preOrder(cur_node.leftChild)
            self._print_tree_preOrder(cur_node.rightChild)

    def height(self, cur_node):
        if not cur_node:
            return 0
        else:
            return max(self.height(cur_node.leftChild), self.height(cur_node.rightChild)) + 1

    def get_size(self):
        if self.root:
            self.size = self._get_size(self.root)
            print(self.size)
        else:
            print('Tree Is Empty')

    def _get_size(self, cur_node):
        if not cur_node:
            return 0
        else:
            return self._get_size(cur_node.leftChild) + self._get_size(cur_node.rightChild) + 1

    def get_root(self):
        print(self.root.key)


bst = BSTree()
while True:
    inp = input().split()
    if inp[0] == 'insert':
        bst.put(int(inp[1]))
    elif inp[0] == 'find':
        bst.search_bool = False
        bst.search(inp[1], bst.root)
        print(bst.search_bool)
    elif inp[0] == 'height':
        print(bst.height(bst.root))
    elif inp[0] == 'size':
        bst.get_size()
    elif inp[0] == 'min':
        bst.minim()
    elif inp[0] == 'root':
        bst.get_root()
    elif inp[0] == 'max':
        bst.maxim()
    elif inp[0] == 'print' and inp[1] == 'inOrder':
        bst.print_tree_inOrder()
    elif inp[0] == 'print' and inp[1] == 'preOrder':
        bst.print_tree_preOrder()
    elif inp[0] == 'print' and inp[1] == 'postOrder':
        bst.print_tree_postOrder()
    elif inp[0] == 'stop':
        break
    else:
        print('wrong command')