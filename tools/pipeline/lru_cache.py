

class LRUCache:

    def __init__(self, max_size = 1000, debug = False) -> None:
        self.max_size = max_size
        self.access_counter = 0

        self.results = dict()
        self.verbose_info = dict()
        self.access_counters = dict()
        self.debug = debug

    def has(self, schema: str, query: str, verbose: bool):
        key = self.generate_key(schema,query)
        if verbose:
            if key in self.results and self.verbose_info[key]:
                return True
            else:
                return False
        else:
            if key in self.results:
                return True
            else:
                return False

    def load(self, schema: str, query: str):
        key = self.generate_key(schema,query)
        if self.has(schema,query,False):
            if self.debug:
                print("Load "+key)
            result = self.results[key]
            self.access_counter+=1
            self.access_counters[key] = self.access_counters
            return result.copy()
        else:
            if self.debug:
                print("Load "+key+" - not found")
            None

    def store(self, schema: str, query: str, result, verbose: bool):
        if not self.has(schema,query,False) and len(self.results.values()) == self.max_size:
            sorted_keys = sorted(self.access_counters)
            self.evict(sorted_keys[0])
        if self.debug:
            key = self.generate_key(schema,query)
            if self.debug:
                print("Store "+key)    
            self.results[key] = result.copy()
            self.verbose_info[key] = verbose
            self.access_counter+=1
            self.access_counters[key] = self.access_counter


    def evict(self, schema: str, query: str):
        if self.has(schema,query,False):
            key = self.generate_key(schema,query)
            self.evict(key)
            
    def evict(self, key: str):
        if self.debug:
            print("Evict "+key)
        del self.results[key]
        del self.verbose_info[key]
        del self.access_counters[key]

    def evict_all(self):
        if self.debug:
            print("Evict all")
        self.access_counter = 0
        self.results.clear()
        self.verbose_info.clear()
        self.access_counters.clear()

    def generate_key(self, schema: str, query: str):
        return "{'schema':'"+schema+"', 'query':'"+query+"'}"

    
    

