"""
Entities : Management of differente entities and their components
"""

from functools import lru_cache
from random import randint, choice
import components


class Registry:
    def __init__(self):
        self.components = {}
        self.entities = {}
        self.next_id = 2

    def create_entity(self, *components):
        entity = self.next_id
        for component in components:
            self.add_component(entity, component)
        self.next_id += 1
        return entity

    def add_component(self, entity, component):
        component_type = type(component)
        if component_type not in self.components:
            self.components[component_type] = set()

        self.components[component_type].add(entity)

        if entity not in self.entities:
            self.entities[entity] = {}
        self.entities[entity][component_type] = component
        self.cache_clear()

    @lru_cache()
    def get_single_component(self, component_type):
        return list(self.components.get(component_type, []))

    @lru_cache()
    def get_multiple_components(self, *component_types):
        entities = (self.components.get(ct, set()) for ct in component_types)
        return list(set.intersection(*entities))

    def cache_clear(self):
        self.get_single_component.cache_clear()
        self.get_multiple_components.cache_clear()

    def remove_components(self, entity, component_type):
        assert component_type in self.components, "Component not registered"
        self.components[component_type].discard(entity)
        del self.entities[entity][component_type]

        if not self.entities[entity]:
            del self.entities[entity]
        if not self.components[component_type]:
            del self.components[component_type]

        self.cache_clear()

    def remove_entity(self, entity):
        for component_type in self.entities[entity]:
            del self.components[component_type]
            if not self.components[component_type]:
                del self.components[component_type]


    def clear_registry(self):
        self.next_id = 2
        for entity in self.entities:
            del self.entities[entity]
        for component_type in self.components:
            del self.components[component_type]

        self.cache_clear()


def add_entities(dungeon, registry):
    p_room = choice(dungeon.rooms)
    y_coord, x_coord = p_room.coords
    random_y = randint(y_coord, y_coord + p_room.dims[0] - 1)
    random_x = randint(x_coord, x_coord + p_room.dims[1] - 1)
    player = registry.create_entity(components.
                                    Position(y=random_y, x=random_x),
                                    components.Player(), components.Icon("@"))
    dungeon.board[random_y][random_x] = player
