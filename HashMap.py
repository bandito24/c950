class HashMap:
    def __init__(self, initial_length):
        self.list = []
        self.length = initial_length
        for i in range(0, initial_length):
            self.list.append([])
    # O(1) time for locate         
    def _locate_bucket(self, key):
        bucket_index = hash(key) % self.length
        return self.list[bucket_index]   
    # O(n) time complexity for for lookup because of the possible resize operation      
    def insert(self, key, value):
        bucket = self._locate_bucket(key)
        for entry in bucket:
            if entry[0] == key:
                entry[1] = value
                return True 
        bucket.append([key, value])
        if len(bucket) > 5:
            self.resize()
        return True
    # O(k) runtime where k represents the number of keyword arguments to loop over  
    def modify_item(self, key, **kwargs):
        item = self.locate(key)
        if item is not None:
            for attribute, value in kwargs.items():
                setattr(item, attribute, value)
            return True
        return False
    # O(1) time complexity--this is because bucket length resizes when
    # bucket array length is more than five. This lookup time is negligable 
    def locate(self, key):
        bucket = self._locate_bucket(key)
        for entry in bucket:
            if entry[0] == key:
                return entry[1]
        return None
   # time complexity for this step is O(n) to iterate over n existing objects
   # space complexity is O(m) where m represents the length of the new list 
    def resize(self):
        new_length = self.length * 2
        new_list = [[] for _ in range(0, new_length)]
        for buckets in self.list:
            for entry in buckets:
                key, value = entry
                new_bucket_index = hash(key) % new_length
                new_list[new_bucket_index].append([key, value])
        self.length = new_length
        self.list = new_list
        print('resizing operation complete')