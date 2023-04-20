
def query_serialize(obj, related=True):
    '''
    With common.minxins.DictionaryMixin to serialize QuerySet.
    @param
    obj     : QuerySet
    related : Includes both field values and related pk if True
    '''
    datas = [o.to_dict(related) for o in obj]
    return datas



