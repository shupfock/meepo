from cantor.api.init import App, make_up_app, on_app_setup
from cantor.utils.logger import get_logger

logger = get_logger()


app = App()
app = make_up_app(app)


@app.on_event("startup")
async def server_startup():
    logger.info("app startup event start")
    await on_app_setup(app)
    logger.info("app startup event complete")
