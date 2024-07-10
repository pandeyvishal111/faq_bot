import typing
from fastapi.responses import JSONResponse



class MakeResponse:

    def __init__(
        self ,
        msg : str = None,
        success : bool = True ,
        status_code : typing.Any = 200,
        data : typing.Any = None,
        error : str = None
    ) -> None:
        self.msg = msg
        self.status_code = status_code
        self.data = data
        self.success = success
        self.error = error


    def error_response(self):
        error_dict = {
            "SUCCESS" : False,
            "MESSAGE" : "Check Error in response for deatils",
            "DATA" : self.data,
            "ERROR" : self.error
        }
        return JSONResponse(error_dict, status_code=self.status_code)


    def success_response(self):
        success_dict = {
            "SUCCESS" : self.success,
            "MESSAGE" : self.msg,
            "DATA" : self.data,
            "ERROR" : self.error
        }
        return JSONResponse(success_dict, status_code=self.status_code)
