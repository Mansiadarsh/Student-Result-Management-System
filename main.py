from fastapi import FastAPI , HTTPException 
from pydantic import BaseModel , Field , computed_field , field_validator 
from typing import  Annotated
import json
import os
app= FastAPI()
def save_data(data):
    with open('student.json','w') as f:
        json.dump(data , f ,indent= 4)

def load_data():
    with open('student.json', 'r')as f:
        return json.load(f)
    
class Student (BaseModel):

    name: Annotated[str, Field(description="The name of the student")]
    age: Annotated[int, Field(description="The age of the student")]

    roll_no: Annotated[int, Field(description="The roll number of the student")]
    math_marks: Annotated[int, Field(description="The math marks of the student")]
    science_marks: Annotated[int, Field(description="The science marks of the student")]
    english_marks: Annotated[int, Field(description="The english marks of the student")]
    computer_marks: Annotated[int, Field(description="The computer marks of the student")]
    physics_marks: Annotated[int, Field(description="The physics marks of the student")]
    @computed_field
    def total_marks(self) -> int:
        total = self.math_marks + self.science_marks + self.english_marks + self.computer_marks + self.physics_marks
        return total
    
    @computed_field
    def percentage(self) -> float:
        total = self.total_marks
        percent = round((total/500)*100, 2)
        return percent
    
    @computed_field
    def grade(self) -> str:
        percent = self.percentage
        if percent >= 90:
            return 'A'
        elif percent >=80:
            return 'B'
        elif percent >=70:
            return 'C'
        elif percent >=60:
            return 'D'
        else:
            return 'F'
    
    @computed_field
    def result(self) -> str:
        if self.grade =='F':
            return 'Fail'
        else:
            return 'Pass'
        
    @field_validator('age')
    @classmethod
    def validate_age(cls, value):
        if value <0 :
            raise ValueError('Age cannot be negative')
        return value
    
    @field_validator('math_marks', 'science_marks', 'english_marks', 'computer_marks', 'physics_marks')
    @classmethod
    def validate_marks(cls ,value):
        if value<0 or value >100:
            raise ValueError('Marks must be between 0 and 100')
        return value
    
@app.get('/home')
def home():
    return {"message":'this is the student management system'}

@app.post('/add_student')
def add_student(student : Student):
    data = load_data()
    data.append(student.model_dump())
    save_data(data)
    return {"message":'Student added successfully'}

@app.get('/students')
def get_students():
    data = load_data()
    return data

@app.get('/students/{roll_no}')
def get_student(roll_no : int):
    data = load_data()
    for student in data:
        if student['roll_no'] == roll_no:
            return student
    raise HTTPException(status_code=404, detail='Student not found')

@app.delete('/student/{roll_no}')
def delete_student(roll_no :int):
    data = load_data()
    for student in data:
        if student['roll_no'] == roll_no:
            data.remove(student)
            save_data(data)
            return{'message':'Student deleted successfully'}
    raise HTTPException(status_code = 400 , detail = 'Student not found')
@app.put('/student/{roll_no}')
def update_student(roll_no : int , student : Student):
    data = load_data()
    for index , s in enumerate(data):
        if s['roll_no'] == roll_no:
            data[index] = student.model_dump()
            save_data(data)
            return {'message':'Student updated successfully'}
    raise HTTPException(status_code=400, detail='Student not found')

@app.get('/topper')
def get_topper():
    data = load_data()
    if not data:
        raise HTTPException(status_code=404, detail='No students found')
    topper = max(data, key=lambda x: x['total_marks'])
    return topper

@app.get('/status')
def get_status():
    data = load_data()
    if not data:
        raise HTTPException(status_code=404, detail='No students found')
    status = {'Pass': 0, 'Fail': 0}
    for student in data:
        if student['result'] == 'Pass':
            status['Pass'] += 1
        else:
            status['Fail'] += 1
    return status

