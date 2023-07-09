from httpx import Response


class MainResponse:
    def __init__(self, reponse: Response):
        self.__json = reponse.json()
        self.__status_code = reponse.status_code

    def __repr__(self):
        return self.__json, self.__status_code

    @property
    def json(self):
        return self.__json

    @property
    def status_code(self):
        return self.status_code

    def assert_status(self, code: int | list[int]):
        match code:
            case int(code):
                assert self.__status_code == code
            case list(code):
                assert self.__status_code in code
            case _:
                raise ValueError('неправильно передан код ответа')
