<h1 align="center">
  django-social-oauth-token
</h1>

<p align="center">
  <a href="https://github.com/khasbilegt/django-social-oauth-token/">
    <img src="https://img.shields.io/github/workflow/status/khasbilegt/django-social-oauth-token/CI?label=CI&logo=github&style=for-the-badge" alt="ci status">
  </a>
  <a href="https://pypi.org/project/django-social-oauth-token/">
    <img src="https://img.shields.io/pypi/v/django-social-oauth-token?style=for-the-badge" alt="pypi link">
  </a>
  <a href="https://codecov.io/github/khasbilegt/django-social-oauth-token">
    <img src="https://img.shields.io/codecov/c/github/khasbilegt/django-social-oauth-token?logo=codecov&style=for-the-badge" alt="codecov">
  </a>
  <br>
  <a>
    <img src="https://img.shields.io/pypi/pyversions/django-social-oauth-token?logo=python&style=for-the-badge" alt="supported python versions">
  </a>
  <a>
    <img src="https://img.shields.io/pypi/djversions/django-social-oauth-token?logo=django&style=for-the-badge" alt="supported django versions">
  </a>
</p>

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#license">License</a>
</p>

<p align="center">OAuthToken generation API for handling OAuth 2.0 Authentication Code Flow based on social-auth</p>

## Installation

1. Use your preferred package manager ([pip](https://pip.pypa.io/en/stable/), [poetry](https://pypi.org/project/poetry/), [pipenv](https://pypi.org/project/pipenv/)) to install the package. For example:

```bash
$ poetry add django-social-oauth-token
```

2. Then register 'social_oauth_token', in the 'INSTALLED_APPS' section of your project's settings.

```python
# settings.py
...

INSTALLED_APPS = (
    ...
    'social_oauth_token',
)

...
```

## How To Use

In order to verify the **Authorization Code** sent by the user and replace it with your own **OAuth Access Token**, send a **POST** request to the `token/<backend>/` endpoint with `client_id` and `code` to receive the token.

The POST request parameters:

```Python
client_id # OAuth Client ID
code # Authorization Code
```

The JSON response:

```json
{
  "access_token": <access_token>,
  "expires_in": <expires_in>,
  "token_type": <token_type>,
  "refresh_token": <refresh_token>,
}
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT License](https://choosealicense.com/licenses/mit/)
