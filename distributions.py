from collections import defaultdict
from pprint import pprint

import openpyxl
from lxml import etree

from distribution_helpers import add_standard_attributes, add_debug_display_attributes, add_setting_elements
from excel_table import find_table, get_table_data
from weighted_list import weighted_list_generator

# Note to self; does lxml automatically escape special characters?

def StandardGen():
    # StandardGen
    # ==========
    # ATTRIBUTES
    # ----------
    # name               -> add_standard_attributes()
    # seed               -> add_standard_attributes()
    # block              -> Never use this - use Block elements instead
    # inherits           -> add_standard_attributes()
    # drawWireframe      -> add_debug_display_attributes()
    # wireframeColor     -> add_debug_display_attributes()
    # drawBoundBox       -> add_debug_display_attributes()
    # boundBoxColor      -> add_debug_display_attributes()
    #
    # SETTINGS ELEMENTS
    # -----------------
    # Setting: Size
    # Setting: Frequency
    # Setting: Height
    # Setting: ParentRangeLimit
    #
    # CHILD ELEMENTS
    # --------------
    # Description
    # OreBlock(s)
    # Replaces(s)
    # Biome(s)
    # StandardGen(s)
    # Veins(s)
    # Cloud(s)
    xml_element = etree.Element("StandardGen")

    raise NotImplementedError

    return xml_element


def Veins(params):
    # Veins
    # ==========
    #
    # ATTRIBUTES
    # ----------
    # name               -> add_standard_attributes()
    # seed               -> add_standard_attributes()
    # block              -> Never use this - use Block elements instead
    # inherits           -> add_standard_attributes()
    # branchType
    # drawWireframe      -> add_debug_display_attributes()
    # wireframeColor     -> add_debug_display_attributes()
    # drawBoundBox       -> add_debug_display_attributes()
    # boundBoxColor      -> add_debug_display_attributes()
    #
    # SETTINGS ELEMENTS
    # -----------------
    # Setting: OreDensity
    # Setting: OreRadiusMult
    # Setting: MotherlodeFrequency
    # Setting: MotherlodeRangeLimit
    # Setting: MotherlodeSize
    # Setting: MotherlodeHeight
    # Setting: BranchFrequency
    # Setting: BranchInclination
    # Setting: BranchLength
    # Setting; BranchHeightLimit
    # Setting: SegmentForkFrequency
    # Setting: SegmentForkLengthMult
    # Setting: SegmentLength
    # Setting: SegmentAngle
    # Setting: SegmentPitch             # New feature in COG: Revival? Not on wiki.
    # Setting: SegmentRadius
    #
    # CHILD ELEMENTS
    # --------------
    # Description
    # OreBlock(s)
    # Replaces(s)
    # Biome(s)
    # StandardGen(s)
    # Veins(s)
    # Cloud(s)



    # Create a dictionary that supplies a default value if we ask it for a key/value pair it doesn't have.
    # p = defaultdict(lambda: ":=_default_")
    p = defaultdict(lambda: None)
    # Load up the key/value pairs that we /do/ have.
    for key, value in params.items():
        p[key] = value
    del key, value

    if "Type" in p and p["Type"] == "Preset":
        xml_element = etree.Element("VeinsPreset")
    elif "Type" in p and p["Type"] == "Distribution":
        xml_element = etree.Element("Veins")
    else:
        raise ValueError

    # Set attributes of parent element.
    add_standard_attributes(xml_element, p["name"], p["seed"], p["inherits"])

    if "branchType" in p:
        xml_element.attrib["branchType"] = p["branchType"]

    add_debug_display_attributes(xml_element, p["color"])

    if "Description" in p:
        desc = etree.SubElement(xml_element,"Description")
        desc.text = p["Description"]

    # Add <Settings> elements.
    setting_names = [
        "OreDensity",
        "OreRadiusMult",
        "MotherlodeFrequency",
        "MotherlodeRangeLimit",
        "MotherlodeSize",
        "MotherlodeHeight",
        "BranchFrequency",
        "BranchInclination",
        "BranchLength",
        "BranchHeightLimit",
        "SegmentForkFrequency",
        "SegmentForkLengthMult",
        "SegmentLength",
        "SegmentAngle",
        "SegmentPitch",  # New feature in COG: Revival? Not on wiki.
        "SegmentRadius",
    ]
    add_setting_elements(p, setting_names, xml_element)

    # Add <OreBlock> elements.
    # In the spreadsheet, these are defined in the column OreBlock in a format like:
    # minecraft:coal_ore,0.99; minecraft:diamond_ore,0.01;

    if "OreBlock" in p:
        weighted_list_generator(xml_element, "OreBlock", "block", p["OreBlock"])



    # Add <Replaces> elements.

    if "Replaces" in p:
        weighted_list_generator(xml_element, "Replaces", "block", p["Replaces"])

    if "ReplacesOre" in p:
        weighted_list_generator(xml_element, "ReplacesOre", "block", p["ReplacesOre"])

    if "ReplacesRegExp" in p:
        weighted_list_generator(xml_element, "ReplacesRegExp", "block", p["ReplacesRegExp"])

    # Add <Biome> elements.

    if "Biome" in p:
        weighted_list_generator(xml_element, "Biome", "name", p["Biome"])

    # Add <Option*> elements

    return xml_element


def Cloud():
    # Cloud
    # ==========
    # ATTRIBUTES
    # ----------
    # name               -> add_standard_attributes()
    # seed               -> add_standard_attributes()
    # block              -> Never use this - use Block elements instead
    # inherits           -> add_standard_attributes()
    # drawWireframe      -> add_debug_display_attributes()
    # wireframeColor     -> add_debug_display_attributes()
    # drawBoundBox       -> add_debug_display_attributes()
    # boundBoxColor      -> add_debug_display_attributes()
    #
    # SETTINGS ELEMENTS
    # -----------------
    # Setting: ParentRangeLimit
    # Setting: DistributionFrequency
    # Setting: CloudRadius
    # Setting: CloudThickness
    # Setting: CloudSizeNoise
    # Setting: CloudHeight
    # Setting: CloudInclination
    # Setting: OreDensity
    # Setting: OreVolumeNoiseCutoff
    # Setting: OreRadiusMult
    #
    # CHILD ELEMENTS
    # --------------
    # Description
    # OreBlock(s)
    # Replaces(s)
    # Biome(s)
    # StandardGen(s)
    # Veins(s)
    # Cloud(s)
    xml_element = etree.Element("Cloud")

    raise NotImplementedError

    return xml_element


def Substitute():
    # Substitute
    # ==========
    # ATTRIBUTES
    # ----------
    # name               -> add_standard_attributes()
    # seed               -> add_standard_attributes()
    # block              -> Never use this - use Block elements instead
    # inherits           -> add_standard_attributes()
    # minHeight
    # maxHeight
    #
    # SETTINGS ELEMENTS
    # -----------------
    # (No settings)
    #
    # CHILD ELEMENTS
    # --------------
    # Description
    # OreBlock(s)
    # Replaces(s)
    # Biome(s)
    xml_element = etree.Element("Substitute")

    raise NotImplementedError

    return xml_element


test_params = {
    "Type":"Preset",
    "name": "copper",
    "seed": "1234",
    "inherits": "PresetLayeredVeins",
    "MotherlodeSize_avg": "1.234",
    "MotherlodeSize_type": "uniform",
    "BranchLength_range": "5.0",
    "OreBlock ID 3": "minecraft:iron_ore",
    "OreBlock Weight 3": "1.0",
    "color": "FFFFFF"
}
test_element = Veins(test_params)
s = (etree.tostring(test_element, pretty_print=True, encoding="unicode"))
# s = s.decode(encoding="utf-8")
print(s)

test_file_path = "./Sprocket2 Spreadsheet.xlsx"
workbook = openpyxl.load_workbook(test_file_path)
worksheet, my_table = find_table(workbook, "Veins_Presets")
table_data = get_table_data(worksheet, my_table)
# pprint(table_data)

for row in table_data:
    print("----")
    if all([v is None for v in row.values()]): # empty row
        continue
    for k in list(row.keys()):
        if row[k] is None:
            del row[k]
    xml = Veins(row)
    s = (etree.tostring(xml, pretty_print=True, encoding="unicode"))
    print(s)