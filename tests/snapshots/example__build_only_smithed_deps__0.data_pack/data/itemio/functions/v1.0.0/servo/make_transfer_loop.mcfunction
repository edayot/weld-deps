execute if score #if_items_defined itemio.math matches 1 run function itemio:v1.0.0/servo/make_transfer_items
execute if score #if_items_defined itemio.math matches 0 run function itemio:v1.0.0/servo/make_transfer_normal
scoreboard players remove #nb_retry itemio.math 1
execute if score #nb_retry itemio.math matches 1.. run function itemio:v1.0.0/servo/make_transfer_loop
