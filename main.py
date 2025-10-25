from fastapi import FastAPI, Form, Request, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import Movietop
import uvicorn
import os
import shutil
from pathlib import Path

templates = Jinja2Templates(directory="templates")
UPLOAD_DIR = Path("uploads")
POSTERS_DIR = Path("static/posters")
DESCRIPTIONS_DIR = Path("uploads/descriptions")

UPLOAD_DIR.mkdir(exist_ok=True)
POSTERS_DIR.mkdir(exist_ok=True)
DESCRIPTIONS_DIR.mkdir(exist_ok=True)

app = FastAPI(title="FastAPI", description="FastAPI приложение на порту 8165")

movie1 = Movietop(id=1, name="Криминальное чтиво", cost=8000000, director="Квентин Тарантино", watched=True)
movie2 = Movietop(id=2, name="Крестный отец", cost=6000000, director="Фрэнсис Форд Коппола", watched=True)
movie3 = Movietop(id=3, name="Темный рыцарь", cost=185000000, director="Кристофер Нолан", watched=True)
movie4 = Movietop(id=4, name="Список Шиндлера", cost=22000000, director="Стивен Спилберг", watched=True)
movie5 = Movietop(id=5, name="Форрест Гамп", cost=55000000, director="Роберт Земекис", watched=True)
movie6 = Movietop(id=6, name="Властелин колец: Возвращение короля", cost=94000000, director="Питер Джексон", watched=True)
movie7 = Movietop(id=7, name="Титаник", cost=200000000, director="Джеймс Кэмерон", watched=True)
movie8 = Movietop(id=8, name="Интерстеллар", cost=165000000, director="Кристофер Нолан", watched=True)
movie9 = Movietop(id=9, name="Аватар", cost=237000000, director="Джеймс Кэмерон", watched=True)
movie10 = Movietop(id=10, name="Побег из Шоушенка", cost=25000000, director="Фрэнк Дарабонт", watched=True)

movies_list = [movie1, movie2, movie3, movie4, movie5, movie6, movie7, movie8, movie9, movie10]

@app.get("/study", response_class=HTMLResponse)
async def study_info():
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

@app.get("/movietop/{movie_id}", response_class=HTMLResponse)
async def get_movie_by_id(movie_id: int):
    movie = None
    for m in movies_list:
        if m.id == movie_id:
            movie = m
            break
    
    if not movie:
        return """
        <html>
            <body>
                <h1>Фильм не найден</h1>
                <p>Фильма с ID {movie_id} не существует.</p>
                <a href="/movies">Вернуться к списку фильмов</a>
            </body>
        </html>
        """
    if movie.poster_path:
        poster_html = f'<img src="{movie.poster_path}" alt="{movie.name}" width="300">'
    else:
        poster_html = '<p>Нет обложки</p>'
    if movie.watched:
        watched_html = '<p>✓ Просмотрен</p>'
    else:
        watched_html = '<p>Не просмотрен</p>'
    
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
            <p><strong>Описание:</strong> {movie.description if movie.description else 'Не указано'}</p>
            <hr>
            <a href="/movies">Вернуться к списку фильмов</a>
        </body>
    </html>
    """

@app.get("/movies")
async def show_all_movies():
    return [movie.dict() for movie in movies_list]

@app.get("/add-movie")
async def show_add_movie_form(request: Request):
    return templates.TemplateResponse("add_movie.html", {"request": request})

@app.post("/add-movie")
async def add_movie(
    name: str = Form(...),
    director: str = Form(...),
    cost: int = Form(...),
    watched: str = Form("false"),
    description_file: UploadFile = File(None),
    poster: UploadFile = File(None)
):
    new_id = max([m.id for m in movies_list], default=0) + 1
    watched_bool = watched == "true"
    description = None
    if description_file and description_file.filename:
        ext = Path(description_file.filename).suffix
        path = DESCRIPTIONS_DIR / f"{new_id}{ext}"
        with open(path, "wb") as f:
            shutil.copyfileobj(description_file.file, f)
        description = str(path)
    poster_path = None
    if poster and poster.filename:
        ext = Path(poster.filename).suffix
        filename = f"{new_id}{ext}"
        path = POSTERS_DIR / filename
        with open(path, "wb") as f:
            shutil.copyfileobj(poster.file, f)
        poster_path = f"/static/posters/{filename}"
    
    new_movie = Movietop(
        id=new_id,
        name=name,
        director=director,
        cost=cost,
        watched=watched_bool,
        description=description,
        poster_path=poster_path
    )
    movies_list.append(new_movie)
    return RedirectResponse(url="/add-movie", status_code=303)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8165,
        reload=True,
        log_level="info"
    )