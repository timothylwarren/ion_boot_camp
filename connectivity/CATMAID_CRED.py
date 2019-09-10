def CATMAID_CRED():
    import pymaid
    myInstance = pymaid.CatmaidInstance( 'https://neurocean.janelia.org/catmaidL1',
                                         'Sales',
                                         'snow tree branches',
                                          '7fa63015863b26b647a00a9f420425bb2eef3a9b'
                                         );
    return (myInstance)