from core.engine.parse_engine import ParseEngine, DefaultParseEngine

if __name__ == "__main__":
    hdl = """
    CHIP Mux4Way16 {
        IN
         a;
        OUT
         b;
        
        PARTS:
        Mux16(a     =a, b=b, sel=sel[0], out=aMuxb);
    }
    """

    engine = DefaultParseEngine()
    chip_description = engine.parse(hdl)

    print(chip_description.chip_name)
    print(chip_description.input_pins)
    print(chip_description.output_pins)
    print(chip_description.chip_parts)
    print(chip_description.chip_connections)
