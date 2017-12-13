class Locker:

    #List containing the filed that are locked by the file system
    locked_files = []

    def __init__(self):
        pass

    #"Test" the lock
    #i.e. check if the file has been locked
    def test_lock(self, file):
        if file in self.locked_files:
            return True
        else:
            return False

    #Acquire a lock for a file
    def acquire_lock(self, file):
        if not self.test_lock(file):
            self.locked_files.append(file)
            print "{0} has been locked".format(file)
            return True
        else:
            return False

    #Release a lock for a file
    def release_lock(self, file):
        if not self.test_lock(file):
            return False
        else:
            self.locked_files.remove(file)
            print "{0} has been unlocked".format(file)
            return True
