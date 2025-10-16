from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from database.models_techcard import TechCard, TechCardStage
from database.models import Group, Lesson, Teacher, LessonType
from database.schemas import TechCardUpdate, TechCardResponse
from database.dependencies import get_techcard_db, get_main_db
from routers.dictionaries_router import router
from utils.docx_generator import generate_techcard_docx


@router.get("/download")
def download_techcard(db: Session = Depends(get_techcard_db), main_db: Session = Depends(get_main_db)):
    """
    Генерирует .docx файл из данных технологической карты и отдаёт его для скачивания.
    """
    db_card = db.query(TechCard).filter(TechCard.id == 1).first()
    if not db_card or not db_card.tema:
        raise HTTPException(status_code=404, detail="Технологическая карта не заполнена")

    # Получаем названия справочных значений
    group_name = main_db.query(Group).filter(Group.primary_key == db_card.group_id).first()
    lesson_name = main_db.query(Lesson).filter(Lesson.primary_key == db_card.lesson_id).first()
    teacher_name = main_db.query(Teacher).filter(Teacher.primary_key == db_card.teacher_id).first()
    lesson_type_name = main_db.query(LessonType).filter(LessonType.primary_key == db_card.lesson_type_id).first()

    # Преобразуем объекты в строки
    group_name = group_name.group_name if group_name else ""
    lesson_name = lesson_name.name_lesson if lesson_name else ""
    teacher_name = teacher_name.full_name if teacher_name else ""
    lesson_type_name = lesson_type_name.lesson_type if lesson_type_name else ""

    # Генерируем файл
    file_stream = generate_techcard_docx(
        db_card,
        group_name,
        lesson_name,
        teacher_name,
        lesson_type_name
    )

    # Отдаём файл пользователю
    return StreamingResponse(
        file_stream,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=tekhnologicheskaya_karta.docx"}
    )
