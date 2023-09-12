

class ArrayComposition():
    
    from pandas import DataFrame, Series
    from numpy import array
    
    def __init__(self, dataframe: DataFrame, fl_normalize: bool):
        self.dataframe = dataframe
        self.fl_normalize = fl_normalize
    
    def get_columns(self) -> list:
        return list(self.dataframe.columns)
    
    def get_array_type(self, column: Series) -> array:
        return self.dataframe[f'{column}'].dtype.type
    
    def get_array_from_series(self, column: Series) -> array:
        return self.dataframe[f'{column}'].to_numpy(dtype=self.get_array_type(column=column))
    
    def get_non_duplicated_array_from_series(self, column: Series, return_counts=True) -> array:
        from numpy import unique
        uniques, counts = unique(self.get_array_from_series(column=column), return_index=False, return_counts=True)
        if return_counts:            
            return uniques, counts
        else:
            return uniques
    
    def get_prometheeii_array_generator(self, column: Series, pref_func, **kwargs):
        from numpy import vectorize, repeat
        
        def generator_engine():
            while True:
                value = yield
                pi_positive = value - arr
                pi_negative = arr - value
                preference_arr = pref_func(mode, pi_positive, cost_criteria, weight, indiference_limiar, preference_limiar)
                preference_arr = repeat(preference_arr, value_counts)
                prefered_arr = pref_func(mode, pi_negative, cost_criteria, weight, indiference_limiar, preference_limiar)
                prefered_arr = repeat(prefered_arr, value_counts)
                pi_positive = preference_arr.sum()
                pi_negative = prefered_arr.sum()
                pi_liquid = pi_positive - pi_negative
                yield pi_liquid
        
        def generator_processor(value):
            generator = generator_engine()
            next(generator)
            result = generator.send(value)
            return result
        
        mode = kwargs.get('mode', 1)
        cost_criteria = kwargs.get('cost_criteria', 0)
        weight = kwargs.get('weight', 1)
        indiference_limiar = kwargs.get('indiference_limiar', 0)
        preference_limiar = kwargs.get('preference_limiar', 0)        
        arr, value_counts = self.get_non_duplicated_array_from_series(column=column)
        arr_function = vectorize(generator_processor)
        arr_preferences = arr_function(arr)
        if self.fl_normalize:
            n_elements = arr_preferences.shape[0]
            outranking = arr_preferences / (n_elements - 1)
            return outranking
        else:
            return arr_preferences


