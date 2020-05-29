from unittest.mock import patch

from pdchaoskit.scripts import get_content


@patch('pdchaoskit.scripts.get_loaded_settings')
@patch('pdchaoskit.api.endpoints.get_loaded_settings')
@patch('pdchaoskit.scripts.client_session')
def test_script(mocked_client_session, mocked_loaded_settings_endpoints, mocked_loaded_settings_provider):

    # arrange
    settings = {
        "auths": {
            "localhost:5000": {
                "type": "bearer",
                "value": "my_api_token_here"
            }
        },
        "controls": {
            "proofdock": {
                "provider": {
                    "arguments": {
                        "api_url": "https://chaosapi.proofdock.io/"
                    }
                }
            }
        }
    }
    mocked_loaded_settings_provider.return_value = settings
    mocked_loaded_settings_endpoints.return_value = settings

    mocked_client_session.return_value.__enter__.return_value.get.return_value.ok = True
    mocked_client_session.return_value.__enter__.return_value.get.return_value.text = "Script content"

    id = 'stress_cpu.sh'
    get_content(id)

    mocked_client_session.return_value.__enter__.return_value.get.assert_called_with(
        "https://chaosapi.proofdock.io/v1/scripts/{}".format(id), timeout=30)
