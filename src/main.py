from fastapi import FastAPI

import config

application: FastAPI = FastAPI(
    debug=config.DEBUG,
    title="Twitter clone",
    version="0.1.0",
    description="Thesis by Andrey Telitsin for Skillbox",
)
