
scoreboard players set #success_output itemio.io 1

$data modify storage itemio:io output set from storage itemio:main.output Items[{Slot:$(Slot)b}]

#check maxcount
execute store result score #test_count_output itemio.math.output run data get storage itemio:io output.count
execute store result score #init_count_output itemio.math.output run data get storage itemio:io output.count
execute if score #test_count_output itemio.math.output > #max_output_count itemio.io store result storage itemio:io output.count int 1 run scoreboard players get #max_output_count itemio.io

scoreboard players operation #remove_count itemio.math.output = #max_output_count itemio.io
scoreboard players operation #new_count itemio.math.output = #init_count_output itemio.math.output
scoreboard players operation #new_count itemio.math.output -= #max_output_count itemio.io
execute if score #new_count itemio.math.output matches ..0 run scoreboard players set #new_count itemio.math.output 0

execute if score #try_input_after itemio.math.output matches 1 run function #itemio:calls/try_input_after
$execute if score #remove_count itemio.math.output matches 1.. if score #nbt_items itemio.math.output matches 0 run item modify block ~ ~ ~ container.$(Slot) itemio:v1.5.3/internal/output/remove_count

execute if score #remove_count itemio.math.output matches 1.. if score #nbt_items itemio.math.output matches 1 run function itemio:v1.5.3/container/output/custom/output_noconfig/remove_count_nbt_items

execute if score #remove_count itemio.math.output matches 0 run scoreboard players set #success_output itemio.io 0
