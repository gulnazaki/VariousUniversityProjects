select Cartype as 'Type Of Vehicle', count(LicensePlate) as 'Amount'
from vehicle
group by Cartype;