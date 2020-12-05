select customer.CustomerID as 'ID', customer.LastName as 'Last Name', customer.FirstName as 'First Name', sum(rents.PaymentAmount) as 'Total Amount'
from customer
inner join rents on customer.CustomerID=rents.CustomerID
group by customer.CustomerID
order by sum(rents.PaymentAmount) desc;