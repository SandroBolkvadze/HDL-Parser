from core.engine.parse_engine import ParseEngine, DefaultParseEngine

if __name__ == "__main__":
    hdl = """
        // This file is part of www.nand2tetris.org
        **
         * And gate:
         * if (a and b) out = 1, else out = 0 
         */
    """

    engine = DefaultParseEngine()
    engine.parse(hdl)

    print(engine.chip_name)
    print(engine.input_pins)
    print(engine.output_pins)
    print(engine.chip_parts)
