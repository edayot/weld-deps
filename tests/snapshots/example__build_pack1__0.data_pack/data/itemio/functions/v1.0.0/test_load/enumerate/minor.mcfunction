execute if score #itemio.minor load.status matches ..0 unless score #itemio.minor load.status matches 0 run function itemio:v1.0.0/test_load/enumerate/set_version
execute unless score #itemio.set load.status matches 1 if score #itemio.minor load.status matches ..0 if score #itemio.minor load.status matches 0 run function itemio:v1.0.0/test_load/enumerate/patch
