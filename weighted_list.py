import re
import unittest

from contracts import contract
from lxml import etree


@contract(parent_xml_element=etree._Element, type_of_element=str, name_of_attribute=str, weighted_pair_list=str)
def weighted_list_generator(parent_xml_element, type_of_element: str, name_of_attribute: str, weighted_pair_list: str):
    # Example input:
    #
    # parent_xml_element  = an etree._Element you want to add child elements to.
    #
    # type_of_element     = "OreBlock"
    #                       (or Replaces or ReplacesOre or Biome or BiomeType or...)
    #
    # name_of_attribute   = "block"
    #                       (or "name")
    #
    # weighted_pair_list  = "minecraft:grass, 1.00; minecraft:dirt, 1.00; minecraft:sand, 1.00; minecraft:gravel, 1.00; minecraft:sandstone, 1.00;"
    #
    # Example result:
    # (Note that the etree._Element is modified in place - this function does not return a value.)
    #
    # <Parent>
    #   <OreBlock block="minecraft:grass" weight="1.00"/>
    #   <OreBlock block="minecraft:dirt" weight="1.00"/>
    #   <OreBlock block="minecraft:sand" weight="1.00"/>
    #   <OreBlock block="minecraft:gravel" weight="1.00"/>
    #   <OreBlock block="minecraft:sandstone" weight="1.00"/>
    # </Parent>

    weighted_pairs = weighted_pair_list_parser(weighted_pair_list)

    for value, weight in weighted_pairs:
        attrs = {
            name_of_attribute: value,
            "weight": weight,
        }
        etree.SubElement(parent_xml_element, type_of_element, attrs)

    # This function returns nothing.
    # The xml_parent_element is modified in place.


@contract(weighted_pair_list=str)
def weighted_pair_list_parser(weighted_pair_list: str, ):
    # Given a string such as:
    # "minecraft:coal_ore,0.99; minecraft:diamond_ore,0.01;"
    #
    # This function will return a list of paired items:
    # [
    #   ["minecraft:coal_ore", "0.99"],
    #   ["minecraft:diamond_ore", "0.01"],
    #  ]
    #
    # Some basic sanity checking is performed.
    #
    #  1. All items should be pairs.
    #     "minecraft:coal_ore;" is not allowed.
    #     "minecraft:coal_ore, 1.2, 3.4;" is not allowed.
    #
    #  2. The second item of each pair should be a number.
    #     "Plains, 10;" is allowed.
    #     "Plains, ten;" is not allowed.

    stripped = re.sub(r"\s", "", weighted_pair_list)  # strip whitespace
    stripped = stripped.rstrip(";")  # strip trailing semicolons

    if len(stripped) == 0:
        return []  # Return an empty list.

    pair_strings = stripped.split(sep=";")
    weighted_pairs = [pair.split(sep=",") for pair in pair_strings]

    # Check that each pair contains two strings
    if any([len(pair) != 2 for pair in weighted_pairs]):
        raise ValueError

    # Check that second item of each pair represents a number
    for a, b in weighted_pairs:
        try:
            float(b)
        except ValueError:
            raise

    return weighted_pairs


class TestWeightedPairListParser(unittest.TestCase):
    def test_one_pair(self):
        weighted_pair_list = "iron,0.95;"
        expected = [["iron", "0.95"]]

        parsed_pairs = weighted_pair_list_parser(weighted_pair_list)
        self.assertEqual(parsed_pairs, expected)

    def test_one_pair_syntax_errors(self):
        variations = (
            "stone",  # missing weight number
            "stone;dirt;"  # missing weighting numbers
            "stone,1.00,dirt,1.00",  # comma used to separate pairs, not semicolon
            "stone,1.00,1.00"  # pairs should only have two items, not three
        )
        for v in variations:
            with self.assertRaises(ValueError):
                parsed_pairs = weighted_pair_list_parser(v)

    def test_one_pair_variations(self):
        weighted_pair_list_variations = (
            "iron,0.95;",  # standard
            "iron, 0.95;",  # whitespace
            "iron, 0.95;\n",  # newlines
            "iron,0.95",  # no trailing semicolon
        )
        expected = [["iron", "0.95"]]
        for v in weighted_pair_list_variations:
            parsed_pairs = weighted_pair_list_parser(v)
            self.assertEqual(parsed_pairs, expected)

    def test_multiple_pairs(self):
        weighted_pair_list = "iron,0.95;gold,0.05;"
        expected = [["iron", "0.95"], ["gold", "0.05"]]

        parsed_pairs = weighted_pair_list_parser(weighted_pair_list)
        self.assertEqual(parsed_pairs, expected)

    def test_multiple_pairs_variations(self):
        weighted_pair_list_variations = (
            "iron,0.95;gold,0.05;",  # Expected
            "iron,0.95;gold,0.05",  # No trailing semicolon
            "iron,0.95;gold,0.05;;;;;;",  # Lots of trailing semicolons
            "iron, 0.95;gold, 0.05;",  # Spaces after commas
            "iron,0.95; gold,0.05; ",  # Spaces after semicolons
            "iron, 0.95; gold, 0.05;",  # Spaces after commas and semicolons
            "   iron   ,   0.95   ;   gold   ,   0.05   ;   ",  # Spaces everywhere
            " \n iron \n ,  \n0.95 \n ; \n gold \n , \n 0.05 \n ; \n ",  # newlines everywhere
        )
        expected = [["iron", "0.95"], ["gold", "0.05"]]

        for v in weighted_pair_list_variations:
            parsed_pairs = weighted_pair_list_parser(v)
            self.assertEqual(parsed_pairs, expected)


class TestWeightedListGenerator(unittest.TestCase):
    def test_typical(self):
        data = "minecraft:grass, 1.00; minecraft:dirt, 1.00; minecraft:sand, 1.00; minecraft:gravel, 1.00; minecraft:sandstone, 1.00;"

        expected = """<Parent>
  <OreBlock block="minecraft:grass" weight="1.00"/>
  <OreBlock block="minecraft:dirt" weight="1.00"/>
  <OreBlock block="minecraft:sand" weight="1.00"/>
  <OreBlock block="minecraft:gravel" weight="1.00"/>
  <OreBlock block="minecraft:sandstone" weight="1.00"/>
</Parent>
"""

        parent_xml_element = etree.Element("Parent")
        weighted_list_generator(parent_xml_element, "OreBlock", "block", data)
        output = etree.tostring(parent_xml_element, pretty_print=True, encoding="unicode")

        self.maxDiff = None
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
