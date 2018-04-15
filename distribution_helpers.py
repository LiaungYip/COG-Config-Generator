import unittest
from collections import defaultdict

from contracts import contract
from lxml import etree


@contract(xml_element=etree._Element, name="str|None", seed="str|None", inherits="str|None")
def add_standard_attributes(xml_element, name, seed=None, inherits=None):
    assert inherits in (None,
                        "PresetStandardGen",  # StandardGenPreset
                        "PresetLayeredVeins",  # VeinsPreset
                        "PresetVerticalVeins",  # VeinsPreset
                        "PresetSmallDeposits",  # VeinsPreset
                        "PresetLavaDeposits",  # VeinsPreset
                        "PresetHugeVeins",  # VeinsPreset
                        "PresetHintVeins",  # VeinsPreset
                        "PresetSparseVeins",  # VeinsPreset
                        "PresetPipeVeins",  # VeinsPreset
                        "PresetStrategicCloud",  # CloudPreset
                        "PresetStratum",  # CloudPreset
                        )

    if (name is None) or (name == "") or (name.strip() == ""):
        raise ValueError("Attempted to create a distribution without a name. All distributions must have a name.")
    else:
        xml_element.attrib["name"] = name

    if seed is not None:
        xml_element.attrib["seed"] = seed

    if inherits is not None:
        xml_element.attrib["inherits"] = inherits

        # This function modifies the xml_element in place.
        # No value is returned.


class TestAddStandardAttributes(unittest.TestCase):
    def test_typical(self):
        x = etree.Element("Veins")

        add_standard_attributes(x, "Huge_Gold_Veins", seed=None, inherits="PresetHugeVeins")
        output = etree.tostring(x, pretty_print=False, encoding="unicode")

        # note that "seed" was not provided, and is not present in the output.
        expected = '<Veins name="Huge_Gold_Veins" inherits="PresetHugeVeins"/>'
        self.assertEqual(output, expected)

    def test_name_is_required(self):
        x = etree.Element("Parent")
        with self.assertRaises(ValueError):
            add_standard_attributes(x, name=None)

        with self.assertRaises(ValueError):
            add_standard_attributes(x, name=" ")

        with self.assertRaises(ValueError):
            add_standard_attributes(x, name="    ")


@contract(xml_element=etree._Element, color="str|None")
def add_debug_display_attributes(xml_element, color):
    if color is None:
        return

    assert xml_element.tag in ("StandardGen", "Veins", "Cloud"), ValueError

    assert len(color) == 6, \
        ValueError("Colour %s is not 6 hexadecimal characters. Example of correct format: 3366FF." % color)

    color = color.upper()
    assert all([char in "0123456789ABCDEF" for char in color]), \
        ValueError("Colour %s is not 6 hexadecimal characters. Example of correct format: 3366FF." % color)

    # Color strings are in ARGB format.
    # i.e. 0xFF______ is fully opaque.
    #      0x00______ is fully transparent.
    #      0x__FF0000 is red.
    #      0x__00FF00 is green.
    #      0x__0000FF is blue.
    #
    # For our purposes, we will always use an opacity of 0x60 (about 40%.)
    color_string = "0x60" + color

    # We always want wireframes.
    xml_element.attrib["drawWireframe"] = "true"
    xml_element.attrib["wireframeColor"] = color_string

    # We never want bounding boxes.
    xml_element.attrib["drawBoundBox"] = "false"
    xml_element.attrib["boundBoxColor"] = color_string

    # This function modifies the xml_element in place.
    # No value is returned.


class TestAddDebugDisplayAttributes(unittest.TestCase):
    pass


@contract(p=defaultdict, setting_names="list(str)", distribution_element=etree._Element)
def add_setting_elements(p, setting_names, distribution_element):
    # Adds one or more <Setting> elements to the parent distribution element, i.e. a <Veins> element.
    #
    # The parent distribution element, i.e. the <Veins> element is modified in-place.
    # Therefore no value is returned from this function.
    #
    # One <Setting> element will be generated for each element in setting_names.
    # ex: if setting_names = ["Size","Freq","Height"] ...
    # ... then three <Setting> elements will be generated:
    # <Setting name="Size" />, <Setting name="Freq" />, <Setting name="Height" />.
    #
    # Each <Setting> has attributes "avg", "range", "type", and (sometimes??) "scaleTo".
    # These are passed in via the argument p (short for parameters).
    # p is a dictionary which contains keys such as "Size_avg", "Freq_range", and "Height_type".
    #
    # The names of the keys in p are defined in the Excel spreadsheet(s).
    #
    # Because p is a special type of dictionary (a 'defaultdict'), not all parameters need to be supplied.
    # If we ask for p["Size_avg"] and it doesn't exist, we will get the value None.

    for setting_name in setting_names:
        attributes = ["_avg", "_range", "_type", "_scaleTo"]
        attributes_blank = [(setting_name + a) not in p for a in attributes]

        # If all attributes for this setting are blank, skip it.
        if all(attributes_blank):
            continue

        setting_element = etree.SubElement(distribution_element, "Setting")
        setting_element.attrib["name"] = setting_name  # example: name = MotherlodeSize

        p_key = setting_name + "_avg"  # example: p_key = MotherlodeSize_avg
        if p[p_key] is not None:
            setting_element.attrib["avg"] = ":= %s * _default_" % p[p_key]  # i.e. ":= 1.234 * _default_"

        p_key = setting_name + "_range"
        if p[p_key] is not None:
            setting_element.attrib["range"] = ":= %s * _default_" % p[p_key]

        p_key = setting_name + "_type"
        if p[p_key] is not None:
            setting_element.attrib["type"] = p[p_key]

        p_key = setting_name + "_scaleTo"
        if p[p_key] is not None:
            setting_element.attrib["scaleTo"] = p[p_key]

            # This function modifies the xml_element in place.
            # No value is returned.


class TestAddSettingElements(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
