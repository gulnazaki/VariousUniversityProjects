select customer.CustomerID as 'ID', customer.LastName as 'Last Name', customer.FirstName as 'First Name'
from customer INNER JOIN reserves on customer.CustomerID=reserves.CustomerID
where reserves.Paid like 'N%'
order by Lastname;