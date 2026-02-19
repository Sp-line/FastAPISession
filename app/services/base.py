from abc import ABC, abstractmethod
from typing import Any, cast

from pydantic import BaseModel

from exceptions.db import ObjectNotFoundException
from repositories.base import RepositoryBase
from repositories.unit_of_work import UnitOfWork


class ServiceBase[
    TRepositoryBase: RepositoryBase,
    TReadSchema: BaseModel,
    TCreateSchema: BaseModel,
    TUpdateSchema: BaseModel,
    TDBCreateSchema: BaseModel,
    TDBUpdateSchema: BaseModel,
](ABC):
    def __init__(
            self,
            repository: RepositoryBase[Any, TDBCreateSchema, TDBUpdateSchema],
            unit_of_work: UnitOfWork,
            table_name: str,
            read_schema_type: type[TReadSchema],
    ) -> None:
        self._repository = cast(TRepositoryBase, repository)
        self._uof = unit_of_work
        self._table_name = table_name
        self._read_schema_type = read_schema_type

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[TReadSchema]:
        return [self._read_schema_type.model_validate(obj) for obj in await self._repository.get_all(skip, limit)]

    async def bulk_create(self, data: list[TCreateSchema]) -> list[TReadSchema]:
        prepared_data = list(map(self._prepare_create_data, data))
        async with self._uof:
            return [self._read_schema_type.model_validate(obj) for obj in await self._repository.bulk_create(prepared_data)]

    async def create(self, data: TCreateSchema) -> TReadSchema:
        prepared_data = self._prepare_create_data(data)
        async with self._uof:
            return self._read_schema_type.model_validate(await self._repository.create(prepared_data))

    async def get_by_id(self, obj_id: int) -> TReadSchema:
        if not (obj := await self._repository.get_by_id(obj_id)):
            raise ObjectNotFoundException(obj_id, self._table_name)
        return self._read_schema_type.model_validate(obj)

    async def update(self, obj_id: int, data: TUpdateSchema) -> TReadSchema:
        prepared_data = self._prepare_update_data(data)
        async with self._uof:
            new_obj = await self._repository.update(obj_id, prepared_data)
            if not new_obj:
                raise ObjectNotFoundException(obj_id, self._table_name)
            return self._read_schema_type.model_validate(new_obj)

    async def delete(self, obj_id: int) -> None:
        async with self._uof:
            if not await self._repository.delete(obj_id):
                raise ObjectNotFoundException(obj_id, self._table_name)

    @staticmethod
    @abstractmethod
    def _prepare_create_data(data: TCreateSchema) -> TDBCreateSchema:
        ...

    @staticmethod
    @abstractmethod
    def _prepare_update_data(data: TUpdateSchema) -> TDBUpdateSchema:
        ...