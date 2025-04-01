from db_utils import save_to_db
from datetime import date
print("Starting test insert...")
#Sample flight fare data
sample_data =[("HYD", "DEL", date(2024, 4, 5), "IndiGo", 4999.0, "Google"),("VGA", "JAI", date(2024, 4, 6), "Air India", 5299.0, "MMT")]

#Save to database
save_to_db(sample_data)