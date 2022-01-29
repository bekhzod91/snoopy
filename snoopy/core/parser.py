import json
import yaml


class BaseLoader(object):
    @staticmethod
    def parse(data: str | bytes) -> dict:
        raise NotImplemented

    @staticmethod
    def dumps(data: dict) -> bytes:
        raise NotImplemented


class JsonLoader(BaseLoader):
    @staticmethod
    def parse(data: str | bytes) -> dict:
        return json.loads(data)

    @staticmethod
    def dumps(data: dict) -> bytes:
        return json.dumps(data).encode()


class YamlLoader(BaseLoader):
    @staticmethod
    def parse(data: str | bytes) -> dict:
        return yaml.load(data, Loader=yaml.Loader)

    @staticmethod
    def dumps(data: dict) -> bytes:
        return yaml.dump(data, Dumper=yaml.Dumper)
