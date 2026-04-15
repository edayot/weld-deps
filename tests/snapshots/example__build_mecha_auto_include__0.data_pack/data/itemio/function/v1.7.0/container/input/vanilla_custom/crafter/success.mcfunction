
# Step by step algo :
# - first, clean the crafter items, the output contains air slot AND nbt matching items (others are just not in the list)
# - then delete all slot that are currently disabled in the crafter UI from the list
# - last step to add items : 
#   - find the minimum count
#   - take all the slots with the minimum count
#   - input items one by one in each slot (veryfing the stack_limit & replacing air by the inputed item)
#   - repeat the last step unless no items are found or the input is empty
# - if a modification as been made, modify the Items in the block & add all I/O

data remove storage itemio:main.input Items_clean[{id: "do_not_useFDSDFS"}]
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
