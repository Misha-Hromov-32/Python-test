import shutil
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..core.config import get_settings
from ..data import movies_list
from ..dependencies import get_current_user
from ..models import Movietop

router = APIRouter()
templates = Jinja2Templates(directory="templates")
settings = get_settings()


@router.get("/study", response_class=HTMLResponse)
async def study_info() -> str:
    return """
    <html>
        <body>
            <h1>Информация о ВУЗе</h1>
            <p><strong>ВУЗ:</strong> БГИТУ</p>
            <p><strong>Группа:</strong> ИСТ-201</p>
            <img src="/static/photo.jpg" alt="Фото" width="300">
        </body>
    </html>
    """


@router.get("/movietop/{movie_id}", response_class=HTMLResponse)
async def get_movie_by_id(movie_id: int) -> str:
    movie = next((item for item in movies_list if item.id == movie_id), None)
    if not movie:
        return f"""
        <html>
            <body>
                <h1>Фильм не найден</h1>
                <p>Фильма с ID {movie_id} не существует.</p>
                <a href="/movies">Вернуться к списку фильмов</a>
            </body>
        </html>
        """

    poster_html = (
        f'<img src="{movie.poster_path}" alt="{movie.name}" width="300">'
        if movie.poster_path
        else "<p>Нет обложки</p>"
    )
    watched_html = "<p>✓ Просмотрен</p>" if movie.watched else "<p>Не просмотрен</p>"
    description_html = movie.description or "Не указано"

    return f"""
    <html>
        <head>
            <title>{movie.name}</title>
        </head>
        <body>
            <h1>{movie.name}</h1>
            {poster_html}
            <h2>Информация о фильме:</h2>
            <p><strong>ID:</strong> {movie.id}</p>
            <p><strong>Режиссер:</strong> {movie.director}</p>
            <p><strong>Бюджет:</strong> ${movie.cost:,}</p>
            {watched_html}
            <p><strong>Описание:</strong> {description_html}</p>
            <hr>
            <a href="/movies">Вернуться к списку фильмов</a>
        </body>
    </html>
    """


@router.get("/movies")
async def show_all_movies():
    return [movie.dict() for movie in movies_list]


@router.get("/add_film")
async def show_add_movie_form(
    request: Request,
    current_user: dict = Depends(get_current_user),
):
    return templates.TemplateResponse("add_movie.html", {"request": request})


@router.post("/add_film", status_code=status.HTTP_201_CREATED)
async def add_movie(
    name: str = Form(...),
    director: str = Form(...),
    cost: int = Form(...),
    watched: str = Form("false"),
    description_file: Optional[UploadFile] = File(default=None),
    poster: Optional[UploadFile] = File(default=None),
    current_user: dict = Depends(get_current_user),
) -> dict:
    movie_id = _generate_movie_id()
    new_movie = Movietop(
        id=movie_id,
        name=name,
        director=director,
        cost=cost,
        watched=_parse_watched_flag(watched),
        description=_save_description(description_file, movie_id),
        poster_path=_save_poster(poster, movie_id),
    )
    movies_list.append(new_movie)

    return {
        "message": "Movie successfully added.",
        "movie": new_movie.dict(),
    }


def _generate_movie_id() -> int:
    return max((movie.id for movie in movies_list), default=0) + 1


def _parse_watched_flag(value: str) -> bool:
    return value.lower() in {"true", "on", "1"}


def _save_description(description_file: Optional[UploadFile], movie_id: int) -> Optional[str]:
    if not description_file or not description_file.filename:
        return None

    extension = Path(description_file.filename).suffix
    filename = f"{movie_id}{extension}"
    path = settings.descriptions_dir / filename
    _write_upload_file(description_file, path)
    return str(path)


def _save_poster(poster: Optional[UploadFile], movie_id: int) -> Optional[str]:
    if not poster or not poster.filename:
        return None

    extension = Path(poster.filename).suffix
    filename = f"{movie_id}{extension}"
    path = settings.posters_dir / filename
    _write_upload_file(poster, path)
    return f"/static/posters/{filename}"


def _write_upload_file(upload: UploadFile, destination: Path) -> None:
    destination.parent.mkdir(exist_ok=True, parents=True)
    with destination.open("wb") as file_obj:
        shutil.copyfileobj(upload.file, file_obj)

