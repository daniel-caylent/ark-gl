def urlopen(url, *args, **kwargs):
    class Response:
        file = url
        def read(self, *args, **kwargs):
            with open(self.file, 'r') as f:
                text = f.read()
            return text.encode()
        
        def close(self):
            pass

    return Response()
