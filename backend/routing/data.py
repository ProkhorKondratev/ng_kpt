from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
from fastapi.exceptions import HTTPException
from services import Handler, Repository
from models import TaskModel, GroupModel

router = APIRouter()


@router.get("/tasks")
async def get_tasks():
    try:
        tasks_db = await Repository.get_tasks()
        tasks = [TaskModel.model_validate(task, from_attributes=True) for task in tasks_db]
        return [task.model_dump() for task in tasks]
    except Exception as e:
        # raise HTTPException(status_code=500, detail=str(e))
        raise e


@router.get("/tasks/{task_id}")
async def get_task(task_id: int):
    try:
        taskDB = await Repository.get_task(task_id)
        task = TaskModel.model_validate(taskDB, from_attributes=True)
        return task.model_dump()
    except Exception as e:
        # raise HTTPException(status_code=500, detail=str(e))
        raise e


@router.get("/groups")
async def get_groups():
    try:
        groups_db = await Repository.get_groups()
        groups = [GroupModel.model_validate(group) for group in groups_db]
        return [group.model_dump() for group in groups]
    except Exception as e:
        # raise HTTPException(status_code=500, detail=str(e))
        raise e


@router.get("/groups/{group_id}")
async def get_group(group_id: int):
    try:
        group_db = await Repository.get_group(group_id)
        group = GroupModel.model_validate(group_db)
        return group.model_dump()
    except Exception as e:
        # raise HTTPException(status_code=500, detail=str(e))
        raise e


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    try:
        await Handler.delete_task(task_id)
        return JSONResponse(status_code=200, content={"message": "Задача успешно удалена"})
    except Exception as e:
        # raise HTTPException(status_code=500, detail=str(e))
        raise e


@router.delete("/groups/{group_id}")
async def delete_group(group_id: int):
    try:
        await Handler.delete_group(group_id)
        return JSONResponse(status_code=200, content={"message": "Группа успешно удалена"})
    except Exception as e:
        # raise HTTPException(status_code=500, detail=str(e))
        raise e


@router.get("/statistics")
async def get_statistics():
    try:
        statistics = await Repository.get_statistics()
        return statistics
    except Exception as e:
        # raise HTTPException(status_code=500, detail=str(e))
        raise e


@router.get("/tasks/{task_id}/download")
async def download_task(task_id: int):
    try:
        task = await Repository.get_task(task_id)
        if task.kpt_file:
            return FileResponse(task.kpt_file, filename=task.name + ".zip")
        else:
            raise HTTPException(status_code=404, detail="Запрошенный файл не найден")
    except Exception as e:
        # raise HTTPException(status_code=500, detail=str(e))
        raise e


@router.get("/groups/{group_id}/download")
async def download_group(group_id: int):
    try:
        file = await Handler.download_group(group_id)
        return FileResponse(file)
    except Exception as e:
        # raise HTTPException(status_code=500, detail=str(e))
        raise e
