from dataclasses import dataclass, field
from typing import ClassVar
import html


@dataclass
class TaggedObject:
    id: int = field(init=False)
    tags: dict[str, str] = field(default_factory=dict)

    id_counter: ClassVar[int] = -1001

    def xml_tags(self, file=None, pretty_print: bool = True, indent: int = 0):
        dent = indent * " " if pretty_print else ""
        for key, value in self.tags.items():
            # TODO: Handle escaping better
            # TODO: Do stripping of values somewhere else (data models)
            print(f'{dent}<tag k="{html.escape(key)}" v="{html.escape(value).strip()}" />', file=file)

    def __post_init__(self):
        self.id = TaggedObject.id_counter
        TaggedObject.id_counter -= 1


@dataclass
class Node(TaggedObject):
    lat: float = None
    lon: float = None
    type: ClassVar[str] = "node"

    def xml(self, file=None, pretty_print: bool = True, indent: int = 0):
        if self.lat is None or self.lon is None:
            raise ValueError(f"Can't export node with unknown coordinates: lat={self.lat}, lon={self.lon}")

        dent = indent * " " if pretty_print else ""
        print(f'{dent}<node id="{self.id}" lat="{self.lat}" lon="{self.lon}">', file=file)
        self.xml_tags(file, pretty_print, indent + 2)
        print(f'{dent}</node>', file=file)


@dataclass
class Way(TaggedObject):
    nodes: list[Node] = field(default_factory=list)
    type: ClassVar[str] = "way"

    def xml(self, file=None, pretty_print: bool = True, indent: int = 0):
        dent = indent * " " if pretty_print else ""
        print(f'{dent}<way id="{self.id}">', file=file)
        for node in self.nodes:
            print(f'{dent}<nd ref="{node.id}"/>', file=file)
        self.xml_tags(file)
        print(f'{dent}</way>', file=file)


@dataclass
class RelationMember:
    object: Node | Way
    role: str

    def xml(self, file=None, pretty_print: bool = True, indent: int = 0):
        dent = indent * " " if pretty_print else ""
        print(f'{dent}<member type="{self.object.type}" ref="{self.object.id}" role="{self.role}"/>', file=file)


@dataclass
class Relation(TaggedObject):
    members: list[RelationMember] = field(default_factory=list)

    def xml(self, file=None, pretty_print: bool = True, indent: int = 0):
        dent = indent * " " if pretty_print else ""
        print(f'{dent}<relation id="{self.id}">', file=file)
        for member in self.members:
            member.xml(file)
        self.xml_tags(file)
        print(f'{dent}</relation>', file=file)


@dataclass
class Data:
    # Metadata
    api_version: str = "0.6"
    generator: str = "school2osm v1.1.0"
    upload: bool = False

    # OSM objects
    nodes: list[Node] = field(default_factory=list)
    ways: list[Way] = field(default_factory=list)
    relations: list[Relation] = field(default_factory=list)

    def xml(self, file=None, pretty_print=True):
        print('<?xml version="1.0" encoding="UTF-8"?>', file=file)
        print(f'<osm version="{self.api_version}" generator="{self.generator}" upload="{str(self.upload).lower()}">',
              file=file)

        indent = 2 if pretty_print else 0
        for node in self.nodes:
            node.xml(file, indent=indent)
        for way in self.ways:
            way.xml(file, indent=indent)
        for relation in self.relations:
            relation.xml(file, indent=indent)

        print('</osm>', file=file)
