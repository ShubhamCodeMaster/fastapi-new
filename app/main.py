from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post,user,auth,vote

from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)
app=FastAPI()
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# @app.get('/')
# async def root():
#     # Read the contents of index.html
#     index_html_path = static_path / "index.html"
#     with open(index_html_path, "r", encoding="utf-8") as file:
#         index_html_content = file.read()

#     # Return the contents as an HTML response
#     return Response(content=index_html_content, status_code=200)






    
