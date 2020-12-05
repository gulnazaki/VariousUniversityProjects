select LicensePlate, datediff(curdate(), LastService) as 'Days Since Last Service', Damages, Malfunction
from vehicle order by LastService;