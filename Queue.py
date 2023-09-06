class QueueIsEmpty:
    pass


class MyQueue:
    def __init__(self):
        self._queue = []
        self._songs = set()
        self.position = 0
        self.length = 0
        self.repeat = False

    def is_empty(self):
        return len(self._queue) == 0

    def get_length(self):
        return self.length

    def increase_position(self):
        self.position += 1

    def get_position(self):
        return self.position

    def change_repeatable(self):

        self.repeat = not self.repeat
        return self.repeat

    def add(self, songname, source):
        if songname not in self._songs:
            self._queue.append((songname, source))
            self._songs.add(songname)
            self.length += 1

    def get_next_track(self):
        if self.is_empty():
            raise None

        else:
            self.position += 1
            print(self.position)
            print(self.length)
            if self.position > len(self._queue):
                if self.repeat:
                    self.position = 1
                else:
                    self.purge()
                    return None

            return self._queue[self.position - 1][1]


    def list_queue(self):
        lst = []
        for i in self._queue:
            lst.append(i[0])

        str_list = "\n".join(lst)
        return "The list is: \n" + str_list

    def purge(self):
        self._queue = []
        self.position = 0
        self._songs = set()
        self.length = 0
