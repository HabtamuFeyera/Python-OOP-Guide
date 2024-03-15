class HtmlDocument:
    version = 5
    extension = 'html'

    def __init__(self, name, contents):
        self.name = name
        self.contents = contents


blank = HtmlDocument('Blank', '')
print(blank.extension)
print(blank.version)