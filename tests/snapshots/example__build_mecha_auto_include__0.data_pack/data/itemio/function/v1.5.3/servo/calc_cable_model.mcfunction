
scoreboard players operation #model_final_temp itemio.math = #model_final itemio.math

execute store result score #rotation_0 itemio.math run data get entity @s Rotation[0]
execute store result score #rotation_1 itemio.math run data get entity @s Rotation[1]

execute if score #rotation_0 itemio.math matches 0 if score #rotation_1 itemio.math matches 90 run function itemio:v1.5.3/servo/calc_cable_model/down

execute if score #rotation_0 itemio.math matches 0 if score #rotation_1 itemio.math matches -90 run function itemio:v1.5.3/servo/calc_cable_model/up

execute if score #rotation_0 itemio.math matches 180 if score #rotation_1 itemio.math matches 0 run function itemio:v1.5.3/servo/calc_cable_model/north

execute if score #rotation_0 itemio.math matches 0 if score #rotation_1 itemio.math matches 0 run function itemio:v1.5.3/servo/calc_cable_model/south

execute if score #rotation_0 itemio.math matches 90 if score #rotation_1 itemio.math matches 0 run function itemio:v1.5.3/servo/calc_cable_model/west

execute if score #rotation_0 itemio.math matches 270 if score #rotation_1 itemio.math matches 0 run function itemio:v1.5.3/servo/calc_cable_model/east
