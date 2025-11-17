# backend/routers/techcard_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from database.models_techcard import TechCard, TechCardStage
from database.models import Group, Lesson, Teacher, LessonType
from database.schemas import TechCardUpdate, TechCardResponse
from database.dependencies import get_techcard_db, get_main_db
from utils.docx_generator import generate_techcard_docx

# ✅ СНАЧАЛА создаём роутер (это ОБЯЗАТЕЛЬНО должно быть ДО декораторов!)
router = APIRouter(
    prefix="/api/techcards",
    tags=["Технологические карты"]
)


# ✅ ТЕПЕРЬ можем использовать @router.put()
@router.put("/{techcard_id}", response_model=TechCardResponse)
def update_techcard(
        techcard_id: int,
        techcard_data: TechCardUpdate,
        db: Session = Depends(get_techcard_db)
):
    """
    Обновляет существующую технологическую карту или создаёт новую.
    """
    try:
        # Ищем существующую техкарту
        db_card = db.query(TechCard).filter(TechCard.id == techcard_id).first()

        if not db_card:
            # Создаём новую техкарту с указанным ID
            db_card = TechCard(id=techcard_id)
            db.add(db_card)
            db.flush()  # ✅ Сохраняем новую карту сразу

        # Обновляем данные основной карты
        db_card.group_id = techcard_data.group_id
        db_card.lesson_id = techcard_data.lesson_id
        db_card.teacher_id = techcard_data.teacher_id
        db_card.lesson_type_id = techcard_data.lesson_type_id
        db_card.tema = techcard_data.tema
        db_card.nomer_zanyatiya = techcard_data.nomer_zanyatiya
        db_card.ped_tech = techcard_data.ped_tech
        db_card.cel_zanyatiya = techcard_data.cel_zanyatiya
        db_card.zadachi_obuch = techcard_data.zadachi_obuch
        db_card.zadachi_razv = techcard_data.zadachi_razv
        db_card.zadachi_vosp = techcard_data.zadachi_vosp
        db_card.prognoz_result = techcard_data.prognoz_result
        db_card.oborudovanie = techcard_data.oborudovanie
        db_card.istochniki = techcard_data.istochniki

        # ✅ Применяем изменения основной карты
        db.flush()

        # Удаляем старые этапы
        db.query(TechCardStage).filter(
            TechCardStage.tech_card_id == techcard_id
        ).delete(synchronize_session=False)

        # ✅ Применяем удаление
        db.flush()

        # Добавляем новые этапы
        for stage_data in techcard_data.stages:
            stage = TechCardStage(
                tech_card_id=techcard_id,
                nomer_etapa=stage_data.nomer_etapa,
                nazvanie_etapa=stage_data.nazvanie_etapa,
                cel_etapa=stage_data.cel_etapa,
                dlitelnost=stage_data.dlitelnost,
                deyatelnost_prepod=stage_data.deyatelnost_prepod,
                deyatelnost_obuch=stage_data.deyatelnost_obuch,
                formiruemye_kompetencii=stage_data.formiruemye_kompetencii
            )
            db.add(stage)

        # ✅ Сохраняем ВСЕ изменения
        db.commit()

        # ✅ Обновляем объект из БД
        db.refresh(db_card)

        return db_card

    except Exception as e:
        # ✅ При ошибке откатываем изменения
        db.rollback()
        print(f"Ошибка при обновлении техкарты: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка обновления: {str(e)}")


@router.get("/download")
def download_techcard(
        db: Session = Depends(get_techcard_db),
        main_db: Session = Depends(get_main_db)
):
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


@router.get("/{techcard_id}", response_model=TechCardResponse)
def get_techcard(techcard_id: int, db: Session = Depends(get_techcard_db)):
    """
    Получает технологическую карту по ID.
    """
    db_card = db.query(TechCard).filter(TechCard.id == techcard_id).first()
    if not db_card:
        raise HTTPException(status_code=404, detail="Технологическая карта не найдена")
    return db_card
