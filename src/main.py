from prefect import flow
from tasks.task_extract import task_extract
from tasks.task_load import task_load

@flow(name="ETL OFERTAS LABORALES DE LINKEDIN")
def main_flow():
    extracted_data = task_extract()
    task_load(extracted_data)
    
if __name__ == "__main__":
    main_flow()