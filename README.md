## OwnYourFiles_foto
# Own Your Files – Photos
### Keep it to yourself
#### Demo: Coming soon in browsers near you...
#### Description:

Own Your Files – Photos is developed for the need of keeping your photos to yourself...

...even when putting 'em to cloud for sharing with your peeps. Keeping "Trust no one"* principle anxiously in mind.

Own Your Files – Photos is a web API designed to be secure yet "easily" setted up into most modern cloud services.

Own Your Files – Photos lets you upload photos and manage users whom are allowed to browse and see those photos. On upload web & mobile optimized images are created and original is saved for downloads (if allowed).

## Documentation:
* to be done...

## Dependencies:
* Python 3.11
### and kudos to following magnificent projects:
* Own Your Files – Photos depends following external libraries:
    * FastAPI
        - https://fastapi.tiangolo.com/
    * FastAPI Users
        - https://fastapi-users.github.io/fastapi-users/
    * Pillow
        - https://pillow.readthedocs.io/en/stable/
    * SQLite
        - https://sqlite.org/index.html
    * aiosqlite
    * anyio
    * bcrypt
    * cffi
    * click
    * cryptography
    * dnspython
    * email-validator
    * greenlet
    * h11
    * httptools
    * idna
    * makefun
    * passlib
    * pycparser
    * pydantic
    * PyJWT
    * python-dotenv
    * python-multipart
    * PyYAML
    * six
    * sniffio
    * SQLAlchemy
    * starlette
    * typing_extensions
    * uvicorn
    * uvloop
    * watchfiles
    * websockets
* and following internal libraries:
    * base64
#### but you just ```pip install -r requirements.txt```

## Executing program for testing
* Modify ```.env-example``` file and save it as ```.env``` (remember to add .env to .gitignore)
* Run ```run_once.py``` to initialize things, see Help for command line options
    ```
    python3.11 run_once.py
    ```

* Run ```main.py```, see Help for command line options
    ```
    python3.11 main.py
    ```
* Open in browser: http://0.0.0.0:8000

## Help

* Run with -h to see command line arguments.
    ```
    python3.11 main.py -h
    ```

## Extra very special mention and huge gratitude:
[frankie567](https://github.com/frankie567) / François Voron for fastAPI Users examples and all

## Author

Samu Reinikainen
samu.reinikainen@gmail.com

## Version History

* 0.0.1
    * Initial Release

## License

This project is licensed under the MIT License





*) except Open Source