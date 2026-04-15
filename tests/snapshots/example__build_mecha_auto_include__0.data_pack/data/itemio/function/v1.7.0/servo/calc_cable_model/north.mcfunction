
scoreboard players operation #model_final_temp itemio.math /= #8 itemio.math
scoreboard players operation #model_final_temp itemio.math %= #2 itemio.math
execute if score #model_final_temp itemio.math matches 0 run scoreboard players add #model_final itemio.math 8
