import os

import requests
from django.core.exceptions import SuspiciousOperation


def pre_aprobado(dni: int):
    """
    Calls an external api and returns if the client is pre-approved
    :param dni: int
    :return: bool
    """
    endpoint = os.environ['PRE_APROBADO_ENDPOINT']
    credential = os.environ['PRE_APROBADO_CREDENTIAL']
    headers = {'credential': credential}
    request_url = f'{endpoint}/{dni}'
    try:
        response = requests.get(request_url, headers=headers).json()
        status = response['status']
        has_error = response['has_error']
        if status and not has_error:
            if status == 'approve':
                return 'A'
            else:
                return 'R'
        else:
            raise SuspiciousOperation('Error en el formato del documento')
    except requests.exceptions.RequestException as e:
        raise SuspiciousOperation('Error en la conexión con el servicio')
