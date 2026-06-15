def tick(world):
    move_npcs(world)
    generate_events(world)
    generate_observations(world)
    update_case_graph(world)
