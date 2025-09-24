from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models import FunctionCode
from backend.executor import run_function_code
from backend.database import create_db, SessionLocal, Function
import uuid

create_db()
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/deploy/")
def deploy_function(function: FunctionCode, db: Session = Depends(get_db)):
    function_id = str(uuid.uuid4())
    db_func = Function(
        id=function_id,
        name=function.name,
        code=function.code,
        language="python",
        timeout=5
    )
    db.add(db_func)
    db.commit()
    return {"function_id": function_id}

@app.get("/functions/")
def list_functions(db: Session = Depends(get_db)):
    return db.query(Function).all()

@app.get("/function/{function_id}")
def get_function(function_id: str, db: Session = Depends(get_db)):
    func = db.query(Function).filter(Function.id == function_id).first()
    if not func:
        raise HTTPException(status_code=404, detail="Function not found")
    return func

@app.put("/function/{function_id}")
def update_function(function_id: str, update: FunctionCode, db: Session = Depends(get_db)):
    func = db.query(Function).filter(Function.id == function_id).first()
    if not func:
        raise HTTPException(status_code=404, detail="Function not found")
    func.name = update.name
    func.code = update.code
    db.commit()
    return {"msg": "Updated"}

@app.delete("/function/{function_id}")
def delete_function(function_id: str, db: Session = Depends(get_db)):
    func = db.query(Function).filter(Function.id == function_id).first()
    if not func:
        raise HTTPException(status_code=404, detail="Function not found")
    db.delete(func)
    db.commit()
    return {"msg": "Deleted"}

@app.post("/execute/{function_id}")
def execute_function(function_id: str, db: Session = Depends(get_db)):
    func = db.query(Function).filter(Function.id == function_id).first()
    if not func:
        raise HTTPException(status_code=404, detail="Function not found")
    output = run_function_code(func.code)
    return {"output": output}
