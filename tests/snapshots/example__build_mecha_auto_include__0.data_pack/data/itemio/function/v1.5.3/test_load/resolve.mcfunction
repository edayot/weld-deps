
schedule clear itemio:v1.5.3/tick
execute if score #itemio.major load.status matches 1 if score #itemio.minor load.status matches 5 if score #itemio.patch load.status matches 3 run function itemio:v1.5.3/test_load
