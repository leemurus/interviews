"""
You are given products - list of string. Design a system that returns at most
three matches from products list for each passed searchWord. Suggested matches
should have common prefix with searchWord. If there are more than three matches
return the first three of all matches if they are sorted lexicographically.

Example:
products: ["mobile","mouse","moneypot","monitor","mousepad", "test", "test"]

m -> ["mobile","moneypot","monitor"],
mo ->["mobile","moneypot","monitor"],
mou ->["mouse","mousepad"],
mous -> ["mouse","mousepad"],
mouse -> ["mouse","mousepad"]
mouses -> []
t -> ["test","test"]
test -> ["test","test"]
testtest -> []
"""

from typing import Self


def get_letter_by_int(index: int) -> str:
    return chr(ord('a') + index)


class Node:
    def __init__(
        self,
        childs: dict[str, Self],
        value: str | None,
        number: int = 0,
    ):
        self.childs = childs
        self.value = value
        self.number = number

    def __str__(self) -> str:
        return f"Node(value={self.value})"

    def __repr__(self) -> str:
        return f"Node(value={self.value})"


class Tree:
    def __init__(self, root: Node):
        self.root = root

    @classmethod
    def build_tree(cls, words: list[str]) -> Self:
        root = Node(childs={}, value=None)

        for word in words:

            cur_node = root
            for letter in word:
                if letter not in cur_node.childs:
                    cur_node.childs[letter] = Node(childs={}, value=letter)

                cur_node = cur_node.childs[letter]

            cur_node.number += 1

        return cls(root)

    def _dfs(self, node: Node, word: str) -> list[str]:
        result = []

        if node.number:
            result = [word] * min(3, node.number)

        for index in range(26):
            if len(result) >= 3:
                return result[:3]

            letter = get_letter_by_int(index)
            if letter in node.childs:
                result.extend(
                    self._dfs(node=node.childs[letter], word=word + letter)
                )

        return result[:3]

    def find_nearest_words(self, word: str) -> list[str]:
        cur_node = self.root

        for letter in word:
            if letter not in cur_node.childs:
                return []

            cur_node = cur_node.childs[letter]

        return self._dfs(node=cur_node, word=word)


def main():
    products = [
        "mobile", "mouse", "moneypot", "monitor", "mousepad", "test", "test"
    ]

    tree = Tree.build_tree(words=products)
    print("m -> ", tree.find_nearest_words("m"))
    print("mo -> ", tree.find_nearest_words("mo"))
    print("mou -> ", tree.find_nearest_words("mou"))
    print("mous -> ", tree.find_nearest_words("mous"))
    print("mouse -> ", tree.find_nearest_words("mouse"))
    print("mouses -> ", tree.find_nearest_words("mouses"))
    print("t -> ", tree.find_nearest_words("t"))
    print("test -> ", tree.find_nearest_words("test"))
    print("testtest -> ", tree.find_nearest_words("testtest"))


if __name__ == '__main__':
    main()
