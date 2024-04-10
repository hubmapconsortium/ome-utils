import html
import unicodedata
from io import StringIO
from typing import Optional
from xml.etree import ElementTree as ET

from pint import Quantity, UnitRegistry

target_physical_size = "nm"
reg = UnitRegistry()


def strip_namespace_and_parse(xmlstr: str):
    it = ET.iterparse(StringIO(xmlstr))
    for _, el in it:
        _, _, el.tag = el.tag.rpartition("}")
    root = it.root
    return root


def physical_size_to_quantity(
    px_node: ET.Element,
    dimension: str,
) -> Optional[Quantity]:
    unit_str = px_node.get(f"PhysicalSize{dimension}Unit", None)
    if unit_str is None:
        print("Could not find physical unit in OMEXML for dimension", dimension)
        return None

    size_str = px_node.get(f"PhysicalSize{dimension}", None)
    if size_str is None:
        print("Could not find physical unit in OMEXML for dimension", dimension)
        return None

    unit_normalized = unicodedata.normalize("NFKC", html.unescape(unit_str))
    size = float(size_str) * reg[unit_normalized]
    return size


def convert_size_to_nm(px_node: ET.Element):
    for dimension in "XY":
        size = physical_size_to_quantity(px_node, dimension)
        if size is not None:
            size_converted = size.to(target_physical_size)
            px_node.set(f"PhysicalSize{dimension}Unit", target_physical_size)
            px_node.set(f"PhysicalSize{dimension}", str(size_converted.magnitude))


def get_physical_size_quantities(xml_str: str) -> dict[str, Quantity]:
    ome_xml: ET.Element = strip_namespace_and_parse(xml_str)
    px_node = ome_xml.find("Image").find("Pixels")
    dimensions = {}
    for dimension in "XYZ":
        size = physical_size_to_quantity(px_node, dimension)
        if size is not None:
            dimensions[dimension] = size
    return dimensions


def get_converted_physical_size(xml_str: str, target_unit: str = "um") -> dict[str, Quantity]:
    dimensions = get_physical_size_quantities(xml_str)
    return {dimension: size.to(target_unit) for dimension, size in dimensions.items()}
