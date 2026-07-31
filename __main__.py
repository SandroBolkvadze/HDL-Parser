from core.engine import Engine

if __name__ == "__main__":
    hdl = """
        /* dasd asd asd asdasd asd 
            dsadasdasd
        */
        // dasd sad asd asd asd asdsa
        abcd
        // dasda sdasd asd as dsadadsad
        zzz
    """

    engine = Engine(hdl)
    engine.advance()
    print(hdl[engine.index])
    engine.index += 4
    engine.advance()
    print(hdl[engine.index])


