from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel,Field, computed_field
from typing import Annotated,Literal, Optional

app=FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(...,description='ID of the Patient ', example="P001")]
    name: Annotated[str, Field(...,description='Name of the Patient ', example="John Doe")]
    city:Annotated[str, Field(...,description='City of the Patient ', example="New York")]
    age: Annotated[int,[Field(...,gt=0,lt=120,description='Age of the Patient ', example=30)]]
    gender:Annotated[Literal['male','female','others'],Field(...,description="Gender of the Patient", example="male")]
    height: Annotated[float,Field(...,gt=0,description='Height of the Patient in m', example=1.75)]
    weight: Annotated[float,Field(...,gt=0,description='Weight of the Patient in kg', example=70.5)]
    # bmi: float

    @computed_field
    @property
    def bmi(self) -> float:
        bmi=round(self.weight / (self.height ** 2), 2)   
        return bmi
    
    @computed_field
    @property
    def verdict(self) ->str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 24.9<self.bmi < 30:
            return "Overweight"
        else:
            return "Obesity"
        
class PateintUpdate(BaseModel):
    name:Annotated[Optional[str],Field(default=None)]
    city:Annotated[Optional[str],Field(default=None)]
    age:Annotated[Optional[int],Field(default=None,gt=0)]
    gender:Annotated[Optional[Literal['male','female']],Field(default=None)]
    height:Annotated[Optional[float],Field(default=None,gt=0)]
    weight:Annotated[Optional[float],Field(default=None,gt=0)]

def load_json():
    with open('patients.json', 'r') as file:
        data= json.load(file)
    
    return data

def save_json(data):
    with open('patients.json', 'w') as file:
        json.dump(data,file)

@app.get("/")
def home():
    return {"message": "Welcome to the Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "This API provides access to patient data."}

@app.get("/view")
def view():
    data = load_json()
    return data

@app.get('/patient/{patient_id}')
def get_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve",example="P001")):
    patients = load_json()

    if patient_id in patients:
        return patients[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get('/sort')
def sort_patients(sort_by: str=Query(...,description="sort on the basis of height,weight or bmi"),order:str=Query('asc',description='sort in ascending or descending order')):

    valid_field=['height','weight','bmi']

    if sort_by not in valid_field:
        raise HTTPException(status_code=400,detail=f"Invalid sort field. Must be one of {valid_field}")
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail="Invalid order. Must be 'asc' or 'desc'")
    
    data=load_json()

    sort_order=True if order=='desc' else False
    sorted_data=sorted(data.values(),key=lambda x:x[sort_by],reverse=sort_order)

    return sorted_data

@app.post('/add_patient')
def add_patient(patient: Patient):
    data=load_json()

    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient with this ID already exists")
    
    data[patient.id]=patient.model_dump(exclude=['id'])

    save_json(data)
    
    return JSONResponse(status_code=201,content={"message":"Patient added successfully", "patient":data[patient.id]})

@app.put('/update/{patient_id}')
def update_patient(patient_id: str , patient_update: PateintUpdate):
    data=load_json()

    if patient_id not in data:  
        raise HTTPException(status_code=404,detail="Patient not found")
    
    existing_patient=data[patient_id]

    updated_data=patient_update.model_dump(exclude_unset=True)

    for key,value in updated_data.items():
        existing_patient[key]=value
 

    existing_patient['id']=patient_id
    patient_pydandic_obj=Patient(**existing_patient)

    existing_patient=patient_pydandic_obj.model_dump(exclude=['id'])

    data[patient_id]=existing_patient

    save_json(data)

    return JSONResponse(status_code=200,content={"message":"Patient updated successfully"})

@app.delete('/delete/{patient_id}')
def delete_patient( patient_id: str=Path(...,description="The ID of the patient to delete",example="P001")):
    data=load_json()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient not found")
    
    del data[patient_id]

    save_json(data)

    return JSONResponse(status_code=200,content={"message":"Patient deleted successfully"})