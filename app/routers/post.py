from .. import models,schemas,oauth2
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List,Optional
router=APIRouter(prefix='/posts',tags=['posts'])

@router.get('/',response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user),
                limit: int = 10,skip: int = 0,search:Optional[str]=""):
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,
                                                                                            isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results


@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
async def create_posts(post:schemas.PostBase,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #new_post is dict
    new=models.Post(owner_id=current_user.id,**post.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new

@router.get('/{id}',response_model=schemas.PostOut)
def get_post(id:int,response:Response,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # post=db.query(models.Post).filter(models.Post.id==id).first()
    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,
                                                                                            isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if not post:
        response.status_code=status.HTTP_404_NOT_FOUND
        return{'message':f"post with id:{id} not found"}

    return post


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    deleted_post=post_query.first()
    if deleted_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exitst")
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail=f"not authorize to perform  requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}',response_model=schemas.PostResponse)
def update_post(id:int,post:schemas.PostBase,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    updated_post=post_query.first()
    if updated_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exitst")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                        detail=f"not authorized to peform requested action")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()