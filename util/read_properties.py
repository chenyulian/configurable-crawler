class Properties(object):
    def __init__(self, fileName):
        self.fileName = fileName
        self.properties = {}

    def __getDict(self, key, dict, value):
        if key.find(".") > 0:
            k = key.split(".")[0]
            dict.setdefault(k, {})
            return self.__getDict(key[len(k)+1:],dict[k],value)
        else:
            dict[key] = value
            return

    def getProperties(self):
        try:
            with open(self.fileName, 'r') as properties_file:
                for line in properties_file.readlines():
                    line = line.strip().replace('\n','')
                    if line.find("#") != -1:
                        line = line[0:line.find("#")]
                    if line.find("=") > 0:
                        strs = line.split("=")
                        strs[1] = line[len(strs[0])+1:]
                        self.__getDict(strs[0].strip(), self.properties, strs[1].strip())
        except Exception as e:
            raise e
        finally:
            return self.properties
