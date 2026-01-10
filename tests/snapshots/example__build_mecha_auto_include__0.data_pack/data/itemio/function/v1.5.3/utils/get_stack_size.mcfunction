
# Receive an item in 
# storage itemio:main get_stack_size
# return the stack size of the item, with 1 as fallback
# Used entity : a97c9c67-fde0-4b89-926d-54fa4a866004

execute if data storage itemio:main get_stack_size.components."minecraft:max_stack_size" run return run data get storage itemio:main get_stack_size.components."minecraft:max_stack_size"

execute as a97c9c67-fde0-4b89-926d-54fa4a866004 run return run function itemio:v1.5.3/utils/get_stack_size/fallback

return 1
