from dataclasses import asdict, dataclass
from config.config import Config


HTTP_Header = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": Config.env.get("ORIGIN_URL"),
    'Access-Control-Allow-Methods': "POST, GET, OPTIONS, DELETE, PUT",
    "Access-Control-Expose-Headers": "Authorization",
    "Access-Control-Allow-Headers": "Accept, Meta-token, meta-token, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, jwt"
}


@dataclass
class Response:
    response: dict or int or str or list
    status: int
    header: dict


@dataclass
class ErrorMessage:
    '''error message'''
    error: str


def error_handler(status: int, err='generic') -> ErrorMessage:
    '''return error message'''
    error_desc = {
        204: '',
        402: f'insufficient credits: {err}',
        401: 'Autenticazione fallita',
        404: 'Not Found',
        400: f'Request error: {err}',
        500: 'Response Error',
        4001: 'Keycloak client error'
    }
    return asdict(ErrorMessage(error=error_desc.get(status)))


HTTP_Header_options = {
    "Access-Control-Allow-Origin": Config.env.get("ORIGIN_URL"),
    'Access-Control-Allow-Methods': "POST, GET, OPTIONS, DELETE, PUT",
    "Access-Control-Expose-Headers": "Authorization",
    "Access-Control-Allow-Headers": "Accept, Meta-token, meta-token, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, jwt"
}
