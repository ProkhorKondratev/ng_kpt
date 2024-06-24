from fastapi import APIRouter, UploadFile, File, Form, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from services import Handler, pause_manager
from models import ProcessingParams

router = APIRouter()


@router.post("/run")
async def collect_kpt(params: ProcessingParams = Depends(ProcessingParams)):
    try:
        group_id, tasks_ids = await Handler.create_tasks(params)
        return JSONResponse(content={"group_id": group_id, "task_ids": tasks_ids})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/{task_id}/restart")
async def restart_task(task_id: int):
    try:
        await Handler.restart_task(task_id, force=True)
        return JSONResponse(content={"message": "Задача успешно перезапущена"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/groups/{group_id}/restart")
async def restart_group(group_id: int):
    try:
        await Handler.restart_group(group_id)
        return JSONResponse(content={"message": "Группа успешно перезапущена"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def status():
    return JSONResponse(content={"status": "paused" if pause_manager.is_paused() else "running"})


@router.get("/toggle")
async def toggle():
    if pause_manager.is_paused():
        pause_manager.unset_pause()
        return JSONResponse(content={"message": "Обработка возобновлена", "status": "running"})
    else:
        pause_manager.set_pause()
        return JSONResponse(content={"message": "Обработка приостановлена", "status": "paused"})
