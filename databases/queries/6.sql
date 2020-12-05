select store.City as 'City', avg(vehicle.Km) as 'Average Km'
from store INNER JOIN vehicle on store.StoreID = vehicle.StoreID
group by City
order by 'Average Km';