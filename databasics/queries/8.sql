select CustomerID as 'ID', LastName as 'Last Name', FirstName as 'First Name' from customer
where CustomerID in
	(select CustomerID
	 from rents 
	 where Returnstate <> 'None');