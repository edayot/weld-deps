execute if score #if_filters_define itemio.math.output matches 1 run function itemio:v1.0.0/container/auto_handled_output/test_filters
execute if score #if_filters_define itemio.math.output matches 0 if score #if_item_input itemio.math.output matches 1 run function itemio:v1.0.0/container/auto_handled_output/test_nbt
execute if score #if_filters_define itemio.math.output matches 0 if score #if_item_input itemio.math.output matches 0 run function itemio:v1.0.0/container/auto_handled_output/output
