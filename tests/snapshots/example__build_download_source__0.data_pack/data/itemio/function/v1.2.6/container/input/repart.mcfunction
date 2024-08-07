scoreboard players set #success_input itemio.io 0
execute if score #loaded itemio.math matches 1 align xyz positioned ~0.5 ~0.5 ~0.5 run function itemio:v1.2.6/container/input/repart_2
execute if score #try_input_after itemio.math.output matches 1 run scoreboard players operation #success_transfer itemio.io = #success_input itemio.io
