from core.engine import Engine

if __name__ == "__main__":
    hdl = """
        /* dasd asd asd asdasd asd 
            dsadasdasd
        */
        // dasd sad asd asd asd asdsa
        
        // dasda sdasd asd as dsadadsad
        CHIP abcd {
            IN a;
            OUT;
        }
    """

    engine = Engine(hdl)
    engine.parse()
    print(engine.chip_name)


