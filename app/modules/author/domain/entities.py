from tortoise.contrib.pydantic import pydantic_model_creator

from ..infrastructure.models import AuthorModel as _AuthorModel

AuthorIn = pydantic_model_creator(_AuthorModel, name="AuthorIn", exclude_readonly=True)
Author = pydantic_model_creator(_AuthorModel, name="Author")
