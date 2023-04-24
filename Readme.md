# Distributed Shared Memory Project

## To run memory manager-

### standalone version / first memory manager - 
1. Run python3 memory_manager_caching.py <ip> <port> <number of pages>
2. eg. python3 memory_manager_caching.py 127.0.0.1 65004 5

### when one memory manager is already running - 
1. Run python3 memory_manager_caching.py <ip> <port> <number of pages> <ip of neighbour> <port of neighbour>
2. eg. python3 memory_manager_caching.py 127.0.0.1 65006 5 127.0.0.1 65004


## To run sorting.py  -
1. run the required number of memory managers
2. have access_module.py in the same folder.
3. run python3 sorting.py 
4. provide input for memory manager ip and port
5. give the cumulative number of pages you need


## To run group_chat.py - 
1. for each member in chat first run a memory manager
2. have access_module.py in the same folder.
3. run python3 group_chat.py
4. provide input for memory manager ip and port
5. give the required name for user
6. read and write in chat according to options