from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine("postgresql+asyncpg:///db.postgresql")
SessionLocal = async_sessionmaker(engine)


class Base(DeclarativeBase):
    pass


class Example(Base):
    __tablename__ = "example-table"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)


async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


class ExampleBase(BaseModel):
    username: str


app = FastAPI()


@app.post("/example")
async def index(example: ExampleBase, db: AsyncSession = Depends(get_db)):
    db_entry = Example(username=example.username)
    db.add(db_entry)
    try:
        await db.commit()
        await db.refresh(db_entry)
        return db_entry
    except IntegrityError as e:
        print(e)
        await db.rollback()
        raise HTTPException(400, detail="Duplicate username")


@app.get("/example")
async def get_data(db: AsyncSession = Depends(get_db)):
    results = await db.execute(select(Example))
    data = results.scalars().all()
    return {"db_querry": data}
