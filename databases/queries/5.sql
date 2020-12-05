select City, Count(CustomerID) as 'Customers'
from customer
group by City
having Customers > 1
order by City;