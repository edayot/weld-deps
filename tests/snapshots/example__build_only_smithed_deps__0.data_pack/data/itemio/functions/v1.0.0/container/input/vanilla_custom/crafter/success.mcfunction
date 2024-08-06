data modify block ~ ~ ~ Items append from storage itemio:main.input Items_clean[]
scoreboard players set #success_input itemio.io 1
data remove storage itemio:io output
data modify storage itemio:io output set from storage itemio:io input
execute store result storage itemio:io output.count int 1 run scoreboard players get #count_input itemio.math.input
execute store result score #count_input itemio.math.input run data get storage itemio:io input.count
execute store result score #count_output itemio.math.input run data get storage itemio:io output.count
scoreboard players set #count_to_remove itemio.math.input 0
scoreboard players operation #count_to_remove itemio.math.input = #count_input itemio.math.input
scoreboard players operation #count_to_remove itemio.math.input -= #count_output itemio.math.input
scoreboard players operation #count_to_remove itemio.io = #count_to_remove itemio.math.input
