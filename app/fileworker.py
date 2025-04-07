import os

class FileWorker:
    def __init__(self, route=""):
        self.route = route

    def createFile(self, text):
        try:
            with open(self.route + ".txt", "w", encoding="utf-8") as f:
                f.write(text.strip().replace("\n", "<br/>"))
        except Exception as e:
            print("Не удалось записать в файл. Ошибка: " + str(e))

    def readFile(self, path):
        try:
            with open(path + ".txt", "r", encoding="utf-8") as f:
                return ''.join([i.strip() for i in f.readlines()])
        except Exception as e:
            print("Не удалось открыть файл. Ошибка: " + str(e))
    
    def remove(self, path):
        try:
            os.remove(path)
            return (True, "Файл удален!")
        except Exception as e:
            return (False, "Не удалось удалить файл!")