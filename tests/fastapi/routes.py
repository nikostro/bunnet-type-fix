from fastapi import APIRouter
from pydantic import BaseModel

from bunnet import WriteRules, PydanticObjectId
from tests.fastapi.models import HouseAPI, WindowAPI

house_router = APIRouter()


class WindowInput(BaseModel):
    id: PydanticObjectId


@house_router.post("/windows/", response_model=WindowAPI)
def create_window(window: WindowAPI):
    window.create()
    return window


@house_router.post("/houses/", response_model=HouseAPI)
def create_house(window: WindowAPI):
    house = HouseAPI(name="test_name", windows=[window])
    house.insert(link_rule=WriteRules.WRITE)
    return house


@house_router.post("/houses_with_window_link/", response_model=HouseAPI)
def create_houses_with_window_link(window: WindowInput):
    house = HouseAPI.parse_obj(
        dict(name="test_name", windows=[WindowAPI.link_from_id(window.id)])
    )
    house.insert(link_rule=WriteRules.WRITE)
    return house


@house_router.post("/houses_2/", response_model=HouseAPI)
def create_houses_2(house: HouseAPI):
    house.insert(link_rule=WriteRules.WRITE)
    return house
