from fastapi import Response, status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, oauth2, models

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("")
def vote(vote_data: schemas.VoteSchema,
         db: Session = Depends(database.get_db),
         current_user: dict = Depends(oauth2.get_current_user)
         ):

    query = db.query(models.Vote).filter(
        models.Vote.post_id == vote_data.post_id, models.Vote.user_id == current_user["user_id"])
    vote_found = query.first()

    post = db.query(models.Posts).filter(
        models.Posts.post_id == vote_data.post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote_data.post_id} not found"
        )

    if vote_data.vote_direction==1:
        if vote_found:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT
            )
        else:
            db.add(models.Vote(post_id=vote_data.post_id,
                user_id=current_user["user_id"]))
            db.commit()
            raise HTTPException(status_code=status.HTTP_200_OK)
    else:
        if vote_found:
            query.delete(synchronize_session=False)
            db.commit()
            raise HTTPException(status_code=status.HTTP_200_OK)
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT
            )


    # if vote_found:
    #     if vote_data.vote_direction == 0:
    #         db.add(models.Vote(post_id=vote_data.post_id,
    #             user_id=current_user["user_id"]))
    #         db.commit()
    #         raise HTTPException(status_code=status.HTTP_200_OK)
    #     else:
    #         raise HTTPException(
    #             status_code=status.HTTP_409_CONFLICT
    #         )
    # else:
    #     if vote_data.vote_direction != 1:
    #         query.delete(synchronize_session=False)
    #         db.commit()
    #         raise HTTPException(status_code=status.HTTP_200_OK)
    #     else:
    #         raise HTTPException(
    #             status_code=status.HTTP_409_CONFLICT
    #         )


    # if vote_found:
    #     if vote_data.vote_direction == 0:
    #         db.add(models.Vote(post_id=vote_data.post_id,
    #             user_id=current_user["user_id"]))
    #         db.commit()
    #         raise HTTPException(status_code=status.HTTP_200_OK)
    #     else:
    #         raise HTTPException(
    #             status_code=status.HTTP_409_CONFLICT
    #         )
    # else:
    #     if vote_data.vote_direction != 1:
    #         query.delete(synchronize_session=False)
    #         db.commit()
    #         raise HTTPException(status_code=status.HTTP_200_OK)
    #     else:
    #         raise HTTPException(
    #             status_code=status.HTTP_409_CONFLICT
    #         )

    # if vote_found:
    #     if vote_data.vote_direction != 0:
    #         raise HTTPException(
    #             status_code=status.HTTP_409_CONFLICT
    #         )
    #     db.add(models.Vote(post_id=vote_data.post_id,
    #            user_id=current_user["user_id"]))
    #     db.commit()
    #     raise HTTPException(status_code=status.HTTP_200_OK)
    # else:
    #     if vote_data.vote_direction != 1:
    #         raise HTTPException(
    #             status_code=status.HTTP_409_CONFLICT
    #         )
    #     query.delete(synchronize_session=False)
    #     db.commit()
    #     raise HTTPException(status_code=status.HTTP_200_OK)
