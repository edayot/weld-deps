
execute if score #itemio.major load.status matches ..1 unless score #itemio.major load.status matches 1 run function itemio:v1.5.3/test_load/enumerate/set_version
execute unless score #itemio.set load.status matches 1 if score #itemio.major load.status matches ..1 if score #itemio.major load.status matches 1 run function itemio:v1.5.3/test_load/enumerate/minor
