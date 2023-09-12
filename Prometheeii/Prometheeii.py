from Engine.ArrayComposition import ArrayComposition
from Evaluator.Compatibilizer import MethodCompatibilizer

class Prometheeii():
    
    def __init__(self, dataframe, canditates_column, metrics_specs, **kwargs):
        self.dataframe = dataframe
        self.canditates_column = canditates_column
        self.metrics_specs = metrics_specs
        self.fl_normalize = kwargs.get('fl_normalize', False)
    
    
    def preference_comparison(self, mode, arr, cost_criteria, weight, indiference_limiar, preference_limiar):
        from numpy import select
        
        if cost_criteria == 0:
            generic_statement = arr<=0
            indiference_statement = arr<=indiference_limiar
        
        else:
            generic_statement = arr>=0
            indiference_statement = arr>=(indiference_limiar)*(-1)
        
        def type_i():
            statement=[generic_statement]
            return select(statement, [0], 1*weight)
        
        def type_ii():
            statement=[indiference_statement]
            return select(statement, [0], 1*weight)
        
        def type_iii():
            statement=[generic_statement, indiference_statement]
            return select(statement, [0, (1/preference_limiar)*arr*weight if preference_limiar != 0 else 0], 1*weight)
        
        return {
            1: type_i(),
            2: type_ii(),
            3: type_iii()
        }.get(mode)
    
    
    def get_value_scores(self):
        from pandas import DataFrame
        dataframes_store = dict()        
        for metric in self.metrics_specs.keys():
            metric_spec = self.metrics_specs.get(metric)
            metric_name = metric
            mode = metric_spec.get('mode', 1)
            weight = metric_spec.get('weight')
            cost_criteria = metric_spec.get('cost_criteria', 0)
            preference_limiar = metric_spec.get('preference_limiar', 1)
            indiference_limiar = metric_spec.get('indiference_limiar', 0)
            array_composition_instance = ArrayComposition(self.dataframe, self.fl_normalize) 
            arr_unique = array_composition_instance.get_non_duplicated_array_from_series(
                metric_name, 
                return_counts=False
            )          
            arr_prometheeii = array_composition_instance.get_prometheeii_array_generator(
                column=metric_name, 
                pref_func=self.preference_comparison,
                mode=mode,
                cost_criteria=cost_criteria,
                weight=weight,
                indiference_limiar=indiference_limiar,
                preference_limiar=preference_limiar
            )
            data_frame = DataFrame(
                {
                    f'{metric_name}': arr_unique,
                    f'score_{metric_name}': arr_prometheeii
                }
            )
            dataframes_store[metric] = data_frame
        return dataframes_store
    
    
    def get_scored_dataframe(self):
        compatibilizer_instance = MethodCompatibilizer(
            method='promethee_ii',
            dataframe=self.dataframe, 
            canditates_column=self.canditates_column, 
            metrics_specs= self.metrics_specs
        )
        compatibilizer_instance.check_metrics_specs()
        metric_scores = self.get_value_scores()
        df_promethee_ii = self.dataframe
        for metric in self.metrics_specs.keys():
            df_score_metric = metric_scores.get(metric)
            df_promethee_ii = df_promethee_ii.merge(df_score_metric, on=metric)
        score_columns = [column for column in df_promethee_ii.filter(like='score_').columns]
        df_promethee_ii['score_candidate'] = df_promethee_ii[score_columns].sum(axis=1)
        df_promethee_ii['ranking'] = df_promethee_ii['score_candidate'].rank(ascending=False)
        return df_promethee_ii


    
