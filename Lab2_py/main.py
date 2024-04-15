class Node:
    def __init__(self):
        self.keys = []
        self.parent = None

class Leaf(Node):
    def __init__(self):
        super().__init__()
        self.records = []
        self.next = None


class InternalNode(Node):
    def __init__(self):
        super().__init__()
        self.children = []

class BPlusTree:
    def __init__(self, order=4):
        self.root = Leaf()
        self.order = order

    def insert(self, key, value, phone):
        node = self.root
        while isinstance(node, InternalNode):
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            node = node.children[i]
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            node.records[i].append((value, phone))
        else:
            node.keys.insert(i, key)
            node.records.insert(i, [(value, phone)])
        if len(node.keys) > self.order:
            self.split_leaf(node)

    def split_leaf(self, leaf):
        new_leaf = Leaf()
        mid = len(leaf.keys) // 2
        new_leaf.keys = leaf.keys[mid:]
        new_leaf.records = leaf.records[mid:]
        leaf.keys = leaf.keys[:mid]
        leaf.records = leaf.records[:mid]
        if leaf.next:
            new_leaf.next = leaf.next
        leaf.next = new_leaf
        new_leaf.parent = leaf.parent
        self.insert_internal(leaf.parent, leaf, new_leaf, new_leaf.keys[0])

    def insert_internal(self, parent, left_child, right_child, key):
        if parent is None:
            new_root = InternalNode()
            new_root.keys = [key]
            new_root.children = [left_child, right_child]
            self.root = new_root
            left_child.parent = new_root
            right_child.parent = new_root
            return
        i = 0
        while i < len(parent.keys) and key > parent.keys[i]:
            i += 1
        parent.keys.insert(i, key)
        parent.children.insert(i + 1, right_child)
        right_child.parent = parent
        if len(parent.keys) > self.order:
            self.split_internal(parent)

    def split_internal(self, node):
        new_node = InternalNode()
        mid = len(node.keys) // 2
        median_key = node.keys[mid]

        new_node.keys = node.keys[mid + 1:]
        new_node.children = node.children[mid + 1:]
        for child in new_node.children:
            child.parent = new_node

        node.keys = node.keys[:mid]
        node.children = node.children[:mid + 1]

        if node == self.root:
            new_root = InternalNode()
            new_root.keys = [median_key]
            new_root.children = [node, new_node]
            self.root = new_root
            node.parent = new_root
            new_node.parent = new_root
        else:
            new_node.parent = node.parent
            self.insert_internal(node.parent, node, new_node, median_key)

    def search(self, key):
        node = self.root
        while isinstance(node, InternalNode):
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return node.records[i]
        return None

    def find_names_greater_or_less_than(self, name, greater=True):
        hashed_name = hash_name(name)
        results = []

        node = self.root
        while isinstance(node, InternalNode):
            node = node.children[0]

        while node:
            for i, key in enumerate(node.keys):
                if (greater and key > hashed_name) or (not greater and key < hashed_name):
                    results.extend(node.records[i])
            node = node.next

        return results

    def delete(self, name):
        hashed_name = hash_name(name)

        node = self.root
        while isinstance(node, InternalNode):
            i = 0
            while i < len(node.keys) and hashed_name >= node.keys[i]:
                i += 1
            node = node.children[i]

        i = 0
        while i < len(node.keys) and hashed_name > node.keys[i]:
            i += 1
        if i < len(node.keys) and hashed_name == node.keys[i]:
            del node.records[i]
            del node.keys[i]

            if len(node.keys) < (self.order + 1) // 2:
                self.rebalance_leaf(node)
        else:
            print("Name not found for deletion")

    def rebalance_leaf(self, leaf):
        left_sibling, right_sibling = self.get_siblings(leaf)
        parent = leaf.parent

        if left_sibling and len(left_sibling.keys) > (self.order + 1) // 2:
            last_key = left_sibling.keys.pop()
            last_record = left_sibling.records.pop()
            leaf.keys.insert(0, last_key)
            leaf.records.insert(0, last_record)

            parent.keys[parent.children.index(leaf) - 1] = leaf.keys[0]
        elif right_sibling and len(right_sibling.keys) > (self.order + 1) // 2:
            first_key = right_sibling.keys.pop(0)
            first_record = right_sibling.records.pop(0)
            leaf.keys.append(first_key)
            leaf.records.append(first_record)

            parent.keys[parent.children.index(right_sibling) - 1] = right_sibling.keys[0]
        elif left_sibling:
            left_sibling.keys.extend(leaf.keys)
            left_sibling.records.extend(leaf.records)
            left_sibling.next = leaf.next

            parent.keys.remove(leaf.keys[0])
            parent.children.remove(leaf)
        elif right_sibling:
            leaf.keys.extend(right_sibling.keys)
            leaf.records.extend(right_sibling.records)
            leaf.next = right_sibling.next

            parent.keys.remove(right_sibling.keys[0])
            parent.children.remove(right_sibling)

        if len(parent.keys) < (self.order + 1) // 2:
            if parent == self.root and len(parent.keys) == 0:
                self.root = leaf
                leaf.parent = None
            else:
                self.rebalance_internal(parent)

    def rebalance_internal(self, node):
        left_sibling, right_sibling = self.get_siblings(node)
        parent = node.parent

        if left_sibling and len(left_sibling.keys) > (self.order + 1) // 2:
            last_key = left_sibling.keys.pop()
            last_child = left_sibling.children.pop()
            node.keys.insert(0, parent.keys[parent.children.index(node) - 1])
            node.children.insert(0, last_child)
            last_child.parent = node
            parent.keys[parent.children.index(node) - 1] = last_key
        elif right_sibling and len(right_sibling.keys) > (self.order + 1) // 2:
            first_key = right_sibling.keys.pop(0)
            first_child = right_sibling.children.pop(0)
            node.keys.append(parent.keys[parent.children.index(node)])
            node.children.append(first_child)
            first_child.parent = node
            parent.keys[parent.children.index(node)] = first_key
        elif left_sibling:
            left_sibling.keys.append(parent.keys.pop(parent.children.index(node) - 1))
            left_sibling.keys.extend(node.keys)
            left_sibling.children.extend(node.children)
            for child in node.children:
                child.parent = left_sibling
            parent.children.remove(node)
        elif right_sibling:
            node.keys.append(parent.keys.pop(parent.children.index(node)))
            node.keys.extend(right_sibling.keys)
            node.children.extend(right_sibling.children)
            for child in right_sibling.children:
                child.parent = node
            parent.children.remove(right_sibling)

        if len(parent.keys) < (self.order + 1) // 2:
            if parent == self.root and len(parent.keys) == 0:
                self.root = left_sibling if left_sibling else node
                self.root.parent = None
            else:
                self.rebalance_internal(parent)

    def get_siblings(self, leaf):
        parent = leaf.parent
        if parent:
            index = parent.children.index(leaf)
            left_sibling = parent.children[index - 1] if index - 1 >= 0 else None
            right_sibling = parent.children[index + 1] if index + 1 < len(parent.children) else None
            return left_sibling, right_sibling
        return None, None

    def print_tree(self, node=None, indent=""):
        if node is None:
            node = self.root
        if isinstance(node, Leaf):
            print(indent + "Leaf: " + str(node.keys) + " " + str(node.records))
        else:
            print(indent + "Node: " + str(node.keys))
            for child in node.children:
                self.print_tree(child, indent + "  ")


if __name__ == '__main__':

    names = ['Alice', 'Bob', 'Caroline', 'Daniel', 'Eva', 'Fiona', 'George', 'Hannah', 'Ian', 'Julia', 'Keith', 'Lena',
             'Michael', 'Natalie', 'Oscar', 'Peter', 'Rachel', 'Samuel', 'Tina', 'Victor', 'William', 'Yvonne',
             'Zachary']

    phones = ['+38' + '0' * 5 + str(index + 1) for index in range(len(names))]

    def hash_name(name):
        name = name.lower()
        max_length = max([len(n) for n in names])
        base = 26
        hash_value = 0
        for i, char in enumerate(name):
            if i >= max_length:
                break
            hash_value += (ord(char) - ord('a')) * (base ** (max_length - i - 1))

        return hash_value

    tree = BPlusTree()

    for index, name in enumerate(names):
        hashed_name = hash_name(name)
        tree.insert(hashed_name, name, phones[index])

    tree.print_tree()

    print()
    for index, name in enumerate(names):
        hashed_name = hash_name(name)
        records = tree.search(hashed_name)
        if records is not None:
            for record in records:
                print(f'Found name -> {record[0]}, Phone: {record[1]}')
        else:
            print(f'Name {name} is not found')

    name = 'Volodymyr'
    hashed_name = hash_name(name)

    records = tree.search(hashed_name)
    if records is not None:
        for record in records:
            print(f'Found name -> {record[0]}, Phone: {record[1]}')
    else:
        print(f'Name {name} is not found')

    print()
    greater_names = tree.find_names_greater_or_less_than('Lena', greater=True)
    print("Names greater than Lena:", greater_names)

    less_names = tree.find_names_greater_or_less_than('Lena', greater=False)
    print("Names less than Lena:", less_names)

    print()
    tree.delete('Lena')
    tree.delete('Oscar')
    tree.delete('Ian')

    tree.print_tree()