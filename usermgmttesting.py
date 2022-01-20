import pandas
from usermgmt import usermgmt
print(usermgmt.adduser('andrewe', 'passworde'))
print(usermgmt.authenticate('andrewe', 'passworde'))