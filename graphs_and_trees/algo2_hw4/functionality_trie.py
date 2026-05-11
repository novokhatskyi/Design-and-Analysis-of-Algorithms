from my_trie import Trie

class Homework(Trie):
    def count_words_with_suffix(self, pattern) -> int:
        if not isinstance(pattern, str):
            raise TypeError(
                f"Illegal argument for count_words_with_suffix: pattern = {pattern} must be a string"
            )

        count = 0

        for word in self.keys():
            if word.endswith(pattern):
                count += 1

        return count

    def has_prefix(self, prefix) -> bool:
        if not isinstance(prefix, str):
            raise TypeError(
                f"Illegal argument for has_prefix: prefix = {prefix} must be a string"
            )

        current = self.root

        for char in prefix:
            if char not in current.children:
                return False
            current = current.children[char]

        return True


if __name__ == "__main__":
    trie = Homework()

    words = ["apple", "application", "banana", "cat"]

    for i, word in enumerate(words):
        trie.put(word, i)

    assert trie.count_words_with_suffix("e") == 1
    assert trie.count_words_with_suffix("ion") == 1
    assert trie.count_words_with_suffix("a") == 1
    assert trie.count_words_with_suffix("at") == 1
    assert trie.count_words_with_suffix("xyz") == 0

    assert trie.has_prefix("app") == True
    assert trie.has_prefix("bat") == False
    assert trie.has_prefix("ban") == True
    assert trie.has_prefix("ca") == True

    print("All tests passed!")