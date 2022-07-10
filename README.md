
# socket_utils

Various utils I used/made while experimenting with socket programming in python.
The other files can be considered prototypes for client.py and multiclient.py which together form a star topology network; with the object defined in multiclient.py acting as a relay between client objects.



\<ServerClient\> objects connect to a <Server> object and are stored in order of said connection. First connection at index 0, second at 1, etc.

Inputs to \<ServerClient\> should consist of:
- \<index\>;\<message\>
  - Will send \<message\> to the \<ServerClient\> connection at index \<index\>
- \<message\>
  -  Will send \<message\> to all clients (including it self)
- /\<command\>
  -  Intercept for server to run a command (the only one implemented is /con which displays all current connections in order)


## Demo
See below for demonstration of these two objects:

![](Resources/server%20demo.gif)
