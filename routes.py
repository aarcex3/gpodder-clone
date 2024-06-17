from datetime import datetime
from typing import List, Union

from fastapi import Depends, UploadFile, status
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from pydantic import ValidationError
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError

import auth
import utils
from database import get_db
from schemas import (
    CreateUserRequest,
    CreateUserResponse,
    OPMLFile,
    Podcast,
    User,
)

router = APIRouter()


@router.get(
    "/{username}/podcasts",
    response_model=List[Podcast],
    status_code=status.HTTP_200_OK,
)
async def get_user_podcasts(
        username: str,
        db: Database = Depends(get_db),
        valid_api_key: bool = Depends(auth.check_api_key),
):
    """
    ## Params
    - **username**: The username of the user
    - **api_key**: The API key of the user
    ## Returns:
    - **podcasts**: A list of podcasts
    """
    try:
        if not valid_api_key:
            raise HTTPException(status_code=401, detail="Invalid API key")
        user = db.users.find_one({"username": username})
        if user:
            if "opmlfile" in user and "podcasts" in user["opmlfile"]:
                return user["opmlfile"]["podcasts"]
            else:
                return []
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500,
                            detail="Internal server error") from Exception


@router.post("/new",
             response_model=CreateUserResponse,
             status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUserRequest, db: Database = Depends(get_db)):
    r"""
    ## Params
    - **username**: The username of the user
    - **password**: The password of the user
        - **Security Requirements**: The password must be at least 8 characters long and 
        contain at least one uppercase letter, one lowercase letter, 
        one digit and one special character.
    - **email**: The email of the user
    ## Returns:
    - **CreateUserResponse**: An object containing the username and the API key of the user
    """
    try:
        user = CreateUserRequest(**user.model_dump())
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e

    if not utils.is_secure_password(user.password):
        utils.handle_exception("Password does not meet security requirements",
                               status.HTTP_422_UNPROCESSABLE_ENTITY)
    user.password = auth.hash_password(user.password)
    if not utils.is_valid_email(user.email):
        utils.handle_exception("Invalid email address",
                               status.HTTP_422_UNPROCESSABLE_ENTITY)
    try:
        api_key = auth.generate_api_key(user.username)
        db.users.insert_one({
            "username": user.username,
            "password": user.password,
            "email": user.email,
            "api_key": api_key,
        })
        return CreateUserResponse(username=user.username, api_key=api_key)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=400,
            detail="User with this username or email already exists"
        ) from DuplicateKeyError
    except Exception:
        raise HTTPException(status_code=500,
                            detail="Internal server error") from Exception


@router.post("/{username}/sync", response_model=Union[List[Podcast], None])
async def sync_user_podcasts(
    username: str,
    podcasts: List[Podcast],
    db: Database = Depends(get_db),
    valid_api_key: bool = Depends(auth.check_api_key),
) -> Union[List[Podcast], None]:
    try:
        if not valid_api_key:
            raise HTTPException(status_code=401, detail="Invalid API key")

        user = User.model_validate(db.users.find_one({"username": username}))

        opmlfile_hash = utils.get_file_hash(podcasts)

        if user.opmlfile.hash != opmlfile_hash:
            user.opmlfile = OPMLFile(
                hash=opmlfile_hash,
                podcasts=podcasts,
                podcasts_qty=len(podcasts),
                created_at=user.opmlfile.created_at,
                updated_at=str(datetime.now()),
            )

            db.users.update_one(
                {"username": username},
                {"$set": {
                    "opmlfile": user.opmlfile.model_dump()
                }},
            )

            return user.opmlfile.podcasts

        else:
            return user.opmlfile.podcasts

    except HTTPException as http_err:
        raise http_err
    except Exception:
        raise HTTPException(status_code=500,
                            detail="Internal server error") from Exception


@router.post("/{username}/podcasts", response_model=OPMLFile)
async def upload_user_podcasts(
        username: str,
        opmlfile: UploadFile,
        db: Database = Depends(get_db),
        valid_api_key: bool = Depends(auth.check_api_key),
) -> OPMLFile:
    """
    ## Params
    - **username**: The username of the user
    - **api_key**: The API key of the user
    - **opmlfile**: The OPML file to upload
    ## Returns:
    - **podcasts**: A list of podcasts
    """
    if not valid_api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    opmlfile_content = opmlfile.file.read()
    podcasts = utils.parse_opml(opmlfile_content)
    opml_hash = utils.get_file_hash(podcasts)
    opml = OPMLFile(hash=opml_hash,
                    podcasts=podcasts,
                    podcasts_qty=len(podcasts))
    db.users.update_one({"username": username},
                        {"$set": {
                            "opmlfile": opml.model_dump()
                        }})
    opmlfile.file.close()
    return opml
