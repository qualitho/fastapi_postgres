from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from sqlalchemy.orm import Session

import models
from database import engine, SessionLocal

# create an app instance
app=FastAPI()

# create all tables and columns in database
models.Base.metadata.create_all(bind=engine)

# define datatypes to be used
class ChoiceBase(BaseModel):
    choice_text:str
    is_correct:bool

class QuestionBase(BaseModel):
    question_text:str
    choises:List[ChoiceBase]

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependecy=Annotated[Session, Depends(get_db)]

# define endpoints

# create questions
@app.post("/questions")
async def create_questions(question:QuestionBase, db:db_dependecy):
    db_question=models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choises:
        db_choice=models.Choices(choice_text=choice.choice_text, is_correct=choice.is_correct, question_id=db_question.id)
        db.add(db_choice)
    db.commit()

# add a choice to a question
@app.put("/questions/{questions_id}")
async def add_choices(question_id:int, choice:ChoiceBase, db:db_dependecy):
    db_question=db.query(models.Questions).filter(models.Questions.id==question_id).first()
    db_choice=models.Choices(choice_text=choice.choice_text, is_correct=choice.is_correct, question_id=db_question.id)
    db.add(db_choice)
    db.commit()

# delete a choice from a question
#TODO Make it work
@app.delete("/questions/{question_id}/{choice_id}")
async def delete_choice(question_id:int, choice_id:int, db:db_dependecy):
    db_choice=db.query(models.Choices).filter((models.Choices.question_id==question_id) & (models.Choices.id==choice_id))
    db.delete(db_choice)
    db.commit()

# query question
@app.get("/questions/{questions_id}")
async def read_question(question_id:int, db:db_dependecy):
    result=db.query(models.Questions).filter(models.Questions.id==question_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Question not found")
    return result

# query choices to a question
@app.get("/choices/{questions_id}")
async def read_choices(question_id:int, db:db_dependecy):
    result=db.query(models.Choices).filter(models.Choices.question_id==question_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="Choices not found")
    return result