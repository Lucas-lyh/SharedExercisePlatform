class TrieNode:
    def __init__(self) -> None:
        self.children = {}
        self.is_end = False

    def add_child(self, child:str):
        if child not in self.children.keys():
            self.children[child] = TrieNode()
        return self.children[child]
    
    def get_child(self, child:str):
        if child in self.children.keys():
            return self.children[child]
        return None
    
class SensiwordFilter:
    def __init__(self) -> None:
        self.root = TrieNode()
        
    def add_sensitive_word(self, word):
        tracker = self.root
        for w in word:
            tracker = tracker.add_child(w)
        tracker.is_end = True
    
    def check(self, sentence):
        trackers = []
        for w in sentence:
            trackers = [t.get_child(w) for t in trackers if t.get_child(w) != None]
            for tracker in trackers:
                if tracker.is_end:
                    return True
            if self.root.get_child(w):
                trackers.append(self.root.get_child(w))
        return False
    
def load_words():
    from orm import SensitiveWord
    fin = open('政治类.txt', 'r', encoding='utf-8')
    for row in fin.readlines():
        SensitiveWord(word=row.strip().strip(',')).save()
        
if __name__ == '__main__':
    load_words()



