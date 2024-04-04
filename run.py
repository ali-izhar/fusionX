# https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/13985
import import_hook 

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
