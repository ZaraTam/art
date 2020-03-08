# Art of the moment

Get a new piece of artwork when you refresh the page<br>
Website: https://art-of-the-moment.herokuapp.com/

Art of the moment is a Flask web app hosted on Heroku

Artworks are powered by [Artsy](https://www.artsy.net/) via its [Public API](https://developers.artsy.net/)
<br>
<br>

## Requirements

- Python 3
- Requests
- Flask
- Jinja2
- Gunicorn
<br>

## Usage

### Clone the application

Clone over HTTPS
```sh
git clone https://github.com/ZaraTam/art.git
```

Clone over SSH
```sh
git clone git@github.com:ZaraTam/art.git
```

### Install package dependencies

```sh
pip install -r requirements.txt
```

:bulb: You will need to sign up for an Artsy developer account to get your own `client ID` and `client secret`

### Run locally on Gunicorn

```sh
gunicorn get-art:app
```
<br>

## Licence

This project is licensed under the GNU General Public License v3.0 - see [LICENSE](https://github.com/ZaraTam/art/blob/master/LICENSE) for details
