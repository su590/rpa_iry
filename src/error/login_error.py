from src.error.base_error import BaseError


# 登录异常
class LoginError(BaseError):
    pass


# 登录时账密异常(账号密码错误等)
class LoginAccountError(LoginError):
    pass


# 登录时验证异常(滑块验证失败、点选验证失败等)
class LoginVerifyError(LoginError):
    pass


# 登录时短信验证异常(缺乏接收短信验证码的手机号等)
class LoginSmsError(LoginError):
    pass
